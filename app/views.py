from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import * 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from uuid import uuid4
import pdfkit
from django.template.loader import get_template
import os
from .functions import *
from .pdf_manager import _get_pdfkit_config
# from xhtml2pdf import pisa
# from io import BytesIO
from django.conf import settings

# Create your views here.

@login_required(login_url='/login')
def home(request):
    if request.GET.get('q'):
        q = request.GET.get('q') 
        invoices = Invoice.objects.filter(Q(title__icontains=q) | Q(client__clientName__icontains=q) | Q(client__emailAddress__icontains=q))
    else:
        invoices = Invoice.objects.all()
    
    if request.method == 'POST':
        client = ClientForm(request.POST)
        if client.is_valid():
            client.save()

    return render(request, 'app/dashboard.html', {'inv_form':InvoiceForm, 'client_form':ClientSelectForm, 'home':'', 'c_form':ClientForm, 'invoices':invoices})


def loginu(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, "Invalid Credentials")


    return render(request, 'app/login.html', {'form':UserLoginForm})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            if request.POST['password1'] == request.POST['password2']:
                cuser = authenticate(username=request.POST['username'], password=request.POST['password1'])
            else:
                messages.error(request, 'Error!')
            if cuser is not None:
                login(request,cuser)
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, 'Error!')
        else:
                messages.error(request, 'Error!')
            

    return render(request, 'app/signup.html', {'form':UserCreateForm})

@login_required(login_url='/login')
def clients(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    clientobjs = Client.objects.filter(Q(clientName__icontains=q) | Q(emailAddress__icontains=q))
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid:
            form.save()
            print('This is the request.POST', request.POST)
            if 'client' in request.POST:
                return HttpResponseRedirect(reverse('home'))
    return render(request, 'app/clients.html', {'form':ClientForm, 'clients':clientobjs})



@login_required(login_url='/login')
def invoices(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    clientobjs = Invoice.objects.filter(Q(title__icontains=q) | Q(client__clientName__icontains=q) | Q(client__emailAddress__icontains=q))
    invoices = Invoice.objects.all()
    return render(request, 'app/invoices.html', {'invoices':invoices, 'inv_form':InvoiceForm, 'client_form':ClientSelectForm})


def products(request):
    return render(request, 'app/products.html')


@login_required(login_url='/login')
def createInv(request):
    if request.method == 'POST':
        data = request.POST
        try:
            client = Client.objects.get(uniqueId=data['client'])
            inv = Invoice.objects.create(title=data['title'], client=client)
            invobj = inv.save()
            slug = invobj.slug
            return HttpResponseRedirect(reverse('create-inv-build', kwargs={'slug':slug}))
        except:
            messages.error(request, 'Something went wrong!')

    return render(request, 'app/dashboard.html')


@login_required(login_url='/login')
def createInvBuild(request, slug):
    try:
        inv = Invoice.objects.get(slug=slug)
        client = inv.client
    except:
        messages.error(request, "Something went wrong!")
    prod_form = ProductForm
    inv_form = InvoiceForm
    client_form = ClientSelectForm
    cform = ClientForm

    if request.method == 'POST':
        prod = prod_form(request.POST)
        invoice = inv_form(request.POST, instance=inv)
        client = client_form(request.POST)
        clientc = cform(request.POST)
        if prod.is_valid():
            prod = prod.save(commit=False)
            prod.invoice = inv
            prod.save()
            messages.success(request, "Product added!")

        elif client.is_valid():
            try:
                c = Client.objects.get(uniqueId=request.POST['client'])
                inv.client = c
                inv.save()
            except:
                messages.error(request, 'Something went wrong!')

        elif clientc.is_valid():
            try:
                c = cform(request.POST)
                c.save()
            except:
                messages.error(request, 'Something went wrong!')
        
        else:
            messages.error(request, "Invalid info!")


    products = inv.product_set.all()
    client = inv.client
    title = inv.title
    slug = inv.slug
    return render(request, 'app/create-inv-build.html', {'prod_form':prod_form, 'inv_form':inv_form, 'client_form':client_form, 'products':products, 'client':client, 'cform':cform, 'title':title, 'slug':slug})


def viewpdf(request, slug):
    inv = Invoice.objects.get(slug=slug)
    products = inv.product_set.all()
    total = 0.0
    if len(products) > 0:
        for x in products:
            total += x.quantity * x.price
    return render(request, 'app/pdf-template.html', {'invoice':inv, 'invoiceTotal':total, 'products':products})


@login_required(login_url='/login')
def createpdf(request, slug):
    inv = Invoice.objects.get(slug=slug)
    products = inv.product_set.all()
    total = 0.0
    if len(products) > 0:
        for x in products:
            total += x.quantity * x.price

    #The name of your PDF file
    filename = f'{inv.uniqueId}.pdf'

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('app/pdf-template.html')

    #Add any context variables you need to be dynamically rendered in the HTML
    context = {'invoice':inv, 'invoiceTotal':total, 'products':products}

    #Render the HTML
    html = template.render(context)

    # result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')

    #Options - Very Important [Don't forget this]
    options = {
        'encoding': 'UTF-8',
        'javascript-delay':'1000', #Optional
        'enable-local-file-access': None, #To be able to access CSS
        'page-size': 'A4',
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
    }
    #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = _get_pdfkit_config()
    
    css1 = os.path.join(settings.CSS_LOCATION, 'bootstrap.min.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options, css=css1)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response



@login_required(login_url='/login')
def emailpdf(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('create-inv-build', slug=slug)

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    #Calculate the Invoice Total
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y



    context = {'invoice':invoice, 'invoiceTotal':invoiceTotal, 'products':products}

    #The name of your PDF file
    filename = f'{invoice.uniqueId}.pdf'

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('app/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'1000', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = _get_pdfkit_config()

    #Saving the File
    filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = filepath+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)

    print(filepath, pdf_save_path)
    #send the emails to client
    to_email = invoice.client.emailAddress
    from_client = settings.EMAIL_HOST_USER
    title = invoice.title
    try:
        emailInvoiceClient(to_email, from_client, pdf_save_path, title)
    except:
        messages.error(request, 'Something went wrong!')
        return redirect('create-inv-build', slug=slug)

    invoice.save()

    #Email was send, redirect back to view - invoice
    messages.success(request, f"Email sent to {invoice.client.clientName} succesfully")
    if os.path.exists(pdf_save_path):
        os.remove(pdf_save_path)

    return redirect('invoices')


@login_required(login_url='/login')
def deletepdf(request, slug):
    inv = Invoice.objects.get(slug=slug)
    inv.delete()
    return redirect('invoices')


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



    



