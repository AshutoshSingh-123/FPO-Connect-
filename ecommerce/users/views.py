from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from store.models import Product, Cart, Fpo_Registeration, Service, Ngo_Registeration, ServiceForCustomer
from blog.models import Post
from .models import Message, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def signup(request):
    terms=True
    if request.method == 'POST':
        agree=request.POST.get('agree')
       
        if agree:
         form_signup = SignUpForm(request.POST)
         if form_signup.is_valid():
           
            user =  form_signup.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form_signup.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Mail has been sent to your provided email address. Please confirm your email address to complete the registration')
            # username = form_signup.cleaned_data.get('username')
            # raw_password = form_signup.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('login')
        else:
          terms=False
          form_signup = SignUpForm()
          return render(request, 'signup.html', {'form_signup': form_signup, 'agree':terms})
    else:
        
        form_signup = SignUpForm()
    return render(request, 'signup.html', {'form_signup': form_signup, 'agree':terms})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='login')
def fpo_dash(request):
     products=Product.objects.filter(product_by=request.user)
     posts=Post.objects.filter(author=request.user)
     fpo=Fpo_Registeration.objects.get(fpo_username=request.user.username)
     wishlist_products=Cart.objects.filter(by_fpo=fpo)
     msgs=Message.objects.filter(to=fpo).order_by('-date')
    #  fpo=Ngo_Registeration.objects.get(ngo_username=request.user.username)
     
     
     services=ServiceForCustomer.objects.filter(service_by=fpo)
     total_services=services.count()
     
     total_msg=msgs.count()
     total_wishlist=wishlist_products.count()
     total_post=posts.count()
     total_product=products.count()
     context={'total_product':total_product, 'products':products, 'posts':posts, 'total_post':total_post, 'wishlist_products':wishlist_products, 'total_wishlist':total_wishlist, 'total_msg':total_msg, 'msgs':msgs, 'services':services, 'total_services':total_services}
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