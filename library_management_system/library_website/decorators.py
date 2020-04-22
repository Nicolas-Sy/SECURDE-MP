from django.http import HttpResponse
from django.shortcuts import redirect 

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)

			else:
				return HttpResponse('You are not allowed to view this page.')

		return wrapper_func
	return decorator

def bookmanager_only(view_func):
	def wrapper_function(request, *args, **kwargs):

		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'Student/Teacher':
			return redirect('library-website')

		if group == 'BookManager':
			return view_func(request, *args, **kwargs)


	return wrapper_function


def user_is_admin(view_func):
	def wrapper_function(request, *args, **kwargs):

		if request.user.is_authenticated and request.user.is_staff:
			return HttpResponse('You are not allowed to view this page.')

		elif request.user.is_authenticated:
			return view_func(request, *args, **kwargs)

		else:
			return view_func(request, *args, **kwargs)

	return wrapper_function
