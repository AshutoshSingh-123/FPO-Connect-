from django.shortcuts import render

# Create your views here.
def home(request):
 return render(request, 'index.html')
# def tryi(request):
#  return render(request, 'try.html')