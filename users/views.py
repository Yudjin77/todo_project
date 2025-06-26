from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from main import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserChangePasswordForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization'}

    # def get_success_url(self):
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Register'}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile',
                     'default_image': settings.DEFAULT_USER_IMAGE}
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'users/profile_view.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'profile_user'

class UserPasswordChange(PasswordChangeView):
    form_class = UserChangePasswordForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"



# Замена на RegisterUser
# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password']) #шифрование пароля(set_password) и занесение его в атрибут password
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

# Замена на LoginUser
# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

# Замена в LogoutView в urls.py
# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("users:login"))
