from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ClientForm(ModelForm):
    clientName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}), required=True)
    phoneNumber = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}))
    emailAddress = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}))
    class Meta:
        model = Client
        fields = ['clientName', 'phoneNumber', 'emailAddress']



class ProductForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}))

    class Meta:
        model = Product
        fields = ['invoice', 'title', 'quantity', 'price']



class InvoiceForm(ModelForm):
    # client = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-control mb-3'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'id':'floatingInput'}))
    class Meta:
        model = Invoice
        fields = ['client', 'title']

    def save(self, *args, **kwargs):
        super(InvoiceForm, self).save(*args, **kwargs)
        return self


class ClientSelectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.choice_list = Client.objects.all()
        self.choices = [('-------', '---Select a Client---')]

        for c in self.choice_list:
            d_t = (c.uniqueId, c.clientName)
            self.choices.append(d_t)

        super(ClientSelectForm, self).__init__(*args, **kwargs)

        self.fields['client'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control mb-3'}), label='', choices=self.choices)

    class Meta:
        model = Invoice
        fields = ['client']

    def clean_client(self):
        c_client = self.cleaned_data['client']
        if c_client == '-------':
            return None
        else:
            return Client.objects.get(uniqueId=c_client)


class UserLoginForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':"floatingInput", 'class':"form-control mb-3"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':"floatingPassword", 'class':"form-control mb-3"}), required=True)
    class Meta:
        model = User
        fields = ['username', 'password']


class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'id':'floatingInput'}), required=True)
    password1 = password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'id':'floatingPassword'}), required=True)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

