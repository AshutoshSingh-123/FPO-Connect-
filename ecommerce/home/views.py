from django.shortcuts import render

# Create your views here.
def home(request):
 u=request.user.email
 context={'user_email':u}
 return render(request, 'index.html', context)
# def tryi(request):
#  return render(request, 'try.html')