from django.contrib import admin
from .models import JobPosting
from .models import UploadedCV

admin.site.register(JobPosting)

admin.site.register(UploadedCV)
