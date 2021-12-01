from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_to_home),
    path('home/', views.home, name='home'),
    path('peoples/', views.peoples, name='peoples'),
    path('report/', views.report_issue, name='report_issue'),
    path('report/<int:pk>', views.issue_detail, name='issue_detail'),
]
