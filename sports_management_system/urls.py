
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from .import views,Staff_views,Student_views,Hod_views

urlpatterns = [
    path('admin/login/', lambda request: redirect('/')),
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name='base'),

    #login path
    path('',views.LOGIN,name='login'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('logout',views.doLogout,name='logout'),

    # profile update
    path('Profile',views.PROFILE,name='profile'),
    path('Profile/update',views.PROFILE_UPDATE,name='profile_update'),

    #This is Hod Panel url
    path('Hod/Home',Hod_views.HOME,name='hod_home'),
    path('Hod/Student/Add',Hod_views.ADD_STUDENT,name='add_student'),
    path('Hod/Student/View',Hod_views.VIEW_STUDENT,name='view_student'),
    path('Hod/Student/Edit/<str:id>',Hod_views.EDIT_STUDENT,name='edit_student'),
    path('Hod/Student/Update',Hod_views.UPDATE_STUDENT,name='update_student'),
    path('Hod/Student/Delete/<str:admin>',Hod_views.DELETE_STUDENT,name='delete_student'),

    path('Hod/Staff/Add',Hod_views.ADD_STAFF,name='add_staff'),
    path('Hod/Staff/View',Hod_views.VIEW_STAFF,name='view_staff'),
    path('Hod/Staff/Edit/<str:id>',Hod_views.EDIT_STAFF,name='edit_staff'),
    path('Hod/Staff/Update',Hod_views.UPDATE_STAFF,name='update_staff'),
    path('Hod/Staff/Delete/<str:admin>',Hod_views.DELETE_STAFF,name='delete_staff'),

    path('Hod/Sport/Add',Hod_views.ADD_SPORT,name='add_sport'),
    path('Hod/Sport/View',Hod_views.VIEW_SPORT,name='view_sport'),
    path('Hod/Sport/Edit/<str:id>',Hod_views.EDIT_SPORT,name='edit_sport'),
    path('Hod/Sport/Update',Hod_views.UPDATE_SPORT,name='update_sport'),
    path('Hod/Sport/Delete/<str:id>',Hod_views.DELETE_SPORT,name='delete_sport'),

    path('Hod/Tournament/Add',Hod_views.ADD_TOURNAMENT,name='add_tournament'),
    path('Hod/Tournament/View',Hod_views.VIEW_TOURNAMENT,name='view_tournament'),
    path('Hod/Tournament/Edit/<str:id>',Hod_views.EDIT_TOURNAMENT,name='edit_tournament'),
    path('Hod/Tournament/Update',Hod_views.UPDATE_TOURNAMENT,name='update_tournament'),
    path('Hod/Tournament/Delete/<str:id>',Hod_views.DELETE_TOURNAMENT,name='delete_tournament'),

    path('Hod/Session/Add',Hod_views.ADD_SESSION,name='add_session'),
    path('Hod/Session/View',Hod_views.VIEW_SESSION,name='view_session'),
    path('Hod/Session/Edit/<str:id>',Hod_views.EDIT_SESSION,name='edit_session'),
    path('Hod/Session/Update',Hod_views.UPDATE_SESSION,name='update_session'),
    path('Hod/Session/Delete/<str:id>',Hod_views.DELETE_SESSION,name='delete_session'),

    path('Hod/Staff/Send_Notification',Hod_views.STAFF_SEND_NOTIFICATION,name='staff_send_notification'),
    path('Hod/Staff/Save_Notification',Hod_views.SAVE_STAFF_NOTIFICATION,name='save_staff_notification'),

    path('Hod/Student/Send_Notification',Hod_views.STUDENT_SEND_NOTIFICATION,name='student_send_notification'),
    path('Hod/Student/Save_Notification',Hod_views.SAVE_STUDENT_NOTIFICATION,name='save_student_notification'),


    path('Hod/Staff/Leave_view',Hod_views.STAFF_LEAVE_VIEW,name='staff_leave_view'),
    path('Hod/Staff/Approve_leave/<str:id>',Hod_views.STAFF_APPROVE_LEAVE,name='staff_approve_leave'),
    path('Hod/Staff/Disapprove_leave/<str:id>',Hod_views.STAFF_DISAPPROVE_LEAVE,name='staff_disapprove_leave'),

    path('Hod/Student/Leave_view',Hod_views.STUDENT_LEAVE_VIEW,name='student_leave_view'),
    path('Hod/Student/Approve_leave/<str:id>',Hod_views.STUDENT_APPROVE_LEAVE,name='student_approve_leave'),
    path('Hod/Student/Disapprove_leave/<str:id>',Hod_views.STUDENT_DISAPPROVE_LEAVE,name='student_disapprove_leave'),

    path('Hod/Staff/Feedback',Hod_views.STAFF_FEEDBACK,name='staff_feedback_reply'),
    path('Hod/Staff/Feedback/save',Hod_views.STAFF_FEEDBACK_SAVE,name='staff_feedback_reply_save'),

    path('Hod/Student/Feedback',Hod_views.STUDENT_FEEDBACK,name='get_student_feedback'),
    path('Hod/Student/Feedback/reply/Save',Hod_views.REPLY_STUDENT_FEEDBACK,name='reply_student_feedback'),

    path('Hod/View_attendance',Hod_views.VIEW_ATTENDANCE,name='view_attendance'),


    #This is Staff Panel url
    path('Staff/Home',Staff_views.HOME,name='staff_home'),

    path('Staff/Notifications',Staff_views.NOTIFICATIONS,name='notifications'),
    path('Staff/mark_as_done/<str:status>',Staff_views.STAFF_NOTIFICATION_MARK_AS_DONE,name='staff_notification_mark_as_done'),

    path('Staff/Apply_leave',Staff_views.STAFF_APPLY_LEAVE,name='staff_apply_leave'),
    path('Staff/Apply_leave_save',Staff_views.STAFF_APPLY_LEAVE_SAVE,name='staff_apply_leave_save'),

    path('Staff/Feedback',Staff_views.STAFF_FEEDBACK,name='staff_feedback'),
    path('Staff/Feedback/Save',Staff_views.STAFF_FEEDBACK_SAVE,name='staff_feedback_save'),

    path('Staff/Take_attendance',Staff_views.STAFF_TAKE_ATTENDANCE,name='staff_take_attendance'),
    path('Staff/Save_Attendance',Staff_views.STAFF_SAVE_ATTENDANCE,name='staff_save_attendance'),
    path('Staff/View_attendance',Staff_views.STAFF_VIEW_ATTENDANCE,name='staff_view_attendance'),


    #This is student Panel url
    path('Student/Home',Student_views.HOME,name='student_home'),

    path('Student/Notifications',Student_views.STUDENT_NOTIFICATIONS,name='student_notifications'),
    path('Student/mark_as_done/<str:status>',Student_views.STUDENT_NOTIFICATION_MARK_AS_DONE,name='student_notification_mark_as_done'),

    path('Student/Feedback',Student_views.STUDENT_FEEDBACK,name='student_feedback'),
    path('Student/Feedback/Save',Student_views.STUDENT_FEEDBACK_SAVE,name='student_feedback_save'),

    path('Student/apply_for_leave',Student_views.STUDENT_LEAVE,name='student_leave'),
    path('Student/leave_save',Student_views.STUDENT_LEAVE_SAVE,name='student_leave_save'),
    
    path('Student/View_attendance',Student_views.STUDENT_VIEW_ATTENDANCE,name='student_view_attendance'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
