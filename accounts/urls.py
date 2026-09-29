
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('login/', views.login_, name='login'),
    path('signup/', views.signup, name='signup'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='signout'),

    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us', views.AboutUs.as_view(), name='about_us'),
    path('okmessage/', views.OkMessage.as_view(), name='okmessage'),
    path('nomessage/', views.NoMessages.as_view(), name='nomessage'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('verify-forgot-password/',views.verify_forgot_password,name='verify_forgot_password'),
    path('rules_and_questions', views.RulesAndQuestions.as_view(), name='rules_and_questions'),


    ]