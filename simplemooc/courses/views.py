from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import Course, Enrollment
from .forms import ContactCourse

def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	#variáveis
	context = {
		'courses': courses
	}

	return render(request, template_name, context)

def details(request, slug):
	# course = get_object_or_404(Course, pk=pk)
	course = get_object_or_404(Course, slug=slug)
	context = {}

	if request.method == 'POST':
		form = ContactCourse(request.POST)
		if form.is_valid():
			context['is_valid'] = True
			form.send_mail(course)
			# print(form.cleaned_data['name'])
			# print(form.cleaned_data['message'])
			form = ContactCourse()

	else:
		form = ContactCourse()

	context['form'] = form
	context['course'] = course

	template_name = 'courses/details.html'
	return render(request, template_name, context)

@login_required
def enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)
	enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
	if created:
		# enrollment.active()
		flash = 'Você foi inscrito no curso com sucesso!'
		messages.success(request, flash)
	else:
		flash = 'Você já está inscrito neste curso.'
		messages.info(request, flash)
	return redirect('accounts:dashboard')

@login_required
def announcements(request, slug):
	course = get_object_or_404(Course, slug=slug)
	if not request.user.is_staff:
		enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
		if not enrollment.is_approved():
			messages.error(request, 'A sua inscrição está pendente.')
			return redirect('accounts:dashboard')

	template_name = 'courses/announcements.html'
	context = {
		'course': course
	}
	return render(request, template_name, context)