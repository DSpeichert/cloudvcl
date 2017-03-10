from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import User
from .models import UserGroup
from .models import Assignment


##from django.views.generic import

# Create your views here.

def index(request):
    return render(request, 'index.html')


##class testView(View): #testing a class based view
##    def get(self, request, *args, **kwargs):
##      return HttpResponse("Hello Again")




# UserListView Class Test to display Users that are currently stored in the table
class UserList(ListView):
    # specify model User
    model = User
    # name used for the list to be used as a template variable
    context_object_name = 'my_user_list'
    # queryset = User.objects.all()
    # Just testing to see if I can display the userlist onto an html page
    # template_name = 'templates/userlist.html'

    """Displays list of all users of the system (Name, Drexel ID, User Type, Ban, Delete)
2. Under user type for each user, there will be three checkboxes indicating which permissions they have (user, instructor, admin)
3. Can select the instructor or admin checkbox for a regular user to promote them (add submit button/function somewhere to confirm changes)
4. There will be two additional checkboxes. Selecting 'Ban' will ban the user from VCL and selecting 'Delete' will delete that user (after the admin submits the changes)
5. Add button/function that will take admin to another view of only instructors (/users/quota) """


# UserGroup Class Test to display Users that are currently stored in the table
class UserGroup(ListView):
    # specify model Usergroup
    model = UserGroup
    # name used for the list to be used as a template variable
    context_object_name = 'my_usergroup_list'


class InstructorList(ListView):
    model = User
    ##context_object_name = 'check_instructor_list'
    queryset = User.objects.filter(is_instructor=True)
    context_object_name = 'check_instructor_list'


# Allow to see user by a name ex: /user/say34
#

# /users/quota
# List all instructors and corresponding fields for # of instances,Cpu, ram
# Add submit function/button
class UserQuota(ListView):
    model = User;
    message = "TODO"
    context_object_name = 'instructor_list'

    def get(self, request):
        return HttpResponse(self.message)


# /assignments/edit
#



# /assignments/add
# form witll prompt user to add name,description,start date, and end date for new assignment
# Include submit button
# create assignment for class(Form will be involved)
class assignmentManage(ListView):
    model = Assignment;
    messgage = "TODO"
    context_object_name = 'assignments_add'

    def get(self, request):
        return HttpResponse(self.message)


# /assignments/launch
# Display button to launch an environmewnt for an assignment

# /assignmentss/launch/environment
# Display virtual environment
# include reboot function/button not needed for demo
# User can switch VMs
#
class assignmentLaunch(ListView):
    model = Assignment;
    message = "TODO"
    context_object_name = 'assignment_launch'

    def get(self, request):
        return HttpResponse(self.message)

# /login

# /logout
