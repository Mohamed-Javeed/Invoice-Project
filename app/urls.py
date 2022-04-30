from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login', loginu, name="login"),
    path('signup', signup, name="signup"),
    path('clients', clients, name="clients"),
    path('create-inv', createInv, name="create-inv"),
    path('create-inv-build/<str:slug>', createInvBuild, name="create-inv-build"),
    path('invoices', invoices, name="invoices"),
    path('products', products, name="products"),
    path('viewpdf/<str:slug>', viewpdf, name="viewpdf"),
    path('createpdf/<str:slug>', createpdf, name="createpdf"),
    path('emailpdf/<str:slug>', emailpdf, name="emailpdf"),
    path('signout', signout, name="signout"),
    path('delete/<str:slug>', deletepdf, name="deletepdf")

]