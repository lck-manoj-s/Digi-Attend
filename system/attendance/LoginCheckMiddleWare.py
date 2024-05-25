from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):

        modulename = view_func.__module__
        user = request.user

        unauthenticated_paths = [
            reverse('ShowLogin'), 
            reverse('doLogin'), 
            reverse('password_reset'),
            reverse('password_reset_done'),
            reverse('password_reset_confirm', kwargs={'uidb64': 'uidb64', 'token': 'token'}),
            reverse('password_reset_complete')
        ]

        if user.is_authenticated:
            print("User:",user,"Module Name:",modulename)
            if user.user_type == '1':
                if modulename == "attendance.hodviews" or modulename == "attendance.views" or modulename == 'django.views.static' or modulename == 'django.contrib.auth.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('admin_home'))
            
            elif user.user_type == '2':
                if modulename == "attendance.staffviews" or modulename == "attendance.views" or modulename == 'django.views.static' or modulename == 'django.contrib.auth.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('staff_home'))

            elif user.user_type == '3':
                if modulename == "attendance.studentviews" or modulename == "attendance.views" or modulename == 'django.views.static' or modulename == 'django.contrib.auth.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('student_home'))
            
            else:
                if request.path in unauthenticated_paths:
                    pass
                else:
                    return HttpResponseRedirect(reverse('ShowLogin'))
        else:
            if request.path == reverse('ShowLogin') or request.path == reverse('doLogin'):
                pass
            else:
                return HttpResponseRedirect(reverse('ShowLogin'))