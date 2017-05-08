# **Administrator Documentation**

## *Setup*

Welcome to the Cloud VCL Administrator guide. This guide will help you
utilize the features of Cloud VCL and manage users and functions. The
first step will be to install Django and Python. You will want to refer to official
 django documentation to [Deploy Django](https://docs.djangoproject.com/en/1.11/howto/deployment/).
Follow the getting-started documentation pertaining to your specific configuration. 
Once you have setting up Django and the WGGI server, you will want to install several other packages.


These packages include:
1. OpenStack SDK
2. Django Bootstrap 3
3. Pyyaml
4. Python NovaClient
5. Passlib6. Django Bootstrap 3 Datepicker 2

_Note: Ensure that you have installed the latest versions of these packages along with the lastest version of Django and Python._

### *Superuser*
To be able to administer the site and login to the admin panel, you must first create a superuser account.
In order to do this go back to the command line and type
```
python manage.py createsuperuser`
```
Press enter, and when prompted, type your username (lowercase, no spaces), email address, and password.
Don't worry that you can't see the password you're typing in – that's how it's supposed to be. Just type
it in and press enter to continue. The output should look like this (where the username and email should
be your own ones):
```
(myvenv) ~/django$ python manage.py createsuperuser
Username: admin
Email address: admin@admin.com
Password:
Password (again):
Superuser created successfully.
```
Return to your browser. Log in with the superuser's credentials you chose; you should see the Django admin
dashboard.

## *The Django admin site*

One of the most powerful parts of Django is the automatic admin interface. If you want to know more about
Django admin, you should check [Django's Admin documentation](https://docs.djangoproject.com/en/1.10/ref/contrib/admin/).
 Once you have logged into the Django Admin panel, you will be able to begin site administration.
 Here you can view recent actions that have been performed on the right center of the screen. You can also
 drill down by subject area to perform actions. Note that each subject area has the option of `Add` or `Edit` that serves
 as a quicklink to the action.
 
 ###*Assignment Administration*
 Select the second subject area by clicking on `Assignments`.
 This will bring you to a new page where you be prompted to select an assignment to change. If there is no pre-existing
 assignments, you can add one via the `Add Assignment` button in the top right corner of the screen. This will open up a
 form that will require you to enter the Name, Description, Start Date/Time, End Date/Time, Course and Environment
 Definition. Make sure you have filled out every field of the form before continuing. If you have completed adding
 assignments, hit the `SAVE` button. If you wish to save your current input and return to the form, hit `Save and continue editing`
 Lastly, if you have more assignments to add, hit `Save and add another`. If you do not want to save and wish to return back
 to the main Assignments admin page, scroll up till the top of the screen and locate the site path in the top left corner.
 This shows you, your current location within the admin panel and will look similar to this:
 ```
 Home>Cvcl>Assignments>Add Assignment
 ```
 If you have no changes to submit, navigate back to the main Assignments admin page, by clicking `Assignments`. If you have
 changes, saving will return you back to the Assignments admin page.
 
 _Filtering Assignments_
 
 You may filter Assignments by course or environment definition in the right center of the screen.
 This will help you quickly access a particular course or environment definition.
 
 _Deleting an Assignment_
 
 Deleting an assignment is done by selecting the checkbox next the Assignment to be deleted. You have the option to
 delete multiple assignments or a single assignment by way of checkbox. Typically, this will be in the table and to
 the left of the `Assignment Name` column. Once selected, navigate to the action dropdown located above the Assignments
 table. Select the dropdown button and hit `Delete selected assignments`. Lastly, click the `Go` button to the right of the dropdown.
 This will bring up a confirmation page which will ask to confirm the content you are deleting. If you wish to delete
 the identified assignment, hit the red `Yes,I'm sure` button. If you changed your mind and wish to keep the assignment,
 click the grey `No, take me back` button.

_Editing an Assignment_

To edit an Assignment, navigate to where it is listed in the Assignments table. You may wish to use the filters for quick
access. Click the blue hyperlink for the Course or Environment Definition to edit the form that generated the assignment.
Upon, completion of editing, save the changes at the bottom of the form. This will update the assignment.

###*Courses Administration*
Select the first subject area by clicking on `Courses`.
 This will bring you to a new page where you be prompted to select an course to change. If there is no pre-existing
 courses, you can add one via the `Add Course` button in the top right corner of the screen. This will open up a
 form that will require you to enter the Name, Instructor, and Students. Make sure you have filled out every field of the form before continuing. If you have completed adding
courses, hit the `SAVE` button. If you wish to save your current input and return to the form, hit `Save and continue editing`
 Lastly, if you have more courses to add, hit `Save and add another`. If you do not want to save and wish to return back
 to the main Course admin page, scroll up till the top of the screen and locate the site path in the top left corner.
 This shows you, your current location within the admin panel and will look similar to this:
 ```
 Home>Cvcl>Courses>Add Course
 ```
 If you have no changes to submit, navigate back to the main Courses admin page, by clicking `Courses`. If you have
 changes, saving will return you back to the Courses admin page.
 
 _Filtering Courses_
 
 You may filter Courses by instructor in the right center of the screen.
 This will help you quickly access a particular course.
 
 _Deleting an Assignment_
 
 Deleting a course is done by selecting the checkbox next the Course to be deleted. You have the option to
 delete multiple courses or a single course by way of checkbox. Typically, this will be in the table and to
 the left of the `Name` column. Once selected, navigate to the action dropdown located above the Courses
 table. Select the dropdown button and hit `Delete selected courses`. Lastly, click the `Go` button to the right of the dropdown.
 This will bring up a confirmation page which will ask to confirm the content you are deleting. If you wish to delete
 the identified course, hit the red `Yes,I'm sure` button. If you changed your mind and wish to keep the course,
 click the grey `No, take me back` button.

_Editing an Assignment_

To edit a Course, navigate to where it is listed in the Courses table. You may wish to use the filters for quick
access. Click the blue hyperlink for the Instructor to edit the form that generated the course.
Upon, completion of editing, save the changes at the bottom of the form. This will update the course. The edit course
page also has an option to delete a course. 

###*Environment Definition Administration*
 Select the second subject area by clicking on `Environment Definition`.
 This will bring you to a new page where you be prompted to select an environment definition to change. If there is no pre-existing
 environment definitions , you can add one via the `Add environment definition` button in the top right corner of the screen. This will open up a
 form that will require you to enter the Name, Instructor and VM Definition. Make sure you have filled out every field of the form before continuing. If you have completed adding
 environment definitions, hit the `SAVE` button. If you wish to save your current input and return to the form, hit `Save and continue editing`
 Lastly, if you have more environment definitions to add, hit `Save and add another`. If you do not want to save and wish to return back
 to the main environment definitions admin page, scroll up till the top of the screen and locate the site path in the top left corner.
 This shows you, your current location within the admin panel and will look similar to this:
 ```
 Home>Cvcl>Assignments>Add Environment Definition
 ```
 If you have no changes to submit, navigate back to the main Assignments admin page, by clicking `Environment Definitions`. If you have
 changes, saving will return you back to the Environment definitions admin page.
 
 _Filtering Environment Definition_
 
 You may filter environment definitions by instructor in the right center of the screen.
 This will help you quickly access an environment definition.
 
 _Deleting an Environment Definition_
 
 Deleting an environment definition is done by selecting the checkbox next the Environment Definition to be deleted. You have the option to
 delete multiple environment definitions or a single environment definition by way of checkbox. Typically, this will be in the table and to
 the left of the `Name` column. Once selected, navigate to the action dropdown located above the Environment Definitions
 table. Select the dropdown button and hit `Delete selected environment definition`. Lastly, click the `Go` button to the right of the dropdown.
 This will bring up a confirmation page which will ask to confirm the content you are deleting. If you wish to delete
 the identified environment definition, hit the red `Yes,I'm sure` button. If you changed your mind and wish to keep the environment definition,
 click the grey `No, take me back` button.

_Editing an Environment Definition_

To edit an Environment Definition, navigate to where it is listed in the Environment Definitions table. You may wish to use the filters for quick
access. Click the blue hyperlink for the Course or Environment Definition to edit the form that generated the environment definition.
Upon, completion of editing, save the changes at the bottom of the form. This will update the environment definition.

