from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Courses,Subjects,SessionYear,Students,Attendance,AttendanceReport,LeaveReportStudent,Staffs,FeedBackStudent,CustomUser
from  django.urls import reverse
import datetime
import json

def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    subjects_data = Subjects.objects.filter(course_id=course)
    session_obj = SessionYear.objects.get(id=student_obj.session_year_id.id)

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    context = {
        "total_attendance": attendance_total,
        "attendance_absent": attendance_absent,
        "attendance_present": attendance_present,
        "subjects": subjects,
        "data_name": subject_name,
        "data1": data_present,
        "data2": data_absent
    }

    return render(request, "student_template/student_home_template.html", context)
def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    data=Subjects.objects.filter(course_id=student.course_id)
    return render(request,'student_template/student_view_attendance.html',{'subjects':data})

def student_view_attendance_post(request):
    if request.method != "POST":
        return HttpResponse("<h2> POST Method required to process the data </h2>")
    else:
        subject_id=request.POST.get("subject")
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        print(subject_id,start_date,end_date)
        start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
        end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        subject_obj=Subjects.objects.get(id=subject_id)
        user_object=CustomUser.objects.get(id=request.user.id)
        stud_obj=Students.objects.get(admin=user_object)

        attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
        attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
        return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    student_id = Students.objects.get(admin=request.user.id)
    data = LeaveReportStudent.objects.filter(student_id=student_id)
    print(data)
    return render(request,'student_template/student_apply_leave.html',{'leave':data})

def student_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("LeaveDate")
        leave_reason = request.POST.get("LeaveReason")
        student_id = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_id,leave_date=leave_date,leave_message=leave_reason,leave_status=0)
            leave_report.save()
            messages.success(request,"Your leave application has been submitted")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except Exception as e:
            messages.error(request,"Failed to save the leave report")
            return HttpResponseRedirect(reverse("student_apply_leave"))

def student_feedback(request):
    student_id = Students.objects.get(admin=request.user.id)
    data = FeedBackStudent.objects.filter(student_id=student_id)
    return render(request,'student_template/student_feedback.html',{'feedback':data})

def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback = request.POST.get("FeedbackMessage")
        student_id = Students.objects.get(admin=request.user.id)
        print("SID:",student_id)
        try:
            student_feedback = FeedBackStudent(student_id=student_id,feedback=feedback,feedback_reply="")
            student_feedback.save()
            messages.success(request,"Your feedback has been recorded")
            return HttpResponseRedirect(reverse("student_feedback"))
        except Exception as e:
            mess = str(e)
            messages.error(request,"Failed to save your feedback, {}".format(mess))
            return HttpResponseRedirect(reverse("student_feedback"))

def profile_student(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/profile_student.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("profile_student"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.save()

            student=Students.objects.get(admin=customuser)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("profile_student"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("profile_student"))