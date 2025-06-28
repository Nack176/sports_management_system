from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Sport,Session_Year,CustomUser,Student,Staff,Tournament,Staff_Notification,Staff_Leave,Staff_Feedback,Student_Notification,Student_Feedback,Student_Leave,Attendance,Attendance_Report
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):

    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    sport_count = Sport.objects.all().count()
    tournament_count = Tournament.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()

    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'sport_count':sport_count,
        'tournament_count':tournament_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }

    return render(request,'Hod/home.html',context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    sport = Sport.objects.all()
    session_year = Session_Year.objects.all()

    if request.method  == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        sport_id = request.POST.get('sport_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email Is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username Is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username =username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()

            sport = Sport.objects.get(id=sport_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = address,
                gender = gender,
                sport_id = sport,
                session_year_id = session_year,
            )
            student.save()
            messages.success(request, user.first_name + ' ' + user.last_name + ' Are Successfully Added')
            return redirect('add_student')

    context = {
        'sport':sport,
        'session_year':session_year,
    }

    return render(request,'Hod/add_student.html',context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id=id)
    sport = Sport.objects.all()
    session_year = Session_Year.objects.all()


    context = {
        'student':student,
        'sport':sport,
        'session_year':session_year,
    }

    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        sport_id = request.POST.get('sport_id')
        session_year_id = request.POST.get('session_year_id')

        # Validate student_id, sport_id and session_year_id
        if not student_id or student_id == "" or sport_id == "Select Sport" or session_year_id == "Select Session":
            messages.error(request, "Please provide valid Student, Sport and Session Year.")
            return redirect('edit_student', id=student_id if student_id else 0)

        user = CustomUser.objects.get(id = student_id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != '' and password != None:
            user.set_password(password)
        if profile_pic != '' and profile_pic != None:
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender
        
        sport = Sport.objects.get(id = sport_id)
        student.sport_id = sport

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')
        
    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student_user = CustomUser.objects.get(id=admin)
    try:
        student = Student.objects.get(admin=student_user)
        # Delete related Attendance_Report objects to avoid FK constraint error
        from app.models import Attendance_Report
        Attendance_Report.objects.filter(student_id=student).delete()
    except Student.DoesNotExist:
        pass
    student_user.delete()
    messages.success(request,'Record Are Successfully Deleted !')

    return redirect('view_student')

@login_required(login_url='/')
def ADD_SPORT(request):
    if request.method == 'POST':
        sport_name = request.POST.get('sport_name')
        
        sport = Sport(
            name = sport_name,
        )
        sport.save()
        messages.success(request,'Sport Are Successfully Created !')
        return redirect('add_sport')
    return render(request,'Hod/add_sport.html')

@login_required(login_url='/')
def VIEW_SPORT(request):
    sport = Sport.objects.all()
    context = {
        'sport' : sport,
    }
    return render(request,'Hod/view_sport.html',context)

@login_required(login_url='/')
def EDIT_SPORT(request,id):
    sport = Sport.objects.get(id = id)
    context = {
        'sport' : sport,
    }
    return render(request,'Hod/edit_sport.html',context)

@login_required(login_url='/')
def UPDATE_SPORT(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sport_id = request.POST.get('sport_id')

        sport = Sport.objects.get(id = sport_id)
        sport.name = name
        sport.save()
        messages.success(request,'Sport Are Successfully Updated !')
        return redirect('view_sport')

        
    return render(request,'Hod/edit_sport.html')

@login_required(login_url='/')
def DELETE_SPORT(request,id):
    sport = Sport.objects.get(id = id)
    try:
        from app.models import Student, Attendance_Report, Attendance, Tournament
        # Delete Attendance_Report and Attendance related to Students of this sport
        students = Student.objects.filter(sport_id=sport)
        for student in students:
            Attendance_Report.objects.filter(student_id=student).delete()
        # Delete Attendance related to Tournaments of this sport
        tournaments = Tournament.objects.filter(sport=sport)
        for tournament in tournaments:
            Attendance.objects.filter(tournament_id=tournament).delete()
        # Delete Students of this sport
        students.delete()
    except Exception:
        pass
    sport.delete()
    messages.success(request,'Sport Are Successfully Deleted !')

    return redirect('view_sport')

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email Is Already Taken !')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username Is Already Taken !')
            return redirect('add_staff')
        
        else:
            user = CustomUser(first_name=first_name,last_name=last_name,email=email,username=username,profile_pic=profile_pic,user_type=2)
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender
                )
            staff.save()
            messages.success(request,'Staff Are Successfully Added !')
            return redirect('add_staff')

    return render(request,'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    
    context = {
        'staff':staff,
    }

    return render(request,'Hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id=id)

    context = {
        'staff':staff,
    }

    return render(request,'Hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password != '' and password != None:
            user.set_password(password)
        if profile_pic != '' and profile_pic != None:
            user.profile_pic = profile_pic

        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender
        staff.save()
        messages.success(request,'Staff Is Successfully Updated !')
        return redirect('view_staff')


    return render(request,'Hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff_user = CustomUser.objects.get(id=admin)
    try:
        staff = Staff.objects.get(admin=staff_user)
        from app.models import Staff_Notification, Staff_Leave, Staff_Feedback, Tournament, Attendance
        Staff_Notification.objects.filter(staff_id=staff).delete()
        Staff_Leave.objects.filter(staff_id=staff).delete()
        Staff_Feedback.objects.filter(staff_id=staff).delete()
        # Delete Attendance related to Tournaments of this staff
        tournaments = Tournament.objects.filter(staff=staff)
        for tournament in tournaments:
            Attendance.objects.filter(tournament_id=tournament).delete()
        tournaments.delete()
    except Staff.DoesNotExist:
        pass
    staff_user.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_TOURNAMENT(request):
    sport = Sport.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        tournament_name = request.POST.get('tournament_name')
        sport_id = request.POST.get('sport_id')
        staff_id = request.POST.get('staff_id')

        sport = Sport.objects.get(id = sport_id)
        staff = Staff.objects.get(id = staff_id)

        tournament = Tournament(
            name = tournament_name,
            sport = sport,
            staff = staff,
        )
        tournament.save()
        messages.success(request,'Tournament Are Successfully Added !')
        return redirect('add_tournament')

    context = {
        'sport':sport,
        'staff':staff,
    }

    return render(request,'Hod/add_tournament.html',context)

@login_required(login_url='/')
def VIEW_TOURNAMENT(request):
    tournament = Tournament.objects.all()

    # Prepare list with created_at formatted for each tournament
    tournament_list = []
    for t in tournament:
        tournament_list.append({
            'id': t.id,
            'name': t.name,
            'sport': t.sport,
            'staff': t.staff,
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else 'N/A',
            'updated_at': t.updated_at.strftime('%Y-%m-%d %H:%M:%S') if t.updated_at else 'N/A',
        })

    context = {
        'tournament': tournament_list,
    }

    return render(request,'Hod/view_tournament.html',context)

@login_required(login_url='/')
def EDIT_TOURNAMENT(request,id):
    tournament = Tournament.objects.get(id = id)
    sport = Sport.objects.all()
    staff = Staff.objects.all()


    context = {
        'tournament':tournament,
        'sport':sport,
        'staff':staff,
    }

    return render(request,'Hod/edit_tournament.html',context)

@login_required(login_url='/')
def UPDATE_TOURNAMENT(request):
    if request.method == 'POST':
        tournament_id = request.POST.get('tournament_id')
        tournament_name = request.POST.get('tournament_name')
        sport_id = request.POST.get('sport_id')
        staff_id = request.POST.get('staff_id')

        # Validate sport_id and staff_id
        if sport_id == "Select Sport" or staff_id == "Select Staff":
            messages.error(request, "Please select valid Sport and Staff.")
            return redirect('edit_tournament', id=tournament_id)

        sport = Sport.objects.get(id = sport_id)
        staff = Staff.objects.get(id = staff_id)

        tournament = Tournament(
            id = tournament_id,
            name = tournament_name,
            sport = sport,
            staff = staff,
            )
        tournament.save()
        messages.success(request,'Tournament Are Successfully Updated !')
        return redirect('view_tournament')
    
@login_required(login_url='/')
def DELETE_TOURNAMENT(request,id):
    try:
        tournament = Tournament.objects.get(id=id)
        from app.models import Attendance, Attendance_Report
        # Delete Attendance_Report related to Attendance of this tournament
        attendances = Attendance.objects.filter(tournament_id=tournament)
        for attendance in attendances:
            Attendance_Report.objects.filter(attendance_id=attendance).delete()
        # Delete Attendance related to this tournament
        attendances.delete()
        # Delete the tournament
        tournament.delete()
        messages.success(request,'Tournament Are Successfully Deleted !')
    except Tournament.DoesNotExist:
        messages.error(request,'Tournament Not Found!')
    return redirect('view_tournament')

@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Created !')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context = {
        'session':session,
    }
    return render(request,'Hod/view_session.html',context)

@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session = Session_Year.objects.filter(id = id)

    context = {
        'session':session,
    }

    return render(request,'Hod/edit_session.html',context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Updated !')
        return redirect('view_session')
    
@login_required(login_url='/')
def DELETE_SESSION(request,id):
    session = Session_Year.objects.get(id = id)
    try:
        from app.models import Student, Attendance, Attendance_Report
        # Delete Attendance_Report related to Attendance of this session
        attendances = Attendance.objects.filter(session_year_id=session)
        for attendance in attendances:
            Attendance_Report.objects.filter(attendance_id=attendance).delete()
        # Delete Attendance related to this session
        attendances.delete()
        # Delete Students of this session
        students = Student.objects.filter(session_year_id=session)
        students.delete()
    except Exception:
        pass
    session.delete()
    messages.success(request,'Session Are Successfully Deleted !')
    return redirect('view_session')

@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request,'Hod/staff_notification.html',context)

@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Are Successfully Sent !')
        return redirect('staff_send_notification')
    
@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_Leave.objects.all()

    context = {
        'staff_leave':staff_leave,
    }

    return render(request,'Hod/staff_leave.html',context)

@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_Leave.objects.all()
    context = {
        'student_leave':student_leave,
    }
    return render(request,'Hod/student_leave.html',context)

@login_required(login_url='/')
def STUDENT_APPROVE_LEAVE(request,id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='/')
def STUDENT_DISAPPROVE_LEAVE(request,id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback':feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'Hod/staff_feedback.html',context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request,'Feedback Are Successfully Sent !')
        return redirect('staff_feedback_reply')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback':feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'Hod/student_feedback.html',context)

@login_required(login_url='/')
def REPLY_STUDENT_FEEDBACK(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request,'Feedback Are Successfully Sent !')
        return redirect('get_student_feedback')

@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context = {
        'student':student,
        'notification':notification,
    }
    return render(request,'Hod/student_notification.html',context)

@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin = student_id)
        stud_notification = Student_Notification(
            student_id = student,
            message = message,
            
        )
        stud_notification.save()
        messages.success(request,'Student Notification Are Successfully Sent !')
        return redirect('student_send_notification')

@login_required(login_url='/')
def VIEW_ATTENDANCE(request):
    
    tournament = Tournament.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')
    get_tournament = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            tournament_id = request.POST.get('tournament_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            # Validate tournament_id and session_year_id are integers and not default strings
            try:
                tournament_id_int = int(tournament_id)
                session_year_id_int = int(session_year_id)
            except (ValueError, TypeError):
                messages.error(request, "Please select valid Tournament and Session Year.")
                return redirect('view_attendance')

            get_tournament = Tournament.objects.get(id = tournament_id_int)
            get_session_year = Session_Year.objects.get(id = session_year_id_int)
            attendance = Attendance.objects.filter(tournament_id = get_tournament, attendance_data = attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id = attendance_id)
    context = {
        'tournament':tournament,
        'session_year':session_year,
        'action':action,
        'get_tournament':get_tournament,
        'get_session_year':get_session_year,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report,
    }
    return render(request,'Hod/view_attendance.html',context)
