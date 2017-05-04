# Instructor Documentation 

##Create a Course
1. From the home page, select the `Courses` tab found in the header. You'll be taken to the Course List page which will contain all of the instructor's courses.
2. While on this page, click the `Create Course` button near the top right corner.
3. Provide a name for the course and select the students you want to add to the course (see step 5 if a student doesn't exist in the database).
4. After pressing submit, you'll be taken to the specific course page where you can view assignments and students in that particular course.
5. If a student doesn't exist in the database, click the `Add Students (CSV Upload)` button near the right side.
6. Click over `Browse for CSV` where you'll be prompted to upload a file. Ensure that the file uploaded includes the fields: *Last Name, First Name, Username*. Once the file is selected, press `Upload CSV and Add Students`.

## Update a Course
1. Go to the Course List page (click the `Courses` tab found in the header).
2. Find the course you want to update and select `Edit` in order to rename the course or add more students.

## Delete a Course
*All corresponding students and assignments will be deleted when you delete a course.*

1. Go to the Course List page by selecting the `Courses` tab found in the header.
2. Find the course you want to delete and click on `Delete`.

## Create an Environment Definition
1. From the home page, select the `Environment Definitions` tab found in the header. You'll be taken to the Environment Definitions List page which will contain all of the instructor's environment definitions.
2. While on this page, click the `Create Environment Definition` button near the top right corner.
3. Provide a name for the environment definition.
4. Please see *Create a VM Definition* to know how to create a VM Definition within your environment definitions.

## Update an Environment Definition
1. Go to the Environment Definition List page (click the `Environment Definitions` tab found in the header).
2. Find the environment definition you want to update and select `Edit` in order to rename it.

## Delete an Environment Definition
*All corresponding VM definitions will be deleted when you delete an environment definition.*

1. Go to the Environment Definition List page by selecting the `Environment Definitions` tab found in the header.
2. Find the environment definition you want to delete and click on `Delete`.

## Create a VM Definition
1. Go to the Environment Definitions List page by selecting the `Environment Definitions` tab found in the header.
2. Click the environment definition you want to create VM definitions in.
3. Select the `Create VM Definition` button towards the top right.
4. Provide the name of the VM definition.
5. Choose the type of image (*CentOS 7.3, Ubuntu Server 16.04.2, Windows Server 2012 R2*).
6. Select the type of flavor (*01c-01m-10d reads 1 VCPU, 1 RAM GB, and 10 GB Total/Root Disk*).
7. The timezone, hostname and Powershell script fields do not need to be complete in order to successfully create a VM definition. Please see *Cloud Configurations* to learn more about VM customizations.
8. Press `Submit` when you have the necessary fields completed.

## Update a VM Definition
1. Go to the Environment Definitions List page by selecting the `Environment Definitions` tab found in the header.
2. Choose the environment definition that has the VM definition you want to update.
3. Find the VM definition and press the `Edit` button to modify any of the existing fields.

## Delete a VM Definition
1. Go to the Environment Definitions List page by selecting the `Environment Definitions` tab found in the header.
2. Choose the environment definition that has the VM definition you want to delete.
3. Find the VM definition and press the `Delete` button to delete it.

## Create an Assignment
1. From the home page, select the `Assignment` tab found in the header. You'll be taken to the Assignment List page which will contain all assignments created.
2. While on this page, click the `Create Assignment` button near the top right corner.
3. Provide a name, description, start and end date for the assignment, as well as choosing which course to add the assignment to along with the environment definition.
4. After pressing `Submit`, you can spawn a fresh instance by selecting `Selecting a New Environment for this Assignment`.

## Update an Assignment
1. Go to the Assignment List page by clicking the `Assignments` tab found in the header.
2. Find the assignment you want to update and select `Edit` in order to modify any of the existing fields.

## Delete an Assignment
1. Go to the Assignment List page by selecting the `Assignment` tab found in the header.
2. Find the assignment you want to delete and click on `Delete`.

## Timezone (Linux Only)
Set the system timezone for an instance.
Example:
```
American/New_York
```

## Hostname (Linux Only)
Set the system hostname to be different than default value.

## Powershell Script (Windows Only)
Run a Powershell script once when the instance is created.
