from django.urls import path
from . import AdminView, LoginView, SignUpView

urlpatterns = [
    path('register/', SignUpView.admin_signup, name='admin_signup'),
    path('', LoginView.admin_login, name='admin_login'),
    path('admin_logout/', LoginView.admin_logout, name='admin_logout'),
    path('add_merit_student/', AdminView.add_merit_student, name='add_merit_student'),
    path('edit_merit_student/<int:pk>/', AdminView.edit_merit_student, name='edit_merit_student'),
    path('manage_merit_student/', AdminView.manage_merit_student, name='manage_merit_student'),
    path('add_demerit_student/', AdminView.add_demerit_student, name='add_demerit_student'),
    path('edit_demerit_student/<int:pk>/', AdminView.edit_demerit_student, name='edit_demerit_student'),
    path('manage_demerit_student/', AdminView.manage_demerit_student, name='manage_demerit_student'),
    path('ajax/load-classes/', AdminView.load_classes, name='load_classes'),
    path('merit-student/delete/<int:pk>/', AdminView.delete_merit_student, name='delete_merit_student'),
    path('demerit-student/delete/<int:pk>/', AdminView.delete_demerit_student, name='delete_demerit_student'),
    path('dashboard/', AdminView.dashboard, name='dashboard'),
    path('tables/', AdminView.tables, name='tables'),
    path('charts_view/', AdminView.charts_view, name='charts_view'),
    path('forgot-password/', LoginView.forgot_password, name='forgot_password'),
]   

