from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from . import models
from models import *
from django.contrib.auth import authenticate, login , logout
from django.core.context_processors import csrf
from django.views.generic.edit import CreateView,FormView,UpdateView
from django.views.generic import TemplateView
from django.db import models
from django.contrib.auth.models import User
from form import *
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
import unicodedata
from django.shortcuts import get_object_or_404
# Create your views here.


class Index(TemplateView):
	template_name = 'studentix/index.html'

# def index(request):
# 	user=request.user
# 	if user_is_authenticated():
# 		return redirect('home')
# 	else:
# 		return redirect('userLogin')

def userLogin(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('studentix/login.html',c)


def auth_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		loginUser=LoginUser.objects.get(user=user)
		url = 'home'
		return HttpResponseRedirect(url)
	else:
		return render(request, 'studentix/login.html', {
            'error_message': "Wrong user name or password. Please try again",
        })

def logoutme(request):
	logout(request)
	return HttpResponseRedirect(reverse(userLogin))

def studentSignup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		username = request.POST['username']
	
		try:
			old_user = User.objects.get(username=username)
		except User.DoesNotExist:
			old_user = None

		if old_user is not None:
			error_message = 'userneme is not available please selelect something other '
			return render(request, 'studentix/signup.html', locals())
		else:
			#dob		   = request.POST['dob']
			#print dob
			if form.is_valid():
				username   = form.cleaned_data['username']
				first_name = form.cleaned_data['first_name']
				last_name  = form.cleaned_data['last_name']
				email      = form.cleaned_data['email']
				password   = form.cleaned_data['password']
				contact	   = form.cleaned_data['contact']
				dob		   = form.cleaned_data['dob']
				new_user   = User(username=username, first_name=first_name,last_name=last_name,email=email,password=password)
				new_user.set_password(password)
				new_user.save()
				new_LoginUser = LoginUser(type=1,user=new_user,contactNo=contact,dob = dob)
				new_LoginUser.save()
				return HttpResponseRedirect(reverse('userLogin'))
			else:
				error_message = "fill correct values in form"
			
	else:
		form = SignupForm()

	return render(request, 'studentix/signup.html', locals())
def parentLogin(request):
	if request.method == 'POST':
		form = ParentForm(request.POST)
		username = request.POST['username']
		birthdate = request.POST['dob']
		try:
			old_user = User.objects.get(username=username)
		except User.DoesNotExist:
			old_user = None

		if old_user is  None:
			error_message = "User with this Username Does not exit"
			return render(request,'studentix/parentLogin.html',locals())

		else:
			loginUser=LoginUser.objects.get(user=old_user)
			birthdate = unicodedata.normalize('NFKD', birthdate).encode('ascii','ignore')
			temp = loginUser.dob.strftime('%Y-%m-%d')
			if loginUser.type != 1 or temp !=  birthdate :
				
				error_message = "Please enter correct birthdate"
				return render(request,'studentix/parentLogin.html',locals())
			else:
				url = 'parentHome/'+username
				print url
				return HttpResponseRedirect(url)
	else:
		form = ParentForm()

	return render(request,'studentix/parentLogin.html',locals())	


def parentHome():
	pass
	
login_required(login_url='/userLogin')
def userHome(request):
	u = request.user
	loginUser=LoginUser.objects.get(user=u)
	s=u.username
	course_list = Course.objects.filter(loginuser=loginUser).order_by('-status')
	message_list = Message.objects.filter(loginuser_reciever=loginUser).order_by('-send_at')
	
	return render(request,'studentix/userHome.html',locals())

def allCourse(request):
	all_course_list = Course.objects.all().order_by('-status')
	return render(request,'studentix/allCourse.html',locals())	

def courseDetail(request,coursename):
	user=request.user
	coursename = coursename.replace ("_", " ")
	c = get_object_or_404(Course, pk=coursename)
	notice_list = c.notice_set.order_by('-created')[:5]	

	s=user.username;
	if s != "":
		p=s+'/'

	if user.is_authenticated():
		loginuser=LoginUser.objects.get(user=user)
		quiz=Quiz.objects.get(course=c,loginuser=loginuser)
		users_enrolled_in_course=c.loginuser.all()
		if loginuser in users_enrolled_in_course:
			is_enrole = True
		else:
			is_enrole = False

		instructor_list = c.loginuser.all().filter(type=2)
		course_content = CourseContent.objects.filter(course = c)
	else:
		is_enrole = False
		instructor_list = c.loginuser.all().filter(type=2)
	return render(request,'studentix/courseDetail.html',locals())


login_required(login_url='/userLogin')
def enrol(request,coursename):
	print "here"
	coursename=coursename.replace ("_", " ")
	c = get_object_or_404(Course, pk=coursename)
	u=request.user
	loginuser=LoginUser.objects.get(user=u)
	q = Quiz.objects.create(loginuser=loginuser,course=c)
	q.save()
	is_enrole=True
	message = "Congratulation! You have successfully Enroled"
	coursename=coursename.replace (" ", "_")
	url = '../courseDetail'+'/'+coursename
	return HttpResponseRedirect(url)	


login_required(login_url='/userLogin')
def content(request,coursename,pk):
	
	c_content =  get_object_or_404(CourseContent,pk=pk)
	return render(request,'studentix/content.html',locals())

login_required(login_url='/userLogin')
def mid_term_quiz(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	u=request.user
	loginuser=LoginUser.objects.get(user=u)
	question_list=c.question_set.all().filter(status=1)
	
	print request.method
	if request.method == 'POST':
		score=0
		q = question_list[0]
		ans = request.POST['ans0']
		if q.answer == ans:
			score+=1

		q = question_list[1]
		ans = request.POST['ans1']
		if q.answer == ans:
			score+=1

		q = question_list[2]
		ans = request.POST['ans2']
		if q.answer == ans:
			score+=1

		q = question_list[3]
		ans = request.POST['ans3']
		if q.answer == ans:
			score+=1

		q = question_list[4]
		ans = request.POST['ans4']
		if q.answer == ans:
			score+=1

		quiz=Quiz.objects.get(course=c,loginuser=loginuser)
		quiz.mid_term_score=score
		quiz.save()
		coursename=coursename.replace ("_", " ")
		url='mid_term_evaluation'
		print url
		return HttpResponseRedirect(url)

	else:
		question0=question_list[0]
		question1=question_list[1]
		question2=question_list[2]
		question3=question_list[3]
		question4=question_list[4]
		print "post but here"
		return render(request,'studentix/mid_term_quiz.html',locals())

login_required(login_url='/userLogin')
def end_term_quiz(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	u=request.user
	loginuser=LoginUser.objects.get(user=u)
	question_list=c.question_set.all().filter(status=2)
	
	print request.method
	if request.method == 'POST':
		score=0
		q = question_list[0]
		ans = request.POST['ans0']
		if q.answer == ans:
			score+=1

		q = question_list[1]
		ans = request.POST['ans1']
		if q.answer == ans:
			score+=1

		q = question_list[2]
		ans = request.POST['ans2']
		if q.answer == ans:
			score+=1

		q = question_list[3]
		ans = request.POST['ans3']
		if q.answer == ans:
			score+=1

		q = question_list[4]
		ans = request.POST['ans4']
		if q.answer == ans:
			score+=1

		quiz=Quiz.objects.get(course=c,loginuser=loginuser)
		quiz.end_term_score=score
		quiz.save()
		coursename=coursename.replace ("_", " ")
		url='end_term_evaluation'
		print url
		return HttpResponseRedirect(url)

	else:
		question0=question_list[0]
		question1=question_list[1]
		question2=question_list[2]
		question3=question_list[3]
		question4=question_list[4]
		return render(request,'studentix/end_term_quiz.html',locals())

login_required(login_url='/userLogin')
def mid_term_evaluation(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	u=request.user
	loginuser=LoginUser.objects.get(user=u)
	quiz=Quiz.objects.get(course=c,loginuser=loginuser)
	marks=quiz.mid_term_score
	if quiz.mid_term_score <0 :
		coursename=coursename.replace (" ", "_")
		url = coursename+'/'+'mid_term_quiz'
		return HttpResponseRedirect(url)
	else:
		question_list=c.question_set.all().filter(status=1)
		return render(request,'studentix/evaluation.html',locals())

login_required(login_url='/userLogin')
def end_term_evaluation(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	u=request.user
	loginuser=LoginUser.objects.get(user=u)
	quiz=Quiz.objects.get(course=c,loginuser=loginuser)
	marks=quiz.end_term_score
	if quiz.end_term_score <0 :
		coursename=coursename.replace (" ", "_")
		url = coursename+'/'+'end_term_quiz'
		return HttpResponseRedirect(url)
	else:
		question_list=c.question_set.all().filter(status = 2)
		return render(request,'studentix/evaluation.html',locals())

login_required(login_url='/userLogin')
def addContent(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	if request.method == 'POST':
		title=request.POST['title']
		content=request.POST['content']
		cc=CourseContent(course=c,title=title,content=content)   #cc->course content
		cc.save()
		return HttpResponseRedirect('../content_succefully_added')
	else:
		return render(request,'studentix/addContent.html',locals())



login_required(login_url='/userLogin')
def addNotice(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	if request.method=='POST':
		h=request.POST['heading']
		d=request.POST['detail']
		new_notice=Notice(course=c,heading=h,detail=d)
		new_notice.save()
		return HttpResponseRedirect('../notice_succefully_added')
	else:
		return render(request,'studentix/addNotice.html',locals())


login_required(login_url='/userLogin')
def content_succefully_added(request):
	type = "Course Content"
	return render(request,'studentix/successfully_added.html',locals())

login_required(login_url='/userLogin')
def notice_succefully_added(request):
	type = "Notice"
	return render(request,'studentix/successfully_added.html',locals())


login_required(login_url='/userLogin')
def mid_term_quiz_succefully_added(request):
	type = "MID term quiz"
	return render(request,'studentix/successfully_added.html',locals())

login_required(login_url='/userLogin')
def end_term_quiz_succefully_added(request):
	type = "End term quiz"
	return render(request,'studentix/successfully_added.html',locals())	

# def sendEmail(request):
# 	user=request.user
# 	if request.method=='POST':

# 		u=request.post['username']
# 		user_r=User.objects.get(username=u)
#         loginuser=LoginUser.objects.get(user=user_r)
#         s=request.POST['subject']
#         m=request.POST['message']
#         new_message=Message(user=user,loginuser_reciever=loginuser,subject = s,message = m)
#         new_message.save()
#         return HttpResponseRedirect('../email_succefully_added')

#     else:
#     	return render(request,'studentix/sendEmail.html',locals()) 

def sendEmail(request):
	user=request.user
	if request.method == 'POST':
		u=request.POST['username']
		user_r = User.objects.get(username =u)
		loginuser = LoginUser.objects.get(user = user_r)
		s = request.POST['subject']
		m = request.POST['message']
		new_message=Message(user_sender=user,loginuser_reciever=loginuser,subject = s,message = m)
		new_message.save()
		return HttpResponseRedirect('../email_succefully_added')
	else:
		return render(request,'studentix/sendEmail.html',locals())


def email_succefully_added(request):
	type = "Email"
	return render(request,'studentix/successfully_added.html',locals())	

def performance(request,username):
	u=user.objects.get(username)
	loginuser=LoginUser.objects.get(user=u)
	quiz_list=Quiz.objects.all().filter(loginuser=loginuser)
	return render(request,'studentix/performance.html',locals())	


login_required(login_url='/userLogin')
def add_mid_term_quiz(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	if request.method=='POST':
		q=request.POST['q0']
		c1=request.POST['c1']
		c2=request.POST['c2']
		c3=request.POST['c3']
		c4=request.POST['c4']
		a=request.POST['a0']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q1']
		c1=request.POST['c11']
		c2=request.POST['c12']
		c3=request.POST['c13']
		c4=request.POST['q14']
		a=request.POST['a1']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q2']
		c1=request.POST['c21']
		c2=request.POST['c22']
		c3=request.POST['c23']
		c4=request.POST['c24']
		a=request.POST['a2']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q3']
		c1=request.POST['c31']
		c2=request.POST['c32']
		c3=request.POST['c33']
		c4=request.POST['c34']
		a=request.POST['a3']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q4']
		c1=request.POST['c41']
		c2=request.POST['c42']
		c3=request.POST['c43']
		c4=request.POST['c44']
		a=request.POST['a4']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

	else:
		return render(request,'studentix/add_mid_term_quiz.html',locals())




login_required(login_url='/userLogin')
def add_end_term_quiz(request,coursename):
	coursename=coursename.replace ("_", " ")
	c=Course.objects.get(courseName=coursename)
	if request.method=='POST':
		q=request.POST['q0']
		c1=request.POST['c1']
		c2=request.POST['c2']
		c3=request.POST['c3']
		c4=request.POST['c4']
		a=request.POST['a0']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q1']
		c1=request.POST['c11']
		c2=request.POST['c12']
		c3=request.POST['c13']
		c4=request.POST['q14']
		a=request.POST['a1']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q2']
		c1=request.POST['c21']
		c2=request.POST['c22']
		c3=request.POST['c23']
		c4=request.POST['c24']
		a=request.POST['a2']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q3']
		c1=request.POST['c31']
		c2=request.POST['c32']
		c3=request.POST['c33']
		c4=request.POST['c34']
		a=request.POST['a3']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

		q=request.POST['q4']
		c1=request.POST['c41']
		c2=request.POST['c42']
		c3=request.POST['c43']
		c4=request.POST['c44']
		a=request.POST['a4']
		que=Question(course=c,question_text=q,choice_1=c1,choice_2=c2,choice_3=c3,choice_4=c4,answer=a,status=1)
		que.save()

	else:
		return render(request,'studentix/add_end_term_quiz.html',locals())			