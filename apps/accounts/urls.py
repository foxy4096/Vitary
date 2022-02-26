from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_edit, name='profile'),
    path('profile/advance/', views.advanced_settings, name='advance_settings'),
    path('profile/advance/delete/', views.delete_account, name='delete_account'),
    path('profile/advance/change_username/',
         views.change_username, name='change_username'),

    path('following/', views.following, name='following'),
    path('followers/', views.followers, name='followers'),

    path('group/create/', views.create_group, name='create_group'),
    path('group/<slug:group_slug>/', views.group_detail, name='group_detail'),
    path('group/<slug:group_slug>/edit/', views.edit_group, name='group_edit'),
    path('group/<slug:group_slug>/delete/', views.delete_group, name='group_delete'),
    path('group/<slug:group_slug>/invite/<str:username>/', views.invite_member, name='invite_member'),
    path('group/<slug:group_slug>/remove/<str:username>/', views.remove_member, name='remove_member'),
    path('group/<slug:group_slug>/accept/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
    path('group/<slug:group_slug>/decline/<int:invitation_id>/', views.reject_invitation, name='decline_invitation'),
    path('group/<slug:group_slug>/leave/', views.leave_group, name='leave_group'),

]
