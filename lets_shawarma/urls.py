"""
URL configuration for lets_shawarma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('xlogin/', views.xlogin),
    #path('phone_login/', views.phone_login),
    #path('xlogin_otp/', views.xlogin_otp),
    path('xlogout/',views.xlogout),
    path('signup/', views.signup),
    path('menu/', views.menu),
    path('catfilter/<cid>', views.catfilter),
    path('sortby/<sid>', views.sortby),
    path('add_to_platter/', views.add_to_platter),
    path('platter/', views.platter),
    path('otp/', views.otp),
    path('checkout/', views.checkout),
    path('payment_done/', views.payment_done),
    path('orders/', views.home),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)