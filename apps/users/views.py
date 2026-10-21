from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/pages/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')



class LoginView(AuthLoginView):
    template_name = 'users/pages/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', settings.DEFAULT_LOGIN_REDIRECT_URL)

        if next_url == settings.DEFAULT_LOGIN_REDIRECT_URL:
            return reverse_lazy(next_url, kwargs={'username': self.request.user.username})

        return next_url


@require_POST
def logout_view(request):
    logout(request)
    return redirect("eshop:home_page")



def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    # product = Product.objects.filter(author=user) # .order_by('-created_at')
    products = user.products.all()  # type: ignore


    context = {
    'user': user,
    'products': products
    }
    return render(request, 'users/pages/profile.html', context)
