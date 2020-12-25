from django.contrib import admin
from django.urls import path, include
from home.views import home, features, signup, signin, signinwithparam, logout, getenroll, newstudent, getdata, removestudent, changestudent, getfacultyenroll, newfaculty, getfacultydata, removefaculty, changefaculty, getclerkdata, changeclerkdata, changedashboarddata, getallfaculty, getallstudent, insertfacattendance, insertstuattendance, settotalfees, getallstudent2, insertstufees, submitdeclarationtoall, getglobaldeclaration, changeadminpwd, removedeclaration, about

urlpatterns = [
    path('', home),
    path('features/', features),
    path('signup/', signup),
    path('signin/', signin),
    path('signin/<passparam>', signinwithparam),
    path('admin/', admin.site.urls),
    path('logout/', logout),
    path('getenroll/', getenroll),
    path('newstudent/', newstudent),
    path('getdata/', getdata),
    path('removestudent/', removestudent),
    path('changestudent/', changestudent),
    path('getfacultyenroll/', getfacultyenroll),
    path('newfaculty/', newfaculty),
    path('getfacultydata/', getfacultydata),
    path('removefaculty/', removefaculty),
    path('changefaculty/', changefaculty),
    path('getclerkdata/', getclerkdata),
    path('changeclerkdata/', changeclerkdata),
    path('changedashboarddata/', changedashboarddata),
    path('getallfaculty/', getallfaculty),
    path('getallstudent/', getallstudent),
    path('insertfacattendance/', insertfacattendance),
    path('insertstuattendance/', insertstuattendance),
    path('settotalfees/', settotalfees),
    path('getallstudent2/', getallstudent2),
    path('insertstufees/', insertstufees),
    path('submitdeclarationtoall/', submitdeclarationtoall),
    path('getglobaldeclaration/', getglobaldeclaration),
    path('changeadminpwd/', changeadminpwd),
    path('remove/delete/remove<passparam>', removedeclaration),
    path('about/', about),
]