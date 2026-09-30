from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

User = get_user_model()


def register_view(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('users:login')

    return render(request, 'users/pages/register.html', {'form': form})



def login_view(request):
    form = AuthenticationForm(data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', settings.DEFAULT_LOGIN_REDIRECT_URL) # В next будет '/product/add/', например.

            if next_url == settings.DEFAULT_LOGIN_REDIRECT_URL:
                return redirect(next_url, request.user.username)

            return redirect(next_url)

    return render(request, 'users/pages/login.html', {'form': form})


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
