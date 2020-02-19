from django.contrib import admin
from home.models import Administrator, Student_detail, Faculty_detail, attendance_faculty, attendance_student, trigger, totalfees, feesrecord, declarationtoall, declarationtosp

# Register your models here.
admin.site.register(Administrator)
admin.site.register(Student_detail)
admin.site.register(Faculty_detail)
admin.site.register(attendance_faculty)
admin.site.register(attendance_student)
admin.site.register(trigger)
admin.site.register(totalfees)
admin.site.register(feesrecord)
admin.site.register(declarationtoall)
admin.site.register(declarationtosp)
