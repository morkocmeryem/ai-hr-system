import os
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import JobPosting, UploadedCV
from .forms import JobPostingForm

# --- AI model dosyaları
from .ml_model import train_and_match
from .training_data import cv_texts, job_descriptions


# -------------------- ANALİZ SAYFASI --------------------
from .cv_parser import extract_text_from_pdf  # PDF içerik çıkarımı için

def application_analysis_view(request):
    uploaded_cvs = UploadedCV.objects.exclude(file='')

    cv_texts = []
    for cv in uploaded_cvs:
        file_path = cv.file.path  # Dosyanın fiziksel yolu
        text = extract_text_from_pdf(file_path)
        if text.strip():
            cv_texts.append(text)
        else:
            cv_texts.append("Boş içerik")

    from .training_data import job_descriptions
    match_results = train_and_match(cv_texts, job_descriptions)

    analyzed_data = []
    for match in match_results:
        job_idx = match['job_id']
        job_text = job_descriptions[job_idx]
        matches = match['matches'][:3]
        for cv_idx, score in matches:
            analyzed_data.append({
                "job": job_text,
                "cv": cv_texts[cv_idx][:300],  # çok uzun metinleri kes
                "score": round(score * 100, 2)
            })

    return render(request, "application_analysis.html", {"analyzed_data": analyzed_data})


# -------------------- CV Detay --------------------
def cv_detail_view(request, id):
    cv = get_object_or_404(UploadedCV, id=id)
    cv_text = extract_text_from_pdf(cv.file.path)

    all_cv_texts = [cv_text]  # sadece bu tek CV'yi analiz edeceğiz
    match_results = train_and_match(all_cv_texts, job_descriptions)

    matched_jobs = []
    if match_results:
        for job_idx, score in match_results[0]["matches"][:3]:
            matched_jobs.append({
                "job": job_descriptions[job_idx],
                "score": round(score * 100, 2)
            })

    return render(request, 'cv_detail.html', {
        'cv': cv,
        'matched_jobs': matched_jobs
    })

# -------------------- Dashboard --------------------
def dashboard_view(request):
    aktif_ilan_sayisi = JobPosting.objects.filter(is_active=True).count()
    uploaded_cvs = UploadedCV.objects.exclude(file='')

    cv_texts = []
    for cv in uploaded_cvs:
        file_path = cv.file.path
        text = extract_text_from_pdf(file_path)
        cv_texts.append(text if text.strip() else "Boş içerik")

    match_results = train_and_match(cv_texts, job_descriptions)

    # 🔄 Kaç farklı CV eşleşmiş → set ile tekrarları önlüyoruz
    uyumlu_cv_ids = set()
    for match in match_results:
        for cv_idx, _ in match["matches"][:3]:
            uyumlu_cv_ids.add(cv_idx)

    total_score = 0
    score_count = 0
    uyumlu_cv_ids = set()

    for match in match_results:
        for cv_idx, score in match["matches"][:3]:
            uyumlu_cv_ids.add(cv_idx)
            total_score += score
            score_count += 1

    ortalama_skor = round((total_score / score_count) * 100, 2) if score_count else 0

    context = {
        "aktif_ilan": aktif_ilan_sayisi,
        "cv_sayisi": uploaded_cvs.count(),
        "uyumlu_cv": len(uyumlu_cv_ids),
        "ortalama_skor": ortalama_skor
    }
    return render(request, "dashboard.html", context)


# -------------------- Login --------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "1234":
            request.session["username"] = username  # Oturuma ekle
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Kullanıcı adı veya şifre yanlış"})
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")


# -------------------- Job CRUD --------------------
def job_management_view(request):
    jobs = JobPosting.objects.all()
    return render(request, 'job_management.html', {'jobs': jobs})


def add_job_view(request):
    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_management')
    else:
        form = JobPostingForm()
    return render(request, 'add_job.html', {'form': form})


def edit_job_view(request, id):
    job = get_object_or_404(JobPosting, id=id)
    if request.method == "POST":
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_management')
    else:
        form = JobPostingForm(instance=job)
    return render(request, 'edit_job.html', {'form': form, 'job': job})


def toggle_job_status_view(request, id):
    job = get_object_or_404(JobPosting, id=id)
    job.is_active = not job.is_active
    job.save()
    return redirect('job_management')


def job_list_view(request):
    jobs = JobPosting.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})


# -------------------- CV Upload & Delete --------------------
def upload_cv_view(request):
    if request.method == 'POST' and request.FILES.get('cv_file'):
        file = request.FILES['cv_file']
        UploadedCV.objects.create(file=file)
        return redirect('upload_cv')

    uploaded_files = UploadedCV.objects.exclude(file='')  # boş dosyaları gösterme
    return render(request, 'upload_cv.html', {'files': uploaded_files})


def delete_cv_view(request, id):
    cv = get_object_or_404(UploadedCV, id=id)
    if request.method == "POST":
        cv.file.delete()
        cv.delete()
    return redirect('upload_cv')
