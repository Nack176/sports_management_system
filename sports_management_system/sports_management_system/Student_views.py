from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Student_Notification,Student,Student_Feedback,Student_Leave,Tournament,Attendance,Attendance_Report
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):
    return render(request,'Student/home.html')

@login_required(login_url='/')
def STUDENT_NOTIFICATIONS(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id=student_id)
        context = {
            'notification':notification,
        }
        return render(request,'Student/notification.html',context)

@login_required(login_url='/')
def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notifications')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)
    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'Student/feedback.html',context)

@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin = request.user.id)
        feedbacks = Student_Feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply = "",
            )
        feedbacks.save()
        return redirect('student_feedback')
    
@login_required(login_url='/')
def STUDENT_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    student_leave_history = Student_Leave.objects.filter(student_id = student)
    context = {
        'student_leave_history':student_leave_history,
    }
    return render(request,'Student/apply_leave.html',context)

@login_required(login_url='/')
def STUDENT_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        
        student_id = Student.objects.get(admin = request.user.id)
        student_leave = Student_Leave(
            student_id = student_id,
            data = leave_date,
            message = leave_message,
        )
    
        student_leave.save()
        messages.success(request,'Leave Are Successfully Sent')
        return redirect('student_leave')
    
@login_required(login_url='/')
def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    tournament = Tournament.objects.filter(sport = student.sport_id)
    action = request.GET.get('action')

    get_tournament = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            tournament_id = request.POST.get('tournament_id')
            get_tournament = Tournament.objects.get(id = tournament_id)

            
            attendance_report = Attendance_Report.objects.filter(student_id = student,attendance_id__tournament_id = tournament_id)
    context = {
        'tournament':tournament,
        'action':action,
        'get_tournament':get_tournament,
        'attendance_report':attendance_report,
    }
    
    return render(request,'Student/view_attendance.html',context)