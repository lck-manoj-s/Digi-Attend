from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse 
from django.contrib import messages
from .models import Subjects,SessionYear,Students,Attendance,AttendanceReport,LeaveReportStaff,Staffs,FeedBackStaff,CustomUser,Courses
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse
import json


def staff_home(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context = {
        "course_id_list": course_id_list,
        "final_course": final_course,
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count":subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list":student_list,
        "student_list_attendance_present":student_list_attendance_present,
        "student_list_attendance_absent":student_list_attendance_absent
    }
    print(student_list,student_list_attendance_present,student_list_attendance_absent)
    return render(request,'staff_template/staff_home_template.html',context)

def staff_take_attendance(request):
    data = Subjects.objects.filter(staff_id=request.user.id)
    data1 = SessionYear.objects.all()
    return render(request,'staff_template/staff_take_attendance.html',{'subjects':data,'sessions':data1})

@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('Subject')
    session_id = request.POST.get('Session')

    subject = Subjects.objects.get(id=subject_id)
    session = SessionYear.objects.get(id=session_id)
    students = Students.objects.filter(course_id=subject.course_id,session_year_id=session)

    students_data = serializers.serialize("python",students)
    data_list = []
    for student in students:
        temp = {'id':student.admin.id,'name':student.admin.first_name+" "+student.admin.last_name}
        data_list.append(temp)
    print(data_list)
    return JsonResponse(json.dumps(data_list),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_data = request.POST.get('Student')
    subject_id = request.POST.get('Subject')
    session_id = request.POST.get('Session')
    attendance_data = request.POST.get('Attendance')

    data = json.loads(student_data)
    subject = Subjects.objects.get(id=subject_id) 
    session = SessionYear.objects.get(id=session_id)
    try:
        attendance = Attendance(subject_id=subject,attendance_date=attendance_data,session_year_id=session)
        attendance.save()

        for stud in data:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
            attendance_report.save()
            
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def staff_update_attendance(request):
    data = Subjects.objects.filter(staff_id=request.user.id)
    data1 = SessionYear.objects.all()
    return render(request,'staff_template/staff_update_attendance.html',{'subjects':data,'sessions':data1})

@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("Subject")
    session = request.POST.get("Session")
    subject_id = Subjects.objects.get(id=subject)
    session_id = SessionYear.objects.get(id=session)
    attendance = Attendance.objects.filter(subject_id=subject_id,session_year_id=session_id)
    attendance_obj = []
    for att in attendance:
        data = {'id':att.id,'attendance_date':str(att.attendance_date),'session_year_id':att.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj),content_type="application/json",safe=False)

@csrf_exempt
def get_attendance_students(request):
    attendance_id = request.POST.get('Attendance')
    attendance = Attendance.objects.get(id=attendance_id)
    attendance_report = AttendanceReport.objects.filter(attendance_id=attendance)

    data_list = []
    for att in attendance_report:
        temp = {'id':att.student_id.admin.id,'name':att.student_id.admin.first_name+" "+att.student_id.admin.last_name,'status':att.status}
        data_list.append(temp)
    print(data_list)
    return JsonResponse(json.dumps(data_list),content_type="application/json",safe=False)

@csrf_exempt
def update_attendance_data(request):
    student_data = request.POST.get('Student')
    attendance_id = request.POST.get('Attendance')
    print("Attendance Date",attendance_id)
    attendance = Attendance.objects.get(id=attendance_id)

    data = json.loads(student_data)
    try:

        for stud in data:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
            
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

def staff_apply_leave(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    data = LeaveReportStaff.objects.filter(staff_id=staff_id)
    print(data)
    return render(request,'staff_template/staff_apply_leave.html',{'leave':data})

def staff_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("LeaveDate")
        leave_reason = request.POST.get("LeaveReason")
        staff_id = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_id,leave_date=leave_date,leave_message=leave_reason,leave_status=0)
            leave_report.save()
            messages.success(request,"Your leave application has been submitted")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except Exception as e:
            messages.error(request,"Failed to save the leave report")
            return HttpResponseRedirect(reverse("staff_apply_leave"))

def staff_feedback(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    data = FeedBackStaff.objects.filter(staff_id=staff_id)
    return render(request,'staff_template/staff_feedback.html',{'feedback':data})

def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback = request.POST.get("FeedbackMessage")
        staff_id = Staffs.objects.get(admin=request.user.id)
        try:
            staff_feedback = FeedBackStaff(staff_id=staff_id,feedback=feedback,feedback_reply="")
            staff_feedback.save()
            messages.success(request,"Your feedback has been recorded")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except Exception as e:
            messages.error(request,"Failed to save your feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def profile_staff(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/profile_staff.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("profile_staff"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("profile_staff"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("profile_staff"))