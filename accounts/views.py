from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User
from .forms import RegisterForm,ShippingForm , BillingForm , UserForm , ProfileForm
from django.views import View, generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile,BillingAddress, ShippingAddress
from cart.models import Order
#token import
from accounts.utils.email import send_account_confirmation_email
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode    
from accounts.token import account_activation_token


class DashboardView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user = request.user)
        billing_address = BillingAddress.objects.filter(user=self.request.user)
        shipping_address = ShippingAddress.objects.filter(user=self.request.user)
        confirm_orders = Order.objects.filter(user=request.user, confirm_order=True, complete_order=False)
        complete_orders = Order.objects.filter(user=request.user, confirm_order=True, complete_order=True)
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profiles)
        context = {
            'profile':profile,
            'billing_address':billing_address,
            'shipping_address':shipping_address,
            'confirm_orders':confirm_orders,
            'complete_orders':complete_orders,
            'user_form':user_form,
            'profile_form':profile_form,

        }
        return render(request, 'accounts/dashboard.html', context)
    
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profiles)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:dashboard')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request, 'accounts/dashboard.html', context)


class RegisterView(generic.CreateView):
    template_name = 'accounts/login.html'
    form_class = RegisterForm
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db() 
        user.profiles.phone = form.cleaned_data.get('phone')
        user.profiles.address = form.cleaned_data.get('address')
        user.save()
        send_account_confirmation_email(self.request, user)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)
    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url:
            return "%s" % (next_url)
        else:
            return reverse_lazy('accounts:login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode('utf-8')
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return redirect('accounts:login')
    else:
        return redirect('accounts:login')



class ShippingView(View):
    def get(self,request):
        form = ShippingForm()
        context = {
                'form': form,
        }
        return render(request, "accounts/shipping_add_form.html",context)
    
    def post(self,request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            billing_with = request.POST.get("billing")
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            if billing_with == 'yes':
                billing, created = BillingAddress.objects.get_or_create(user=request.user, full_name=request.POST.get("full_name"), phone=request.POST.get("phone"), city=request.POST.get("city"), area=request.POST.get("area"), address=request.POST.get("address"), address_type=request.POST.get("address_type"))
            return redirect('accounts:dashboard')
        else:
            context = {
                'form': form,
            }
            return render(request, "accounts/shipping_add_form.html",context)


class ShippingUpdateView(View):
    def get(self,request,*args, **kwargs):
        shipping = get_object_or_404(ShippingAddress, id=kwargs['id'])    
        context = {
            'shipping':shipping
        }
        return render(request, "accounts/shipping_update.html",context)
    
    def post(self,request,*args, **kwargs):
        shipping = get_object_or_404(ShippingAddress, id=kwargs['id'])  
        if request.method == "POST":
            user = request.user
            form = ShippingForm(request.POST or None, instance=shipping)
            if form.is_valid():
                form.save()
                return redirect('accounts:dashboard')


class BillingView(generic.FormView):
    def get(self,request):
        form = BillingForm()
        context = {
                'form': form,
        }
        return render(request, "accounts/billing_add_form.html",context)

    def post(self,request):
        form = BillingForm(request.POST)
        if form.is_valid():
            shipping_with = request.POST.get("shipping")
            billing = form.save(commit=False)
            billing.user = request.user
            billing.save()
            if shipping_with == 'yes':
                shipping, created = ShippingAddress.objects.get_or_create(user=request.user, full_name=request.POST.get("full_name"), phone=request.POST.get("phone"), city=request.POST.get("city"), area=request.POST.get("area"), address=request.POST.get("address"), address_type=request.POST.get("address_type"))
            return redirect('accounts:dashboard')
        else:
            context = {
                'form': form,
            }
            return render(request, "accounts/billing_add_form.html",context)

class BillingUpdateView(View):
    def get(self,request,*args, **kwargs):
        billing = get_object_or_404(BillingAddress, id=kwargs['id'])
        context = {
            'billing':billing
        }
        return render(request, "accounts/billing_update.html",context)
    def post(self,request,*args, **kwargs):
        billing = get_object_or_404(BillingAddress, id=kwargs['id'])
        if request.method == "POST":
            user = request.user
            form = BillingForm(request.POST or None, instance=billing)
            if form.is_valid():
                form.save()
                return redirect('accounts:dashboard')


class BillingDeleteView(View):
    def get(self,request,*args, **kwargs):
        billing = get_object_or_404(BillingAddress, id=kwargs['id'])
        billing.delete()
        return redirect("accounts:dashboard")

class ShippingDeleteView(View):
    def get(self,request,*args, **kwargs):
        shipping = get_object_or_404(ShippingAddress, id=kwargs['id'])
        shipping.delete()
        return redirect("accounts:dashboard")