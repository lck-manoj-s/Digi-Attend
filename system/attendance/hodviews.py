import datetime
from attendance.forms import AddStudentForm,EditStudentForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import CustomUser,Courses,Subjects,Staffs,Students,SessionYear,FeedBackStudent,FeedBackStaff,LeaveReportStudent,LeaveReportStaff,Attendance,AttendanceReport
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)

    context = {
        "student_count":student_count1,
        "staff_count":staff_count,
        "subject_count":subject_count,
        "course_count":course_count,
        "course_name_list":course_name_list,
        "subject_count_list":subject_count_list,
        "student_count_list_in_course":student_count_list_in_course,
        "student_count_list_in_subject":student_count_list_in_subject,
        "subject_list":subject_list,
        "staff_name_list":staff_name_list,
        "attendance_present_list_staff":attendance_present_list_staff,
        "attendance_absent_list_staff":attendance_absent_list_staff,
        "student_name_list":student_name_list,
        "attendance_present_list_student":attendance_present_list_student,
        "attendance_absent_list_student":attendance_absent_list_student
    }
    return render(request,"hod_template/home_content.html",context)

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        firstname = request.POST.get("FirstName")
        lastname = request.POST.get("LastName")
        user_name = request.POST.get("UserName")
        email = request.POST.get("Email")
        password = request.POST.get("Password")
        address = request.POST.get("Address")
        try:
            user = CustomUser.objects.create_user(username=user_name,password=password,email=email,last_name=lastname,first_name=firstname,user_type='2')
            user.staffs.address = address
            user.save()
            messages.success(request,"Successfully added a new staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except Exception as e:
            #mess = str(e)
            messages.error(request,"Failed to add a new staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request,"hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        coursename = request.POST.get("CourseName")
        try:
            course_model = Courses(course_name=coursename)
            course_model.save()
            messages.success(request,"Successfully added a new course")
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as e:
            #mess = str(e)
            messages.error(request,"Failed to add a new course")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    data = AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{'form':data})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data["FirstName"]
            lastname = form.cleaned_data["LastName"]
            user_name = form.cleaned_data["UserName"]
            email = form.cleaned_data["Email"]
            password = form.cleaned_data["Password"]
            address = form.cleaned_data["Address"]
            gender = form.cleaned_data["Gender"]
            session_id = form.cleaned_data["SessionYear"]
            course = form.cleaned_data["Course"]

            if request.FILES.get('ProfilePicture'):
                profile_pic = request.FILES.get('ProfilePicture')
                file_object = FileSystemStorage()
                filename = file_object.save(profile_pic.name,profile_pic)
                profile_pic_url = file_object.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.create_user(username=user_name,password=password,email=email,last_name=lastname,first_name=firstname,user_type='3')
                user.students.address = address
                user.students.gender = gender

                user_session_obj = SessionYear.objects.get(id=session_id)
                user.students.session_year_id = user_session_obj

                course_stud_obj = Courses.objects.get(id=course)
                user.students.course_id = course_stud_obj

                if profile_pic_url:
                    user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request,"Successfully added a new student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                mess = str(e)
                messages.error(request,"Failed to add a new student-{}".format(mess))
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request,'hod_template/add_student_template.html',{'form':form})

    
def add_subject(request):
    data = Courses.objects.values('id','course_name')
    data1 = CustomUser.objects.filter(user_type='2')
    return render(request,"hod_template/add_subject_template.html",{'courses':data,'staffs':data1})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        subjectname = request.POST.get("SubjectName")
        course = request.POST.get("Course")
        staff = request.POST.get("Staff")
        try:
            course_sub_obj = Courses.objects.get(id=course)
            staff_sub_obj = CustomUser.objects.get(id=staff)
            subject = Subjects(subject_name=subjectname,course_id=course_sub_obj,staff_id=staff_sub_obj)
            subject.save()
            messages.success(request,"Successfully added a new subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except Exception as e:
            #mess = str(e)
            messages.error(request,"Failed to add a new subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    data = Staffs.objects.all()
    return render(request,'hod_template/manage_staff_template.html',{'staffs':data})

def manage_student(request):
    data = Students.objects.all()
    return render(request,'hod_template/manage_student_template.html',{'students':data})

def manage_course(request):
    data = Courses.objects.all()
    return render(request,'hod_template/manage_course_template.html',{'courses':data})

def manage_subject(request):
    data = Subjects.objects.all()
    return render(request,'hod_template/manage_subject_template.html',{'subjects':data})

def edit_staff(request,staff_id):
    data = Staffs.objects.get(admin=staff_id)
    return render(request,'hod_template/edit_staff_template.html',{'staff':data,'id':staff_id})

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        staff_id = request.POST.get("StaffID")
        firstname = request.POST.get("FirstName")
        lastname = request.POST.get("LastName")
        user_name = request.POST.get("UserName")
        email = request.POST.get("Email")
        address = request.POST.get("Address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.username = user_name
            user.save()

            staff_edit_model = Staffs.objects.get(admin=staff_id)
            staff_edit_model.address = address
            staff_edit_model.save()

            messages.success(request,"Successfully updated the staff details")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={'staff_id':staff_id}))
        except Exception as e:
            #mess = str(e)
            messages.error(request,"Failed to update the staff details")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={'staff_id':staff_id}))

def edit_student(request,student_id):
    request.session['StudentID'] = student_id
    data = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['Email'].initial = data.admin.email
    form.fields['ProfilePicture'].initial = data.profile_pic
    form.fields['FirstName'].initial = data.admin.first_name
    form.fields['LastName'].initial = data.admin.last_name
    form.fields['UserName'].initial = data.admin.username
    print(len(data.admin.username))
    form.fields['Address'].initial = data.address
    return render(request,'hod_template/edit_student_template.html',{'form':form,'id':student_id,'username':data.admin.username})

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        student_id = request.session.get("StudentID")
        if student_id == None:
            return HttpResponseRedirect(reverse('manage_student'))

        form = EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data["FirstName"]
            lastname = form.cleaned_data["LastName"]
            user_name = form.cleaned_data["UserName"]
            print("Size:",len(user_name))
            email = form.cleaned_data["Email"]
            address = form.cleaned_data["Address"]

            if request.FILES.get('ProfilePicture'):
                profile_pic = request.FILES.get('ProfilePicture')
                file_object = FileSystemStorage()
                filename = file_object.save(profile_pic.name,profile_pic)
                profile_pic_url = file_object.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.username = user_name
                user.save()

                student_edit_model = Students.objects.get(admin=student_id)
                student_edit_model.address = address
                if profile_pic_url:
                    student_edit_model.profile_pic = profile_pic_url
                student_edit_model.save()

                del request.session['StudentID']

                messages.success(request,"Successfully updated the student details")
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id':student_id}))

            except Exception as e:
                mess = str(e)
                messages.error(request,"Failed to update the student details-{}".format(mess))
                return HttpResponseRedirect(reverse("edit_student", kwargs={'student_id':student_id}))
        
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request,'hod_template/edit_student_template.html',{'form':form,'id':student_id,'username':student.admin.username})

def edit_course(request,course_id):
    data = Courses.objects.get(id=course_id)
    return render(request,'hod_template/edit_course_template.html',{'course':data,'id':course_id})

def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        course_name = request.POST.get("CourseName")
        course_id = request.POST.get("CourseID")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request,"Successfully updated the course details")
            return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))
        
        except Exception as e:
            mess = str(e)
            messages.error(request,"Failed to update the course details due to {}".format(mess))
            return HttpResponseRedirect(reverse("edit_course", kwargs={'course_id':course_id}))

def edit_subject(request,subject_id):
    data = Subjects.objects.get(id=subject_id)
    data1 = Courses.objects.values('id','course_name')
    data2 = CustomUser.objects.filter(user_type='2')
    return render(request,'hod_template/edit_subject_template.html',{'subject':data,'courses':data1,'staffs':data2,'id':subject_id})

def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")

    else:
        subject_id = request.POST.get("SubjectID")
        subject_name = request.POST.get("SubjectName")
        course_id = request.POST.get("SubjectID")
        course = request.POST.get("Course")
        staff = request.POST.get("Staff")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course_sub_obj = Courses.objects.get(id=course)
            staff_sub_obj = CustomUser.objects.get(id=staff)
            subject.course_id = course_sub_obj
            subject.staff_id = staff_sub_obj

            subject.save()
            messages.success(request,"Successfully updated the subject details")
            return HttpResponseRedirect(reverse('edit_subject', kwargs={'subject_id':subject_id}))
        
        except Exception as e:
            mess = str(e)
            messages.error(request,"Failed to update the subject details due to {}".format(mess))
            return HttpResponseRedirect(reverse('edit_subject', kwargs={'subject_id':subject_id}))

def add_session(request):
    return render(request,'hod_template/add_session_template.html')

def add_session_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        session_start = request.POST.get("SessionStart")
        session_end = request.POST.get("SessionEnd")
        try:
            sessions = SessionYear(session_start_year=session_start,session_end_year=session_end)
            sessions.save()
            messages.success(request,"Successfully added a new programme year")
            return HttpResponseRedirect(reverse("add_session"))
        except Exception as e:
            #mess = str(e)
            messages.error(request,"Failed to add a new programme year")
            return HttpResponseRedirect(reverse("add_session"))
        
def view_session(request):
    data = SessionYear.objects.all()
    return render(request,'hod_template/view_session_template.html',{'sessions':data})

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    data=FeedBackStaff.objects.all()
    for i in data:
        print("the reply message:",i.feedback_reply)
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":data})

def student_feedback_message(request):
    data=FeedBackStudent.objects.all()
    for i in data:
        print("the reply message:",i.feedback_reply)
    return render(request,"hod_template/student_feedback_template.html",{"feedbacks":data})

@csrf_exempt
def student_feedback_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_message(request):
    data = LeaveReportStaff.objects.all()
    return render(request,'hod_template/staff_leave_template.html',{'leave':data})

def student_leave_message(request):
    data = LeaveReportStudent.objects.all()
    return render(request,'hod_template/student_leave_template.html',{'leave':data})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_message"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_message"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_message"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_message"))

def profile_admin(request):
    return render(request,'hod_template/profile_admin.html')

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("profile_admin"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("profile_admin"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("profile_admin"))