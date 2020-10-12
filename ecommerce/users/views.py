from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from store.models import Product, Cart, Fpo_Registeration, Service, Ngo_Registeration
from blog.models import Post
from .models import Message, Profile
from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form_signup = SignUpForm(request.POST)
        if form_signup.is_valid():
            form_signup.save()
            username = form_signup.cleaned_data.get('username')
            raw_password = form_signup.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        
        form_signup = SignUpForm()
    return render(request, 'signup.html', {'form_signup': form_signup})
@login_required(login_url='login')
def fpo_dash(request):
     products=Product.objects.filter(product_by=request.user)
     posts=Post.objects.filter(author=request.user)
     fpo=Fpo_Registeration.objects.get(fpo_username=request.user.username)
     wishlist_products=Cart.objects.filter(by_fpo=fpo)
     msgs=Message.objects.filter(to=fpo)
     
     
     total_msg=msgs.count()
     total_wishlist=wishlist_products.count()
     total_post=posts.count()
     total_product=products.count()
     context={'total_product':total_product, 'products':products, 'posts':posts, 'total_post':total_post, 'wishlist_products':wishlist_products, 'total_wishlist':total_wishlist, 'total_msg':total_msg, 'msgs':msgs}
     return render(request, 'fpo_dashboard.html',context)

@login_required(login_url='login')
def ngo_dash(request):
     fpo=Ngo_Registeration.objects.get(ngo_username=request.user.username)
     
     
     services=Service.objects.filter(service_by=fpo)
     total_services=services.count()
     context={'services':services, 'total_services':total_services}
     return render(request, 'ngo_dashboard.html',context)
@login_required
def profile(request):
  if request.method=='POST':
    u_form=UserUpdateForm(request.POST, instance=request.user)
    p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect('profile')

  else:
    u_form=UserUpdateForm(instance=request.user)
    p_form=ProfileUpdateForm(instance=request.user.profile)
  context={'u_form':u_form,
  'p_form':p_form
  }
  return render(request, 'profile.html',context)