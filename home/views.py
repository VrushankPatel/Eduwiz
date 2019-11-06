from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect,JsonResponse
from arc4 import ARC4
from django.views.decorators.csrf import csrf_exempt
from home.models import *
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.db.models import Avg, Max, Min, Sum
import random
import hashlib
import json
import smtplib
import requests
from datetime import date,datetime
import threading
# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        #send_mail(self.subject,self.html_content,settings.EMAIL_HOST_USER,self.recipient_list,fail_silently=True) # another way for sms
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()

def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()

class MobileThread(threading.Thread):
    def __init__(self, mobile, sms_content):
        self.mobile = mobile
        self.sms_content = sms_content        
        threading.Thread.__init__(self)

    def run (self):
        send(self.mobile,self.sms_content)

def send_sms(mobile,sms_content):
    MobileThread(mobile,sms_content).start()

def home(request):    
    return render(request, 'home/static/templates/home/index.html')


def features(request):
    return render(request, "home/static/templates/home/features.html")

def signup(request):
    if request.method == "GET":
        # /Signup/signup.html
        return render(request, "home/static/templates/Signup/Signup.html", {"checker": "signup"})
    else:
        if request.POST['checker'] == "signup" and not checkifexists(request.POST['email']) and not checkifexistsmob(request.POST["phone"]):            
            print("debug : ",checkifexistsmob(request.POST["phone"]))
            a1 = random.randrange(100000, 1000000)
            a2 = random.randrange(100000, 1000000)            
            to_list = [request.POST["email"]]            
            subject = "Eduwiz account verification"
            send_html_mail(subject,str("OTP (One time password for your eduwiz account sign up is <br><h1>%s</h1>" % a1),to_list)
            send_sms(str("91"+request.POST["phone"]),str("OTP (One time password for your eduwiz account sign up is %s" % a2))
            a1 = hashlib.md5(("%s" % a1).encode()).hexdigest()
            a2 = hashlib.md5(("%s" % a2).encode()).hexdigest()
            return render(request, "home/static/templates/Signup/verify.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthday"], "gender": request.POST["gender"], "email": request.POST["email"], "mobile": request.POST["phone"], "privatedata1": a1, "privatedata2": a2, "checker": "verify", "raiseerror": "", "OTP1": "False", "OTP2": "True", "msg": "Enter OTP sended to your email", "msg2": "Enter OTP sended to your mobile", "msgcolor": "blue"})          
        elif request.POST['checker'] == "verify" and not checkifexists(request.POST['email']):
            if request.POST["privatedata1"] == hashlib.md5(("%s" % request.POST["OTPemail"]).encode()).hexdigest() and request.POST["privatedata2"] == hashlib.md5(("%s" % request.POST["OTPmobile"]).encode()).hexdigest():
                return render(request, "home/static/templates/Signup/password.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthday"], "gender": request.POST["gender"], "email": request.POST["email"], "mobile": request.POST["phone"], "checker": "password"})
            else:
                return render(request, "home/static/templates/Signup/verify.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthday"], "gender": request.POST["gender"], "email": request.POST["email"], "mobile": request.POST["phone"], "privatedata1": request.POST["privatedata1"], "privatedata2": request.POST["privatedata2"], "checker": "verify", "OTP1": not (request.POST["privatedata1"] == hashlib.md5(("%s" % request.POST["OTPemail"]).encode()).hexdigest()), "OTP2": not (request.POST["privatedata2"] == hashlib.md5(("%s" % request.POST["OTPmobile"]).encode()).hexdigest()), "firstotp": request.POST["OTPemail"], "secondotp": request.POST["OTPmobile"], "msg": "Invalid OTP", "msg2": "Invalid OTP", "msgcolor": "red"})
        elif request.POST['checker'] == "password" and not checkifexists(request.POST['email']):
            return render(request, "home/static/templates/Signup/Schooldetails.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthday"], "gender": request.POST["gender"], "email": request.POST["email"], "mobile": request.POST["phone"], "adminmobile": request.POST["phone"], "checker": "schooldetails", "privatedata1" : rc4(request.POST["pwd"], request.POST["email"]) })
        elif request.POST['checker'] == "resend" and not checkifexists(request.POST['email']):
            a1 = random.randrange(100000, 1000000)
            a2 = random.randrange(100000, 1000000)            
            to_list = [request.POST["email"]]            
            subject = "Eduwiz account verification"
            send_html_mail(subject,str("OTP (One time password for your eduwiz account sign up is <br><h1>%s</h1>" % a1),to_list)
            send_sms(str("91"+request.POST["phone"]),str("OTP (One time password for your eduwiz account sign up is %s" % a2))
            a1 = hashlib.md5(("%s" % a1).encode()).hexdigest()
            a2 = hashlib.md5(("%s" % a2).encode()).hexdigest()
            return render(request, "home/static/templates/Signup/verify.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthday"], "gender": request.POST["gender"], "email": request.POST["email"], "mobile": request.POST["phone"], "privatedata1": a1, "privatedata2": a2, "checker": "verify", "raiseerror": "", "OTP1": "False", "OTP2": "True", "msg": "Enter OTP sended to your email", "msg2": "Enter OTP sended to your mobile", "msgcolor": "blue"})
        elif request.POST['checker'] == "schooldetails" and not checkifexists(request.POST['email']):
            return render(request, "home/static/templates/Signup/createacc.html", {"firstname": request.POST["first_name"], "lastname": request.POST["last_name"], "dob": request.POST["birthdate"], "gender": request.POST["gender"], "email": request.POST["email"], "adminmobile": request.POST["adminmobile"] , "schoolname": request.POST["schoolname"], "schooladdress": request.POST["schooladdress"], "schoolmobile": request.POST["schoolmobile"], "privatedata1": request.POST["privatedata1"], "checker": "createacc"})
        elif request.POST['checker'] == "createacc" and not checkifexists(request.POST['email']):
            data = {"admin_name":str(request.POST["first_name"] + " " + request.POST["last_name"]),"admin_dob":str(request.POST["birthdate"]),"admin_gender":str(request.POST["gender"]),"admin_email":str(request.POST["email"]),"admin_mobile":int(request.POST["adminmobile"]),"admin_pwd":str(request.POST["privatedata1"]),"school_name":str(request.POST["schoolname"]),"school_address":str(request.POST["schooladdress"]),"school_mobile":int(request.POST["schoolmobile"]),"clerk_name":str(request.POST["clerkname"]),"clerk_id":str(request.POST["clerkid"]),"clerk_pwd":str(rc4(request.POST["clerkpwd"],request.POST["clerkid"])),"dashboard_id":str(request.POST["dashboardid"]),"dashboard_pwd":str(rc4(request.POST["dashboardpwd"],request.POST["dashboardid"]))}

            admindata = Administrator(admin_name=data["admin_name"], admin_dob=data["admin_dob"],admin_gender=data["admin_gender"],admin_mobile=data["admin_mobile"],admin_email=data["admin_email"],admin_pwd=data["admin_pwd"],school_name=data["school_name"],school_address=data["school_address"],school_mobile=data["school_mobile"],clerk_name=data["clerk_name"],clerk_id=data["clerk_id"],clerk_pwd=data["clerk_pwd"],dashboard_id=data["dashboard_id"],dashboard_pwd=data["dashboard_pwd"])

            admindata.save()
            return render(request,"home/static/templates/success.html",{"id":admindata.id})
            # return render(request,"home/static/templates/Signup/temp.html",data)
        elif checkifexists(request.POST['email']):            
            return render(request,"home/static/templates/swal.html",{"msg1":"OOPS...","msg2":"There is already an account with this Email. Please use another email","type":"error"})
        elif checkifexistsmob(request.POST['phone']):            
            return render(request,"home/static/templates/swal.html",{"msg1":"OOPS...","msg2":"There is already an account with this Mobile number. Please use another Mobile","type":"error"})
        else:
            return HttpResponse("Unknown error occured")


def signin(request):
    if request.method == "GET":
        try:
            if request.COOKIES['idloggedin']:        
                return HttpResponseRedirect('/signin/dashboard')            
        except:
            return render(request,"home/static/templates/signin/signin.html")    
    else:
        try:            
            a=Administrator.objects.get(id=request.POST["id"])
            if request.POST["usertype"] == "Administrator":                
                if a.admin_email == request.POST["email"] and a.admin_pwd == str(rc4(request.POST["pwd"], request.POST["email"])):      
                    response = HttpResponseRedirect('/signin/dashboard')
                    response.set_cookie("idloggedin",a.id)                                    
                    response.set_cookie("userloggedin","Administrator")                                                        
                    return response                        
            elif request.POST["usertype"] == "Faculty":
                a=Faculty_detail.objects.filter(school_id=request.POST["id"])
                for i in range(len(a)):                    
                    if a[i].email == request.POST["email"] and a[i].password == request.POST["pwd"]:                        
                        response = HttpResponseRedirect('/signin/dashboard')
                        response.set_cookie("idloggedin",request.POST["id"])                                    
                        response.set_cookie("facultyname",a[i].name)                                    
                        response.set_cookie("userloggedin","Faculty")                                    
                        return response            
                return HttpResponse("faculty does not exists")
            elif request.POST["usertype"] == "Clerk":
                if a.clerk_id == request.POST["email"] and a.clerk_pwd == str(rc4(request.POST["pwd"], request.POST["email"])):
                    response = HttpResponseRedirect('/signin/dashboard')
                    response.set_cookie("idloggedin",a.id)                                    
                    response.set_cookie("userloggedin","Clerk")                                    
                    return response                    
            elif request.POST["usertype"] == "Student":
                a=Student_detail.objects.filter(school_id=request.POST["id"])
                for i in range(len(a)):                    
                    if a[i].Enroll == int(request.POST["email"]) and a[i].password == request.POST["pwd"]:                        
                        response = HttpResponseRedirect('/signin/dashboard')
                        response.set_cookie("idloggedin",request.POST["id"])                                    
                        response.set_cookie("facultyname",a[i].name)                                    
                        response.set_cookie("userloggedin","Student")                                    
                        return response            
                return HttpResponse("Student does not exists")
        except Exception as e:            
            return render(request,"home/static/templates/signin/signin.html",{"alert":"There is no account with this ID"})            
        return render(request,"home/static/templates/signin/signin.html",{"alert":"There is no account with this ID"})    

def signinwithparam(request,passparam):     
    try:
        if request.COOKIES['idloggedin']:
            if request.COOKIES['userloggedin'] == "Administrator":                
                uname = Administrator.objects.get(id = request.COOKIES['idloggedin'])
                studentss = Student_detail.objects.filter(school_id=request.COOKIES['idloggedin'])
                x = len
                y = studentss.filter
                if passparam == "dashboard":                                         
                    attstat = getattstat(request.COOKIES['idloggedin']) 
                    print("debug special 2")
                    sfp = getfeesper(request.COOKIES['idloggedin'])                   
                    sfp2 = getfeesper2(request.COOKIES['idloggedin'])                                       
                    currentyear = str(datetime.now().year-1) + "-" + str(datetime.now().year)                
                    nextyear = str(datetime.now().year) + "-" + str(datetime.now().year+1) 
                    return render(request,"home/static/templates/in-Administrator/examples/dashboard.html",{"uname":uname.admin_name,"st1":x(y(std=1)),"st2":x(y(std=2)),"st3":x(y(std=3)),"st4":x(y(std=4)),"st5":x(y(std=5)),"st6":x(y(std=6)),"st7":x(y(std=7)),"st8":x(y(std=8)),"st9":x(y(std=9)),"st10":x(y(std=10)),"st11":x(y(std=11)),"st12":x(y(std=12)),"sfp1":sfp[0],"sfp2":sfp[1],"sfp3":sfp[2],"sfp4":sfp[3],"sfp5":sfp[4],"sfp6":sfp[5],"sfp7":sfp[6],"sfp8":sfp[7],"sfp9":sfp[8],"sfp10":sfp[9],"sfp11":sfp[10],"sfp12":sfp[11],"cy":currentyear,"ny":nextyear,"sfpn1":sfp2[0],"sfpn2":sfp2[1],"sfpn3":sfp2[2],"sfpn4":sfp2[3],"sfpn5":sfp2[4],"sfpn6":sfp2[5],"sfpn7":sfp2[6],"sfpn8":sfp2[7],"sfpn9":sfp2[8],"sfpn10":sfp2[9],"sfpn11":sfp2[10],"sfpn12":sfp2[11],"att1":attstat[0],"att2":attstat[1],"att3":attstat[2],"att4":attstat[3],"att5":attstat[4],"att6":attstat[5],"att7":attstat[6],"att8":attstat[7],"att9":attstat[8],"att10":attstat[9],"att11":attstat[10],"att12":attstat[11]})
                elif passparam == "addremove":
                    return render(request,"home/static/templates/in-Administrator/examples/addremove.html",{"uname":uname.admin_name,"st1":x(y(std=1)),"st2":x(y(std=2)),"st3":x(y(std=3)),"st4":x(y(std=4)),"st5":x(y(std=5)),"st6":x(y(std=6)),"st7":x(y(std=7)),"st8":x(y(std=8)),"st9":x(y(std=9)),"st10":x(y(std=10)),"st11":x(y(std=11)),"st12":x(y(std=12))})
                    #return HttpResponse(request.COOKIES['idloggedin'])
                elif passparam == "Attendancemanager":
                    return render(request,"home/static/templates/in-Administrator/examples/Attendancemanager.html",{"uname":uname.admin_name})
                elif passparam == "changecredentials":
                    return render(request,"home/static/templates/in-Administrator/examples/changecredentials.html",{"uname":uname.admin_name})
                elif passparam == "Feescoll":
                    schoolid=int(request.COOKIES['idloggedin'][0])
                    try:
                        feesset = totalfees.objects.get(school_id=schoolid)
                        return render(request,"home/static/templates/in-Administrator/examples/Feescoll.html",{"uname":uname.admin_name,"totalfees":"hidden","insertfees":""})                    
                    except:
                        return render(request,"home/static/templates/in-Administrator/examples/Feescoll.html",{"uname":uname.admin_name,"totalfees":"","insertfees":"hidden"})  
                elif passparam == "viewdata":
                    return render(request,"home/static/templates/in-Administrator/examples/viewdata.html",{"uname":uname.admin_name})        
                elif passparam == "declaration":
                    return render(request,"home/static/templates/in-Administrator/examples/declaration.html",{"uname":uname.admin_name})
            elif request.COOKIES['userloggedin'] == "Clerk":
                uname = Administrator.objects.get(id = request.COOKIES['idloggedin'])
                studentss = Student_detail.objects.filter(school_id=request.COOKIES['idloggedin'])
                x = len
                y = studentss.filter                
                if passparam == "dashboard":                                            
                    sfp = getfeesper(request.COOKIES['idloggedin'])                   
                    sfp2 = getfeesper2(request.COOKIES['idloggedin'])                                       
                    currentyear = str(datetime.now  ().year-1) + "-" + str(datetime.now().year)                
                    nextyear = str(datetime.now().year) + "-" + str(datetime.now().year+1)                     
                    return render(request,"home/static/templates/in-Clerk/examples/dashboard.html",{"uname":uname.clerk_name,"st1":x(y(std=1)),"st2":x(y(std=2)),"st3":x(y(std=3)),"st4":x(y(std=4)),"st5":x(y(std=5)),"st6":x(y(std=6)),"st7":x(y(std=7)),"st8":x(y(std=8)),"st9":x(y(std=9)),"st10":x(y(std=10)),"st11":x(y(std=11)),"st12":x(y(std=12)),"sfp1":sfp[0],"sfp2":sfp[1],"sfp3":sfp[2],"sfp4":sfp[3],"sfp5":sfp[4],"sfp6":sfp[5],"sfp7":sfp[6],"sfp8":sfp[7],"sfp9":sfp[8],"sfp10":sfp[9],"sfp11":sfp[10],"sfp12":sfp[11],"cy":currentyear,"ny":nextyear,"sfpn1":sfp2[0],"sfpn2":sfp2[1],"sfpn3":sfp2[2],"sfpn4":sfp2[3],"sfpn5":sfp2[4],"sfpn6":sfp2[5],"sfpn7":sfp2[6],"sfpn8":sfp2[7],"sfpn9":sfp2[8],"sfpn10":sfp2[9],"sfpn11":sfp2[10],"sfpn12":sfp2[11]})                
                elif passparam == "Feescoll":
                    schoolid=int(request.COOKIES['idloggedin'][0])
                    try:
                        feesset = totalfees.objects.get(school_id=schoolid)
                        return render(request,"home/static/templates/in-Clerk/examples/Feescoll.html",{"uname":uname.clerk_name,"totalfees":"hidden","insertfees":""})                    
                    except:
                        return render(request,"home/static/templates/in-Clerk/examples/Feescoll.html",{"uname":uname.clerk_name,"totalfees":"","insertfees":"hidden"})  
                elif passparam == "viewdata":
                    return render(request,"home/static/templates/in-Clerk/examples/viewdata.html",{"uname":uname.clerk_name})        
                elif passparam == "declaration":
                    return render(request,"home/static/templates/in-Clerk/examples/declaration.html",{"uname":uname.clerk_name})
            elif request.COOKIES['userloggedin'] == "Faculty":
                uname = request.COOKIES['facultyname']
                studentss = Student_detail.objects.filter(school_id=request.COOKIES['idloggedin'])
                x = len
                y = studentss.filter
                if passparam == "dashboard":   
                    attstat = getattstat(request.COOKIES['idloggedin']) 
                    sfp = getfeesper(request.COOKIES['idloggedin'])                                       
                    sfp2 = getfeesper2(request.COOKIES['idloggedin'])                   
                    currentyear = str(datetime.now().year-1) + "-" + str(datetime.now().year)                
                    nextyear = str(datetime.now().year) + "-" + str(datetime.now().year+1) 
                    return render(request,"home/static/templates/in-Faculty/examples/dashboard.html",{"uname":uname,"st1":x(y(std=1)),"st2":x(y(std=2)),"st3":x(y(std=3)),"st4":x(y(std=4)),"st5":x(y(std=5)),"st6":x(y(std=6)),"st7":x(y(std=7)),"st8":x(y(std=8)),"st9":x(y(std=9)),"st10":x(y(std=10)),"st11":x(y(std=11)),"st12":x(y(std=12)),"sfp1":sfp[0],"sfp2":sfp[1],"sfp3":sfp[2],"sfp4":sfp[3],"sfp5":sfp[4],"sfp6":sfp[5],"sfp7":sfp[6],"sfp8":sfp[7],"sfp9":sfp[8],"sfp10":sfp[9],"sfp11":sfp[10],"sfp12":sfp[11],"cy":currentyear,"ny":nextyear,"sfpn1":sfp2[0],"sfpn2":sfp2[1],"sfpn3":sfp2[2],"sfpn4":sfp2[3],"sfpn5":sfp2[4],"sfpn6":sfp2[5],"sfpn7":sfp2[6],"sfpn8":sfp2[7],"sfpn9":sfp2[8],"sfpn10":sfp2[9],"sfpn11":sfp2[10],"sfpn12":sfp2[11],"att1":attstat[0],"att2":attstat[1],"att3":attstat[2],"att4":attstat[3],"att5":attstat[4],"att6":attstat[5],"att7":attstat[6],"att8":attstat[7],"att9":attstat[8],"att10":attstat[9],"att11":attstat[10],"att12":attstat[11]})              
                elif passparam == "Attendancemanager":                    
                    return render(request,"home/static/templates/in-Faculty/examples/Attendancemanager.html",{"uname":uname})
                elif passparam == "viewdata":
                    return render(request,"home/static/templates/in-Faculty/examples/viewdata.html",{"uname":uname})        
                elif passparam == "declaration":
                    return render(request,"home/static/templates/in-Faculty/examples/declaration.html",{"uname":uname})   
            elif request.COOKIES['userloggedin'] == "Student":
                uname = request.COOKIES['facultyname']
                studentss = Student_detail.objects.filter(school_id=request.COOKIES['idloggedin'])
                x = len
                y = studentss.filter
                if passparam == "dashboard":   
                    attstat = getattstat(request.COOKIES['idloggedin']) 
                    sfp = getfeesper(request.COOKIES['idloggedin'])                                       
                    sfp2 = getfeesper2(request.COOKIES['idloggedin'])                   
                    currentyear = str(datetime.now().year-1) + "-" + str(datetime.now().year)                
                    nextyear = str(datetime.now().year) + "-" + str(datetime.now().year+1) 
                    return render(request,"home/static/templates/in-Faculty/examples/dashboard.html",{"uname":uname,"st1":x(y(std=1)),"st2":x(y(std=2)),"st3":x(y(std=3)),"st4":x(y(std=4)),"st5":x(y(std=5)),"st6":x(y(std=6)),"st7":x(y(std=7)),"st8":x(y(std=8)),"st9":x(y(std=9)),"st10":x(y(std=10)),"st11":x(y(std=11)),"st12":x(y(std=12)),"sfp1":sfp[0],"sfp2":sfp[1],"sfp3":sfp[2],"sfp4":sfp[3],"sfp5":sfp[4],"sfp6":sfp[5],"sfp7":sfp[6],"sfp8":sfp[7],"sfp9":sfp[8],"sfp10":sfp[9],"sfp11":sfp[10],"sfp12":sfp[11],"cy":currentyear,"ny":nextyear,"sfpn1":sfp2[0],"sfpn2":sfp2[1],"sfpn3":sfp2[2],"sfpn4":sfp2[3],"sfpn5":sfp2[4],"sfpn6":sfp2[5],"sfpn7":sfp2[6],"sfpn8":sfp2[7],"sfpn9":sfp2[8],"sfpn10":sfp2[9],"sfpn11":sfp2[10],"sfpn12":sfp2[11],"att1":attstat[0],"att2":attstat[1],"att3":attstat[2],"att4":attstat[3],"att5":attstat[4],"att6":attstat[5],"att7":attstat[6],"att8":attstat[7],"att9":attstat[8],"att10":attstat[9],"att11":attstat[10],"att12":attstat[11]})              
                elif passparam == "Attendancemanager":                    
                    return render(request,"home/static/templates/in-Faculty/examples/Attendancemanager.html",{"uname":uname})
                elif passparam == "viewdata":
                    return render(request,"home/static/templates/in-Faculty/examples/viewdata.html",{"uname":uname})        
                elif passparam == "declaration":
                    return render(request,"home/static/templates/in-Faculty/examples/declaration.html",{"uname":uname})            
        else:
            return render(request,"home/static/error/error.html")
    except Exception as e:
        print(e)
        response = HttpResponseRedirect('/signin')
        response.delete_cookie('idloggedin')
        return response            
    response = HttpResponseRedirect('/signin')
    response.delete_cookie('idloggedin')
    return response  
    
def rc4(encryptiontext, key):
    return ARC4(hashlib.md5(key.encode()).hexdigest()).encrypt(hashlib.md5(encryptiontext.encode()).hexdigest())


def sendmail(msg, destinationaddress):
    try:
        username = 'ServiceEduwiz@gmail.com'
        password = 'eduwiz@123'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(username, destinationaddress, msg)
        server.quit()
        return "Success"
    except:
        return "Failed"

@csrf_exempt
def getenroll(request):
    try:        
        enroll = Student_detail.objects.filter(school_id=int(request.COOKIES['idloggedin'][0]),std=int(request.POST['standard'])).aggregate(Max('Enroll'))        
        return HttpResponse(json.dumps({"enroll" : int(enroll["Enroll__max"])+1}))
    except Exception as e:
        return HttpResponse(json.dumps({"enroll" : "1"}))

@csrf_exempt
def changefaculty(request):
    try:    
        schoolid = request.COOKIES["idloggedin"]   
        DOB = str(request.POST['DOB'])
        DOB = DOB[8]+DOB[9]+"-"+DOB[5]+DOB[6]+"-"+DOB[0:4]        
        pwd = request.POST['Password']
        enroll = request.POST['enroll']
        a = Faculty_detail.objects.get(school_id = int(schoolid), Enroll = enroll)
        a.name = request.POST['name']
        a.dob = DOB
        a.subject = request.POST['Subject']
        a.email = request.POST['Email']
        a.mobile = request.POST['mobile']
        a.address = request.POST['address']   
        a.password = pwd
        a.save()
        return HttpResponse(json.dumps({"msg":"Changes applied successfully"}))    
    except Exception as e:
        return HttpResponse(json.dumps({"msg2":e}))    

@csrf_exempt
def newstudent(request): 
    schoolid = request.COOKIES["idloggedin"]   
    standard = request.POST["standard"]
    enroll = request.POST['enroll']
    student_name = request.POST['name']
    fathername = request.POST['father_name']
    fatheroccupation = request.POST['father_occupation']
    DOB = str(request.POST['DOB'])
    DOB = DOB[8]+DOB[9]+"-"+DOB[5]+DOB[6]+"-"+DOB[0:4]
    student_Email = request.POST['Email']
    student_mobile = request.POST['mobile']
    student_address = request.POST['address']   
    andob = DOB.replace("-","")
    pwd = shuffle_words(str(enroll),str(andob))     
    try:
        Student_detail(
            school_id = schoolid,
            std = standard,
            Enroll = enroll,
            name = student_name,
            father_name = fathername,
            father_occupation = fatheroccupation,
            dob = DOB,
            email = student_Email,
            mobile = student_mobile,
            address = student_address,
            password = pwd
        ).save()  
        student_mobile = "91"+student_mobile
        mob = str(student_mobile)               
        msg = str("You are now registered with Eduwiz. your login Id for eduwiz is '"+enroll+"'. and Eduwiz password is "+pwd)
        #t = send(mob,msg)
        return HttpResponse(json.dumps({"msg" : "Successfully added the student in database."}))
    except Exception as e:
        return HttpResponse(json.dumps({"errormsg":str(e)}))
    
def checkifexists(email):
    try:
        Administrator.objects.get(admin_email=email)
    except:
        return False
    return True          

def checkifexistsmob(mobile):
    try:
        Administrator.objects.get(admin_mobile=mobile)
    except:
        return False
    return True          

@csrf_exempt
def getdata(request):
    standard = request.POST["stdstd"]
    enroll = request.POST['enroll']    
    data = Student_detail.objects.get(school_id=int(request.COOKIES['idloggedin'][0]),std=standard,Enroll = enroll)
    return HttpResponse(json.dumps({"name":data.name,"fathername":data.father_name,"fatherocc":data.father_occupation,
    "dob":data.dob,"email":data.email,"mobile":data.mobile,"address":data.address,"password":data.password}))

@csrf_exempt
def removestudent(request):    
    standard = request.POST["stdstd"]
    enroll = request.POST['enroll']
    Student_detail.objects.get(school_id=int(request.COOKIES['idloggedin'][0]),std=standard,Enroll = enroll).delete()
    return HttpResponse(json.dumps({"msg" : "Successfully deleted student data."}))

@csrf_exempt
def removefaculty(request):
    enroll = request.POST['enroll']
    Faculty_detail.objects.get(school_id=int(request.COOKIES['idloggedin'][0]),Enroll = enroll).delete()
    return HttpResponse(json.dumps({"msg" : "Successfully deleted faculty data."}))
    
@csrf_exempt
def changestudent(request):    
    schoolid = request.COOKIES["idloggedin"]   
    DOB = str(request.POST['DOB'])
    DOB = DOB[8]+DOB[9]+"-"+DOB[5]+DOB[6]+"-"+DOB[0:4]        
    pwd = request.POST['Password']
    standard = request.POST["standard"]
    enroll = request.POST['enroll']
    a = Student_detail.objects.get(school_id = int(schoolid), std = int(standard), Enroll = enroll)
    a.name = request.POST['name']
    a.father_name = request.POST['father_name']
    a.father_occupation = request.POST['father_occupation']
    a.dob = DOB
    a.email = request.POST['Email']
    a.mobile = request.POST['mobile']
    a.address = request.POST['address']   
    a.password = pwd
    a.save()
    return HttpResponse(json.dumps({"msg":"Changes applied successfully"}))

@csrf_exempt
def settotalfees(request):
    schoolid = request.COOKIES["idloggedin"]   
    st1 = int(request.POST['std1'])
    st2 = int(request.POST['std2'])
    st3 = int(request.POST['std3'])
    st4 = int(request.POST['std4'])
    st5 = int(request.POST['std5'])
    st6 = int(request.POST['std6'])
    st7 = int(request.POST['std7'])
    st8 = int(request.POST['std8'])
    st9 = int(request.POST['std9'])
    st10 = int(request.POST['std10'])
    st11 = int(request.POST['std11'])
    st12 = int(request.POST['std12'])    
    sd = totalfees(school_id = schoolid,s1=st1,s2=st2,s3=st3,s4=st4,s5=st5,s6=st6,s7=st7,s8=st8,s9=st9,s10=st10,s11=st11,s12=st12)
    sd.save()    
    return HttpResponse(json.dumps({}))

@csrf_exempt
def getfacultyenroll(request):
    try:        
        enroll = Faculty_detail.objects.filter(school_id=int(request.COOKIES['idloggedin'][0])).aggregate(Max('Enroll'))                
        return HttpResponse(json.dumps({"enroll" : int(enroll["Enroll__max"])+1}))
    except Exception as e:
        return HttpResponse(json.dumps({"enroll" : "1"}))
    pass

@csrf_exempt
def newfaculty(request):
    Schoolid = request.COOKIES["idloggedin"]   
    enroll = request.POST['enroll']
    Faculty_name = request.POST['name']    
    DOB = str(request.POST['DOB'])
    DOB = DOB[8]+DOB[9]+"-"+DOB[5]+DOB[6]+"-"+DOB[0:4]
    Faculty_Email = request.POST['Email']
    Faculty_subject = request.POST['Subjects']
    Faculty_mobile = request.POST['mobile']
    Faculty_address = request.POST['address']   
    andob = DOB.replace("-","")
    pwd = shuffle_words(str(enroll),str(andob))     
    try:
        Faculty_detail(
            school_id = Schoolid,
            Enroll = enroll,
            name = Faculty_name,            
            dob = DOB,
            subject = Faculty_subject,
            email = Faculty_Email,
            mobile = Faculty_mobile,
            address = Faculty_address,
            password = pwd
        ).save()  
        Faculty_mobile = "91"+Faculty_mobile
        mob = str(Faculty_mobile)               
        msg = str("You are now registered with Eduwiz. your login Id for eduwiz is '"+enroll+"'. and Eduwiz password is "+pwd)
        #t = send(mob,msg)
        return HttpResponse(json.dumps({"msg" : "Successfully added the Faculty in database."}))
    except Exception as e:
        return HttpResponse(json.dumps({"errormsg":str(e)}))

@csrf_exempt
def getfacultydata(request):
    enroll = request.POST['enroll']
    data = Faculty_detail.objects.get(school_id=int(request.COOKIES['idloggedin'][0]),Enroll = enroll)
    return HttpResponse(json.dumps({"name":data.name,
    "dob":data.dob,"email":data.email,"subject":data.subject,"mobile":data.mobile,"address":data.address,"password":data.password}))

@csrf_exempt
def getclerkdata(request):
    Schoolid = request.COOKIES["idloggedin"]  
    data = Administrator.objects.get(id = Schoolid) 
    return HttpResponse(json.dumps({"clerk_name":data.clerk_name,"clerk_id":data.clerk_id,"clerk_pwd":data.clerk_pwd,"dashboard_id":data.dashboard_id}))
    
@csrf_exempt
def changeclerkdata(request):
    Schoolid = request.COOKIES["idloggedin"]  
    name = request.POST['name']
    id = request.POST['id']
    pwd2 = request.POST['pwd']
    pwd = rc4(pwd2,id)    
    d = Administrator.objects.get(id = Schoolid)
    d.clerk_name = name
    d.clerk_id = id
    d.clerk_pwd = pwd
    d.save()    
    return HttpResponse(json.dumps({"msg":"Changes successfully applied."}))

@csrf_exempt
def changedashboarddata(request):
    Schoolid = request.COOKIES["idloggedin"]  
    id = request.POST['did']
    pwd2 = request.POST['dpwd']
    pwd = rc4(pwd2,id)    
    d = Administrator.objects.get(id = Schoolid)    
    d.dashboard_id = id
    d.dashboard_pwd = pwd
    d.save()  
    return HttpResponse(json.dumps({"msg":"Changes successfully applied."}))  

@csrf_exempt
def getallfaculty(request):
    Schoolid = request.COOKIES["idloggedin"]  
    date1 = request.POST["date"]    
    date1 = date1[8]+date1[9]+"-"+date1[5]+date1[6]+"-"+date1[0:4]   
    f = Faculty_detail.objects.filter(school_id=Schoolid)    
    a = {}
    for i in range(len(f)):
        try:
            w = attendance_faculty.objects.get(school_id=Schoolid,date=date1,Enroll=f[i].Enroll)
        except:
            w=None
        if w:            
            a[i+1] = {"Enroll":f[i].Enroll,"name":f[i].name,"subject":f[i].subject,"present":w.present}
        else:
            a[i+1] = {"Enroll":f[i].Enroll,"name":f[i].name,"subject":f[i].subject,"present":""}
    return HttpResponse(json.dumps({"data":a,"total":len(f)}))            
    
@csrf_exempt
def getallstudent(request):    
    STD = int(request.POST["std"])    
    Schoolid = request.COOKIES["idloggedin"]      
    date1 = request.POST["date"]    
    date1 = str(date1[8]+date1[9]+"-"+date1[5]+date1[6]+"-"+date1[0:4])    
    
    s = Student_detail.objects.filter(school_id=Schoolid,std=STD)    
    a = {}
    for i in range(len(s)):        
        try:
            w = attendance_student.objects.get(school_id=Schoolid,date=date1,std=STD ,Enroll=s[i].Enroll)                        
        except:
            w=None
        if w:            
            a[i+1] = {"Enroll":s[i].Enroll,"name":s[i].name,"fathername":s[i].father_name,"present":w.present}
        else:
            a[i+1] = {"Enroll":s[i].Enroll,"name":s[i].name,"fathername":s[i].father_name,"present":""}        
    return HttpResponse(json.dumps({"datas":a,"totals":len(s)}))

@csrf_exempt
def getallstudent2(request):      
    stad = int(request.POST["standard1"])    
    Schoolid = request.COOKIES["idloggedin"]              
    pyear = request.POST["payyear"]
    s = Student_detail.objects.filter(school_id=Schoolid,std=stad)    
    a = {}
    for i in range(len(s)):        
        try:
            w = feesrecord.objects.get(school_id=Schoolid,std=stad ,Enroll=s[i].Enroll,year=pyear)
        except:
            w=None
        if w:                        
            a[i+1] = {"Enroll":s[i].Enroll,"name":s[i].name,"fathername":s[i].father_name,"feespaid":w.paidfees,"totalfees":gettotalfees(stad,Schoolid)}
        else:            
            a[i+1] = {"Enroll":s[i].Enroll,"name":s[i].name,"fathername":s[i].father_name,"feespaid":0,"totalfees":gettotalfees(stad,Schoolid)}        
    return HttpResponse(json.dumps({"data":a,"total":len(s)}))

@csrf_exempt
def insertfacattendance(request):     
    attdate = request.POST["attdate"]
    attdate = attdate[8]+attdate[9]+"-"+attdate[5]+attdate[6]+"-"+attdate[0:4]
    w = attendance_faculty.objects.filter(date = attdate)
    if w:
        for i in range(len(w)):
            w[i].present = (request.POST[str(w[i].Enroll)] == "true")
            w[i].save()
    else:        
        Schoolid = request.COOKIES["idloggedin"]  
        f = Faculty_detail.objects.filter(school_id=Schoolid)               
        aa = []
        for i in range(int(request.POST["total"])):        
            attendance_faculty(school_id = Schoolid,date = attdate,Enroll = str(f[i].Enroll),present = (request.POST[str(f[i].Enroll)] == "true")).save()    
    return HttpResponse(json.dumps({"msg":"Attendance is successfully inserted"}))

@csrf_exempt
def insertstuattendance(request):
    attdate = request.POST["attdate"]
    attdate = attdate[8]+attdate[9]+"-"+attdate[5]+attdate[6]+"-"+attdate[0:4]
    stdd = request.POST["standard1"]
    w = attendance_student.objects.filter(date = attdate,std = stdd)
    if w:
        for i in range(len(w)):
            w[i].present = (request.POST[str(w[i].Enroll)] == "true")
            w[i].save()
    else:        
        Schoolid = request.COOKIES["idloggedin"]  
        f = Student_detail.objects.filter(school_id=Schoolid,std=stdd)               
        aa = []
        for i in range(int(request.POST["total"])):        
            attendance_student(school_id = Schoolid,date = attdate,std=stdd,Enroll = str(f[i].Enroll),present = (request.POST[str(f[i].Enroll)] == "true")).save()    
    return HttpResponse(json.dumps({"msg":"Attendance is successfully inserted"}))

@csrf_exempt
def insertstufees(request):
    stdd = request.POST["standard2"]
    Schoolid = request.COOKIES["idloggedin"]  
    Schoolid = int(Schoolid)
    attdate = str(date.today())
    attdate = attdate[8]+attdate[9]+"-"+attdate[5]+attdate[6]+"-"+attdate[0:4]
    total = int(request.POST["total"])
    yearpay = request.POST["payyear"]
    f = Student_detail.objects.filter(school_id=Schoolid,std=stdd)    
    for i in range(total):        
        try:
            isexist = feesrecord.objects.get(school_id = Schoolid,std=stdd,Enroll=str(f[i].Enroll),year = yearpay)
        except:
            isexist = None
        if isexist:
            isexist.paidfees = request.POST[str(f[i].Enroll)]
            isexist.year = yearpay
            isexist.date = attdate
            isexist.save()
        else:
            feesrecord(school_id = Schoolid,std=stdd,Enroll=str(f[i].Enroll),paidfees=request.POST[str(f[i].Enroll)],year = yearpay,date=attdate).save()
    return HttpResponse(json.dumps({"msg":"Fees record successfully inserted"}))

@csrf_exempt
def submitdeclarationtoall(request):
    Schoolid = request.COOKIES["idloggedin"]  
    date = request.POST["datee"]
    decaredon = request.POST["declaredate"]
    msg = request.POST["message"]
    declarationtoall(school_id=Schoolid,declared_on=decaredon,event_date=date,message = msg).save()
    return HttpResponse(json.dumps({"msg":"Declaration successful"}))

def logout(request):    
    response = HttpResponseRedirect('/signin')
    response.delete_cookie('idloggedin')
    response.delete_cookie('userloggdin')
    response.delete_cookie('facultyname')
    return response    
        
def shuffle_words(word_a, word_b):
    word = word_a + word_b
    lst = list(word)
    random.shuffle(lst)
    shuffled_word = ''.join(lst[:len(word_a)]) + ''.join(lst[len(word_a):]) 
    return shuffled_word

def send(mobile,msg):
    if type(mobile) is not str:
        return "Please enter valid phone number in string format"
    elif type(msg) is not str:
        return "Please enter valid message in string format"
    f1=open("api.txt","r")
    a=list()
    temp=f1.readline()
    while temp:
        a.append([temp[:32],temp[32:48]])
        temp=f1.readline()
    f1.close()
    response = requests.post('http://www.way2sms.com/api/v1/sendCampaign',{'apikey':a[0][0],'secret':a[0][1],'usetype':'stage','phone': mobile,'message':msg,'senderid':''})
    b=a;
    while response.text.find("\"status\":\"error\"") is not -1:
        if response.text.find("\"message\":\"API and Secret keys are expired.\"") is not -1:
            del a[0];
            response = requests.post('http://www.way2sms.com/api/v1/sendCampaign',{'apikey':a[0][0],'secret':a[0][1],'usetype':'stage','phone': mobile,'message':msg,'senderid':''})
            b=a
        if response.text.find("\"message\":\"Invalid phone number is given.\"") is not -1:
            return "invalidmobile"
        if response.text.find("\"message\":\"API and Secret key verification failed.\"") is not -1:
            if len(b)!=1:
                del b[0]
                response = requests.post('http://www.way2sms.com/api/v1/sendCampaign',{'apikey':b[0][0],'secret':b[0][1],'usetype':'stage','phone': mobile,'message':msg,'senderid':''})
            else:
                return "API and secret keys can not matched"
    f1=open("api.txt","w")
    newtext=""
    for i,j in a:
        newtext=newtext+i+j+"\n"
    f1.write(newtext)
    del newtext
    f1.close()
    return "success"
    
def gettotalfees(std,Schoolid):    
    if std == 1:
        return totalfees.objects.get(school_id=Schoolid).s1
    elif std == 2:
        return totalfees.objects.get(school_id=Schoolid).s2
    elif std == 3:
        return totalfees.objects.get(school_id=Schoolid).s3
    elif std == 4:
        return totalfees.objects.get(school_id=Schoolid).s4
    elif std == 5:
        return totalfees.objects.get(school_id=Schoolid).s5
    elif std == 6:
        return totalfees.objects.get(school_id=Schoolid).s6
    elif std == 7:
        return totalfees.objects.get(school_id=Schoolid).s7
    elif std == 8:
        return totalfees.objects.get(school_id=Schoolid).s8
    elif std == 9:
        return totalfees.objects.get(school_id=Schoolid).s9
    elif std == 10:
        return totalfees.objects.get(school_id=Schoolid).s10
    elif std == 11:
        return totalfees.objects.get(school_id=Schoolid).s11
    elif std == 12:
        return totalfees.objects.get(school_id=Schoolid).s12

def getfeesper(schoolid):
    t = []    
    try:
        currentyear = str(datetime.now().year-1) + "-" + str(datetime.now().year)                
        for i in range(12):
            feesp = feesrecord.objects.filter(school_id=schoolid,std=i+1,year=currentyear).aggregate(Sum('paidfees'))['paidfees__sum']
            total = int(gettotalfees(std = i+1,Schoolid = schoolid)) * len(Student_detail.objects.filter(school_id=schoolid,std=i+1))        
            if feesp is None:
                feesp = 0
            if not total:
                total = 1
            t.append((feesp*100)/total)  
    except:
        return [0 for i in range(12)]    
    return t

def getfeesper2(schoolid):
    t = []  
    try:  
        nextyear = str(datetime.now().year) + "-" + str(datetime.now().year+1)     
        for i in range(12):
            feesp = feesrecord.objects.filter(school_id=schoolid,std=i+1,year=nextyear).aggregate(Sum('paidfees'))['paidfees__sum']
            total = int(gettotalfees(std = i+1,Schoolid = schoolid)) * len(Student_detail.objects.filter(school_id=schoolid,std=i+1))        
            if feesp is None:
                feesp = 0
            if not total:
                total = 1
            t.append((feesp*100)/total)  
    except:
        return [0 for i in range(12)]    
    return t

@csrf_exempt
def changeadminpwd(request):    
    a = Administrator.objects.get(id = request.COOKIES["idloggedin"])
    a.admin_pwd = rc4(request.POST['newpwd'],Administrator.objects.get(id = request.COOKIES["idloggedin"]).admin_email)
    a.save()
    return HttpResponse(json.dumps({"msg":"Successfully changed password"}))

def getattstat(schoolid):
    data = []
    try:
        e = attendance_student.objects.filter(school_id=schoolid) 
        
        total = len(Student_detail.objects.filter(school_id=schoolid)) * 23
        
        m='0'
        
        for i in range(12):
            if i+1 not in [10,11,12]:
                m = str('-'+'0'+str(i+1)+'-')
                
                data.append((len(attendance_student.objects.filter(school_id=7,date__icontains = m,present=True))*100)/total)
            else:
                m = str('-'+str(i+1)+'-')
                data.append((len(attendance_student.objects.filter(school_id=7,date__icontains = m,present=True))*100)/total)    
    except:
        return [0 for i in range(12)]    
    return data    

@csrf_exempt
def getglobaldeclaration(request):
    Schoolid = request.COOKIES["idloggedin"]              
    user = request.POST["usertype"]
    s = declarationtoall.objects.filter(school_id=Schoolid)
    a = {}
    for i in range(len(s)):
        a[i+1] = {"declaredon":s[i].declared_on,"event_date":s[i].event_date,"message":s[i].message,"itsid":s[i].id}
    return HttpResponse(json.dumps({"data":a,"total":len(s)}))

@csrf_exempt
def removedeclaration(request,passparam):
    passparam = int(passparam)
    declarationtoall.objects.get(id = passparam).delete()
    return HttpResponse(json.dumps({"msg":"Announcement successfully deleted"}))

def about(request):
    return render(request, 'home/static/templates/horizontal flipping information card/Fliping info card photo.html')       
