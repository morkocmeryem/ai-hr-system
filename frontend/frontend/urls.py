from django.contrib import admin
from django.urls import path
from panel.views import (
    login_view,
    dashboard_view,
    job_list_view,
    job_management_view,
    add_job_view,
    toggle_job_status_view,
    edit_job_view,
    upload_cv_view,
    delete_cv_view,
    application_analysis_view,
    cv_detail_view,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Giriş ve Dashboard
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # İlanlar
    path('ilanlar/', job_list_view, name='job_list'),
    path('jobs/', job_management_view, name='job_management'),
    path('ilan-ekle/', add_job_view, name='add_job'),
    path('ilan-durum/<int:id>/', toggle_job_status_view, name='toggle_job_status'),
    path('ilan-duzenle/<int:id>/', edit_job_view, name='edit_job'),
    path('cv-detay/<int:id>/', cv_detail_view, name='cv_detail'),

    # CV Yükleme
    path('cv-yukle/', upload_cv_view, name='upload_cv'),
    path('cv-sil/<int:id>/', delete_cv_view, name='delete_cv'),
    path('basvurular/', application_analysis_view, name='application_analysis'),
]

# CV yükleme için gerekli ayar
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
