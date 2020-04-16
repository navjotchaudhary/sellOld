from django.shortcuts import render,redirect
from django.contrib.auth import logout as ls
from .forms import SignUpForm
from django.contrib import auth
from .models import User
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
# Create your views here.
def logout(request):    
    ls(request)
    return redirect('product:product_list')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        #form.save()
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        

        site_name = get_current_site(request)
        domain = site_name.domain

        message = {
            'domain': domain,
            'site_name': site_name,
            'token': account_activation_token.make_token(user),
            
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
        }
        message = render_to_string("registration/account_activate.html",{
            'domain': domain,
            'site_name': site_name,
            'token': account_activation_token.make_token(user),
            
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
        })
        


        send_mail(
            'registered',
            f'you r {message}',
            'b.20.python.01.02@gmail.com',
            ['b.20.python.01.02@gmail.com'],
            fail_silently=False,
        )
        return redirect('product:product_list')
    return render(request, 'registration/signup.html', {'form': form})




def activateAccount(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        
        return redirect('product:product_list')
    else:
        print("Invalid Link")
        return HttpResponse("<h3>Invalid Link</h3>")