from django.urls import path, include

from . import views
urlpatterns = [
    path('cabinet/', views.cabinet_view),
    path('token/', views.token),
    path('cabinet/<int:user_id>/', views.cabinet_view),
    path('check/', views.check_view),
    path('cabinet/register/', views.register_view),
    # reports
    path('cabinet/post_reports/', views.all_report_view),
    path('cabinet/get_reports/', views.projects_from_reports),
    path('cabinet/<int:user_id>/report/<int:report_id>', views.report_view),
    path('cabinet/report/<int:report_id>', views.report_view),
    # projects
    path('cabinet/projects/', views.all_projects_view),
    path('cabinet/projects_for_reports/', views.projects_for_reports),
    path('cabinet/<int:user_id>/project/<int:project_id>', views.project_view),
    path('cabinet/project/<int:project_id>', views.project_view),
    # roles
    path('groups/', views.group_view),
    path('actions/', views.action_view),
    path('salary/', views.salary),
    path('workers/', views.workers_departament),
    path('available_actions/', views.available_actions),
    path('admin/logs/', views.logs),
    path('admin/groups_admin/', views.groups_with_permission),
]





