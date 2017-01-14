from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
# FN,LN,Email,password

class LoginUser(models.Model):
	type = models.IntegerField()
	user = models.OneToOneField(User, primary_key = True)
	contactNo = models.CharField(max_length=10)
	dob = models.DateField(("Date of Birth"),default=date.today)
	

	def __unicode__(self):
		if self.type == 2:
			strg = self.user.username + ' Instructor type user'
		else:
			strg =self.user.username + ' Student type user'  
		return strg


class Course(models.Model):
	loginuser = models.ManyToManyField(LoginUser, through='Quiz')
	courseName = models.CharField(max_length=50,primary_key=True)
	description = models.CharField(max_length=1000)
	image = models.CharField(max_length=1000)
	prerequisites = models.CharField(max_length=1000)
	syllabus = models.CharField(max_length=1000)
	payments = models.IntegerField()
	# notice = models.CharField(max_length=1000)
	status = models.IntegerField(default=1)          # -1->expired,0->ongoing,1->upcoming
	start_date = models.DateField(default=date.today)
	end_date = models.DateField(default=date.today)
	mid_term = models.IntegerField(default=-1)
	end_term = models.IntegerField(default=-1)

	def __unicode__(self):
		return self.courseName

class Quiz(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	loginuser = models.ForeignKey(LoginUser,on_delete=models.CASCADE)
	mid_term_score = models.IntegerField(default=-1)
	end_term_score = models.IntegerField(default=-1)
	status = models.IntegerField(default = 1)      #1 for mid_term 2 for end_term
	Taken_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		strg = self.course.courseName +' Taken by '+ self.loginuser.user.username
		return strg

class CourseContent(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=10000)
	def __unicode__(self):
		return self.title


class Notice(models.Model):
	course  = models.ForeignKey(Course,on_delete=models.CASCADE)
	heading = models.CharField(max_length=100)
	detail  = models.CharField(max_length=1000)
	created = models.DateTimeField(auto_now_add=True)
		


class Question(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	status = models.IntegerField(default= 1)
	question_text=models.CharField(max_length=100,default='')
	choice_1=models.CharField(max_length=100,default='')
	choice_2=models.CharField(max_length=100,default='')
	choice_3=models.CharField(max_length=100,default='')
	choice_4=models.CharField(max_length=100,default='')
	answer = models.IntegerField()

	def __unicode__(self):
		strg = 'Question ' + str(self.pk)
		return strg

class Message(models.Model):
	user_sender=models.OneToOneField(User)
	loginuser_reciever=models.OneToOneField(LoginUser)
	subject = models.CharField(max_length=100,default='')
	message = models.CharField(max_length=10000,default='')
	send_at = models.DateTimeField(auto_now_add=True)