from django.urls import path, include

from . import views

urlpatterns = [
    path('cabinet/<int:user_id>/', views.cabinet_view),
    path('cabinet/<int:user_id>/reports/', views.all_report_view),
    path('cabinet/<int:user_id>/reports/<int:report_id>', views.report_view),
]