from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('admin-login/',views.admin_login,name='admin_login'),
    path('user-list/',views.user_list,name='user_list'),
    path('create-user/',views.create_user,name='create_user'),
    path('edit-user/<int:user_id>/',views.edit_user,name='edit_user'),
    path('delete-user/<int:user_id>/',views.delete_user,name='delete_user'),
    path('logout/',views.logout,name='logout'),
]