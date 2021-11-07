from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "accounts"

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('shipping', views.ShippingView.as_view(), name='shipping'),
    path('shipping_update/<int:id>', views.ShippingUpdateView.as_view(), name='shipping_update'),
    path('shipping_delete/<int:id>', views.ShippingDeleteView.as_view(), name='shipping_delete'),
    path('billing', views.BillingView.as_view(), name='billing'),
    path('billing_update/<int:id>', views.BillingUpdateView.as_view(), name='billing_update'),
    path('billing_delete/<int:id>', views.BillingDeleteView.as_view(), name='billing_delete'),
    
    #login register
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    #token
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html' , success_url=reverse_lazy('accounts:password_change_done')), name='change_password'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html' , success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html' , success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
