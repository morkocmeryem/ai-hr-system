import csv
import os
import django

# Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
django.setup()

from panel.models import JobPosting, UploadedCV

# Job verilerini yükle
def load_fake_jobs():
    with open('fake_jobs.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            JobPosting.objects.create(
                title=row['title'],
                department=row['department'],
                is_active=row['is_active'].lower() == 'true'  # "true" → True
            )
    print("İlan verileri yüklendi ✅")

# CV verilerini yükle
def load_fake_cvs():
    with open('fake_cvs.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            UploadedCV.objects.create(
                candidate_name=row['candidate_name']
                # Burada file alanı boş kalır ama test için yeterli
            )
    print("CV verileri yüklendi ✅")

if __name__ == '__main__':
    load_fake_jobs()
    load_fake_cvs()
