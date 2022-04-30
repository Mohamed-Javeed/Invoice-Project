from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User
from django.urls import reverse


class Client(models.Model):
    clientName = models.CharField(max_length=225)
    phoneNumber = models.IntegerField(null=True)
    emailAddress = models.EmailField(null=True)
    uniqueId = models.CharField(null=True, max_length=100,blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.clientName} {self.emailAddress} {self.uniqueId}'

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify(f'{self.clientName} {self.emailAddress} {self.uniqueId}')
            self.lastUpdated = timezone.localtime(timezone.now())

            super(Client, self).save(*args, **kwargs)


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    uniqueId = models.CharField(null=True, max_length=100,blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.uniqueId}'

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify(f'{self.title} {self.uniqueId}')
            self.lastUpdated = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)
        return self


    
class Product(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    uniqueId = models.CharField(null=True, max_length=100,blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.uniqueId}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify(f'{self.title} {self.uniqueId}')
            self.lastUpdated = timezone.localtime(timezone.now())

            super(Product, self).save(*args, **kwargs)    
