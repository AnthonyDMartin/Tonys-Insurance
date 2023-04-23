from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from pojisteni import models as MODELY
from pojisteni import forms as FORMY
from django.contrib.auth.models import User


def uvitani_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'pojistenec/uvitani.html')


def registrace_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'pojistenec/registrace.html',context=mydict)


def je_pojistenec(user):
    return user.groups.filter(name='CUSTOMER').exists()


@login_required(login_url='customerlogin')
def pojistenec_profil_view(request):
    dict = {
        'pojistenec': models.Customer.objects.get(user_id=request.user.id),
        'dostupne_smlouvy': MODELY.Policy.objects.all().count(),
        'zadosti': MODELY.PolicyRecord.objects.all().filter(
            customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'celkem_dotazu': MODELY.Question.objects.all().filter(
            customer=models.Customer.objects.get(user_id=request.user.id)).count(),

    }
    return render(request, 'pojistenec/pojistenec_profil.html', context=dict)


def aktualizace_udaju_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = MODELY.User.objects.get(id=customer.user_id)
    userForm = FORMY.CustomerUserForm(instance=user)
    customerForm = FORMY.CustomerForm(instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = FORMY.CustomerUserForm(request.POST, instance=user)
        customerForm = FORMY.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('pojistenec_profil')
    return render(request, 'pojistenec/aktualizace_udaju.html', context=mydict)


def zadost_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = MODELY.Policy.objects.all()
    return render(request, 'pojistenec/zadost.html', {'policies': policies, 'pojistenec': customer})


def zazadat_view(request, pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = MODELY.Policy.objects.get(id=pk)
    policyrecord = MODELY.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('archiv')


def archiv_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = MODELY.PolicyRecord.objects.all().filter(customer=customer)
    return render(request, 'pojistenec/archiv.html', {'policies': policies, 'pojistenec': customer})


def poslat_dotaz_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm = FORMY.QuestionForm()

    if request.method == 'POST':
        questionForm = FORMY.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect('archiv-dotazu')
    return render(request, 'pojistenec/poslat_dotaz.html', {'questionForm': questionForm, 'pojistenec': customer})


def archiv_dotazu_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = MODELY.Question.objects.all().filter(customer=customer)
    return render(request, 'pojistenec/archiv_dotazu.html', {'questions': questions, 'pojistenec': customer})
