from django.db import models

class JobPosting(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.file.name

class UploadedCV(models.Model):
        file = models.FileField(upload_to='uploaded_cvs/')
        uploaded_at = models.DateTimeField(auto_now_add=True)
        # isteğe bağlı olarak aday adı gibi alanlar da ekleyebilirsin
        candidate_name = models.CharField(max_length=100, blank=True)
