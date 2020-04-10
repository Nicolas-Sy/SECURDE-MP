from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from library_website.models import BookInstance, Book, Author, Publisher

def register (request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if form.is_valid() and profile_form.is_valid():
			user = form.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserRegisterForm()
		profile_form = UserProfileForm()

	context = {'form' : form, 'profile_form': profile_form}
	return render(request, 'users/register.html', context)

@login_required
def profile (request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save() 
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='r').order_by('due_back')
	
	context = {
		'u_form': u_form,
		'p_form': p_form,
		'bookinstance_list': bookinstance_list,
	}
	return render(request, 'users/profile.html', context)

# class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
#     """Generic class-based view listing books on loan to current user."""
#     model = BookInstance
#     template_name ='users/profile.html'
#     paginate_by = 10
    
#     def get_queryset(self):
#         return 