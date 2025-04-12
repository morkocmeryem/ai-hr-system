import os
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import JobPosting, UploadedCV
from .forms import JobPostingForm
from .models import UploadedCV

def application_analysis_view(request):
    uploaded_cvs = UploadedCV.objects.all()
    return render(request, "application_analysis.html", {"cvs": uploaded_cvs})

def cv_detail_view(request, id):
    cv = get_object_or_404(UploadedCV, id=id)
    return render(request, 'cv_detail.html', {'cv': cv})

# -------------------- Dashboard --------------------
def dashboard_view(request):
    aktif_ilan_sayisi = JobPosting.objects.filter(is_active=True).count()
    cv_sayisi = UploadedCV.objects.count()
    context = {
        "aktif_ilan": aktif_ilan_sayisi,
        "cv_sayisi": cv_sayisi,
        "uyumlu_cv": 36  # şimdilik sabit
    }
    return render(request, "dashboard.html", context)

# -------------------- Login --------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "1234":
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Kullanıcı adı veya şifre yanlış"})
    return render(request, "login.html")

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

# -------------------- CV Upload (Manuel) --------------------
def upload_cv_view(request):
    if request.method == 'POST' and request.FILES.get('cv_file'):
        file = request.FILES['cv_file']
        UploadedCV.objects.create(file=file)
        return redirect('upload_cv')

    uploaded_files = UploadedCV.objects.all()
    return render(request, 'upload_cv.html', {'files': uploaded_files})

def delete_cv_view(request, id):
    cv = get_object_or_404(UploadedCV, id=id)
    if request.method == "POST":
        cv.file.delete()
        cv.delete()
    return redirect('upload_cv')

from .models import UploadedCV
# -------------------- Başvuru Yönetimi --------------------
def upload_cv_view(request):
    if request.method == 'POST' and request.FILES.get('cv_file'):
        file = request.FILES['cv_file']
        UploadedCV.objects.create(file=file)
        return redirect('upload_cv')

    uploaded_files = UploadedCV.objects.exclude(file='')  # boş dosyaları gösterme
    return render(request, 'upload_cv.html', {'files': uploaded_files})
