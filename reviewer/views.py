from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login

from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model
from .models import Course, Announcement, ImportUser, Comment
from .forms import CourseForm, CommentForm, CommentFormDisabled, ImportUserCreationForm

import json

# Create your views here.

def index(request):
	announcements = Announcement.objects.order_by('datepost')

	context = {'announcements': announcements, 'ann_len': len(announcements)}

	return render(request, 'reviewer/index.html', context)

def construction(request):
	return render(request, 'reviewer/construction.html')

def su(request):


	courses = Course.objects.order_by('code', 'number_len', 'number')

	if request.method == "POST":
		data = request.POST
		courseform = CourseForm(data)

		tempname = data['name']
		coursefulln = tempname.split(" ")
		tempnum = coursefulln[len(coursefulln)-1]
		tempcode = ' '.join(coursefulln[:-(len(coursefulln)-1)])
		temp_oldcurr = data.get('old_curr', False)
		temp_visible = data.get('visible', True)

		if temp_oldcurr == 'on':
			temp_oldcurr = True
		if temp_visible == 'on':
			temp_visible = True
		
		# Add input validation
		new_course = Course(name=data['name'], code=tempcode, number=tempnum, title=data['title'], description=data['description'], old_curr=temp_oldcurr, visible=temp_visible)	

		new_course.save()
		return redirect('su')
	else:
		courseform = CourseForm()
	
	context = { 'courses': courses, 'courseform': courseform}


	return render(request, 'reviewer/admin.html', context)


def courselist(request):

	courselist = Course.objects.filter(visible=True).order_by('code', 'number_len', 'number')

	context = {'courselist': courselist, 'course_count': len(courselist)}
	return render(request, 'reviewer/course-list.html', context)

def course(request, csubj, cnum):

	coursefilter = Course.objects.filter(code__iexact=csubj).filter(number__iexact=str(cnum))

	if (len(coursefilter) > 0):
		course_comments = coursefilter[0].comment_set.order_by('-date_posted')

		if request.method == "POST":
			data = request.POST
			resultid = None 

			if request.user.is_authenticated:
				commentform = CommentForm(data, request.FILES)

				# Add input validation
				new_comment = Comment(course_attr=coursefilter[0], user_attr=request.user, body=data['body'], image=request.FILES.get('image', None))	
				new_comment.save()
				resultid = new_comment.id
			else:
				commentform = CommentFormDisabled(data, request.FILES)

			redirect('course', csubj, cnum)

			data = {'commentid': resultid}
			return HttpResponse( json.dumps(data) )
		elif request.method == "DELETE":
			comment_findid = int(request.body.decode("utf-8").split("-")[1])

			delcom = Comment.objects.get(pk=comment_findid)
			result = "Nice try."
			if (request.user == delcom.user_attr):
				delcom.delete()
				result = "Delete successful."
			return HttpResponse(result)
		elif request.method == "GET":
			if request.user.is_authenticated:
				commentform = CommentForm()
			else:
				commentform = CommentFormDisabled()

			context = {'course_filt': coursefilter[0], 'course_comments': course_comments, 'comment_form': commentform}
			return render(request, 'reviewer/course.html', context)
	else:
		raise Http404("Course does not exist.")

def user(request, username):

	user_filter = ImportUser.objects.filter(username=username)

	if (len(user_filter) > 0):
		comments = user_filter[0].comment_set.order_by('-date_posted')
		context = {'user_filt': user_filter[0], 'user_comments':comments }
		return render(request, 'reviewer/user.html', context)
	else:
		raise Http404("User does not exist.")



def register(request):
	
	if request.method == 'POST':
		form = ImportUserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)

			login(request, user)
			return redirect('index')
	else:
		form = ImportUserCreationForm()

	context = {'form': form}
	return render(request, 'registration/register.html', context)