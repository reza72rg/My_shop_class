from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

          
# Create your views here.
class UserLoginView(View):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    
 
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        global next
        next = request.GET.get('next')
        form = self.form_class
        return render(request,self.template_name,{'form':form})
    
    def post(self, request):
       
        form = self.form_class(request=request,data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)       
                if next:
                    messages.success(request,'you are login successfuly','success')
                    return redirect(next)
                messages.success(request,'you are login successfuly','success')
                return redirect('/')
                # Redirect to a success page.
            
        else:
            messages.error(request,'username or password is wrong','danger')
            #messages.success(request,'Thanks . Your message has been received.','success')        
        return render(request,self.template_name,{'form':form})   
         

class UserLogOut(LoginRequiredMixin, View):
    login_url = 'accounts/login.html'  
    def get(self,request):
        logout(request)
        messages.success(request, 'This is a success message.')
        return redirect('/')
        
   

class RegisterView(View):
    form_class = RegistrationForm
    template_name = 'accounts/singup.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password1'])
            messages.success(request,'Thanks . Your registration was successfuly plase log in.','success')
            return redirect('accounts:login')
        return render(request,self.template_name,{'form':form})

