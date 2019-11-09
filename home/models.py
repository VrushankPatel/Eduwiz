from django.db import models

# Create your models here.

class Administrator(models.Model):
    admin_name = models.CharField(max_length=101)
    admin_dob = models.CharField(max_length=10)
    admin_gender = models.CharField(max_length=8)
    admin_mobile = models.PositiveIntegerField()
    admin_email = models.CharField(max_length=100)
    admin_pwd = models.TextField()
    school_name = models.TextField()
    school_address = models.TextField()
    school_mobile = models.PositiveIntegerField()
    clerk_name = models.CharField(max_length=100)
    clerk_id = models.TextField()
    clerk_pwd = models.TextField()
    dashboard_id = models.TextField()
    dashboard_pwd = models.TextField()

    def __str__(self):
        return str(str(self.id)+" "+self.admin_name)


class Student_detail(models.Model):
    school_id = models.PositiveIntegerField()
    std = models.PositiveIntegerField()
    Enroll = models.PositiveIntegerField()
    name = models.CharField(max_length=75)
    father_name = models.CharField(max_length=75)
    father_occupation = models.CharField(max_length=50)
    dob = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return str(str(self.school_id)+" "+self.name)


class Faculty_detail(models.Model):
    school_id = models.PositiveIntegerField()
    Enroll = models.PositiveIntegerField()
    name = models.CharField(max_length=75)
    dob = models.CharField(max_length=10)
    subject = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return str(str(self.school_id)+" "+self.name)


class attendance_student(models.Model):
    school_id = models.PositiveIntegerField()
    date = models.CharField(max_length=10)
    std = models.PositiveIntegerField()
    Enroll = models.PositiveIntegerField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return "School id = "+str(self.school_id) + ", Enroll = "+str(self.Enroll) + ", onDate = "+self.date + ", Attendance = "+str(self.present)


class attendance_faculty(models.Model):
    school_id = models.PositiveIntegerField()
    date = models.CharField(max_length=10)
    Enroll = models.PositiveIntegerField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return "School id = "+str(self.school_id) + ", Enroll = "+str(self.Enroll) + ", onDate = "+self.date + ", Attendance = "+str(self.present)


class feesrecord(models.Model):
    school_id = models.PositiveIntegerField()
    std = models.PositiveIntegerField()
    Enroll = models.PositiveIntegerField()
    paidfees = models.PositiveIntegerField()
    year = models.CharField(max_length=10)
    date = models.CharField(max_length=20)

    def __str__(self):
        return "School id = "+str(self.school_id) + "Std = "+str(self.std) + ", Enroll = "+str(self.Enroll) + ", onDate = "+self.date + ", Paid = "+str(self.paidfees) + " , " + "year = " + str(self.year)


class totalfees(models.Model):
    school_id = models.PositiveIntegerField()
    s1 = models.PositiveIntegerField()
    s2 = models.PositiveIntegerField()
    s3 = models.PositiveIntegerField()
    s4 = models.PositiveIntegerField()
    s5 = models.PositiveIntegerField()
    s6 = models.PositiveIntegerField()
    s7 = models.PositiveIntegerField()
    s8 = models.PositiveIntegerField()
    s9 = models.PositiveIntegerField()
    s10 = models.PositiveIntegerField()
    s11 = models.PositiveIntegerField()
    s12 = models.PositiveIntegerField()


class trigger(models.Model):
    school_id = models.PositiveIntegerField()
    isfeesset = models.BooleanField(default=False)


class declarationtoall(models.Model):
    school_id = models.PositiveIntegerField()
    declared_on = models.CharField(max_length=10)
    event_date = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return "School id = "+str(self.school_id) + "declared on = "+str(self.declared_on) + ", event date = "+str(self.event_date) + ", message = "+self.message


class declarationtosp(models.Model):
    school_id = models.PositiveIntegerField()
    declared_on = models.CharField(max_length=10)
    event_date = models.CharField(max_length=10)
    message = models.TextField()
    people_type = models.CharField(max_length=12)
    Enroll = models.PositiveIntegerField()
    std = models.PositiveIntegerField()
