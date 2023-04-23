from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from pojistenec import models as MODELY
from pojistenec import forms as FORMY


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'pojisteni/index.html')


def je_pojistenec(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if je_pojistenec(request.user):
        return redirect('pojistenec/pojistenec-profil')
    else:
        return redirect('admin-sprava-pojisteni')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_sprava_pojisteni_view(request):
    dict = {
        'celkem_pojistencu': MODELY.Customer.objects.all().count(),
        'celken_smluv': models.Policy.objects.all().count(),
        'celkem_druhu': models.Category.objects.all().count(),
        'celkem_dotazu': models.Question.objects.all().count(),
        'celkem_navrhu': models.PolicyRecord.objects.all().count(),
        'schvalene_navrhy': models.PolicyRecord.objects.all().filter(status='Schváleno').count(),
        'zamitnute_navrhy': models.PolicyRecord.objects.all().filter(status='Zamítnuto').count(),
        'cekajici_navrhy': models.PolicyRecord.objects.all().filter(status='Čeká na schválení').count(),
    }
    return render(request, 'pojisteni/admin_sprava_pojisteni.html', context=dict)


@login_required(login_url='adminlogin')
def pojistenci_view(request):
    customers = MODELY.Customer.objects.all()
    return render(request, 'pojisteni/pojistenci.html', {'customers': customers})


@login_required(login_url='adminlogin')
def pridat_pojistence_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('pojistenci')
    return render(request, 'pojisteni/pridat_pojistence.html', context=mydict)


@login_required(login_url='adminlogin')
def aktualizace_pojistence_view(request, pk):
    customer = MODELY.Customer.objects.get(id=pk)
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
            return redirect('pojistenci')
    return render(request, 'pojisteni/aktualizace_pojistence.html', context=mydict)


@login_required(login_url='adminlogin')
def odstraneni_pojistence_view(request, pk):
    customer = MODELY.Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/pojistenci')


def pridat_druh_pojisteni_view(request):
    categoryForm = forms.CategoryForm()
    if request.method == 'POST':
        categoryForm = forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('druhy-pojisteni')
    return render(request, 'pojisteni/pridat_druh_pojisteni.html', {'categoryForm': categoryForm})


def druhy_pojisteni_view(request):
    categories = models.Category.objects.all()
    return render(request, 'pojisteni/druhy_pojisteni.html', {'categories': categories})


def smazat_druh_pojisteni_view(request, pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('druhy-pojisteni')


@login_required(login_url='adminlogin')
def zmenit_nazev_pojisteni_view(request, pk):
    category = models.Category.objects.get(id=pk)
    categoryForm = forms.CategoryForm(instance=category)

    if request.method == 'POST':
        categoryForm = forms.CategoryForm(request.POST, instance=category)

        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('druhy-pojisteni')
    return render(request, 'pojisteni/zmenit_nazev_pojisteni.html', {'categoryForm': categoryForm})


def pridat_smlouvu_view(request):
    policyForm = forms.PolicyForm()

    if request.method == 'POST':
        policyForm = forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)

            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()
            return redirect('smlouvy')
    return render(request, 'pojisteni/pridat_smlouvu.html', {'policyForm': policyForm})


def smlouvy_view(request):
    policies = models.Policy.objects.all()
    return render(request, 'pojisteni/smlouvy.html', {'policies': policies})


def admin_aktualizace_smlouvy_view(request):
    policies = models.Policy.objects.all()
    return render(request, 'pojisteni/admin_aktualizace_smlouvy.html', {'policies': policies})


@login_required(login_url='adminlogin')
def aktualizace_smlouvy_view(request, pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm = forms.PolicyForm(instance=policy)

    if request.method == 'POST':
        policyForm = forms.PolicyForm(request.POST, instance=policy)

        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)

            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()

            return redirect('admin-aktualizace-smlouvy')
    return render(request, 'pojisteni/aktualizace_smlouvy.html', {'policyForm': policyForm})


def zruseni_smlouvy_view(request):
    policies = models.Policy.objects.all()
    return render(request, 'pojisteni/zruseni_smlouvy.html', {'policies': policies})


def smazat_smlouvu_view(request, pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('zruseni-smlouvy')


def zobrazeni_navrhu_smluv_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request, 'pojisteni/zobrazeni_navrhu_smluv.html', {'policyrecords': policyrecords})


def schvalene_navrhy_smluv_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Schváleno')
    return render(request, 'pojisteni/schvalene_navrhy_smluv.html', {'policyrecords': policyrecords})


def zamitnute_navrhy_smluv_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Zamítnuto')
    return render(request, 'pojisteni/zamitnute_navrhy_smluv.html', {'policyrecords': policyrecords})


def cekajici_navrhy_smluv_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Čeká na schválení')
    return render(request, 'pojisteni/cekajici_navrhy_smluv.html', {'policyrecords': policyrecords})


def schvalit_view(request, pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status = 'Schváleno'
    policyrecords.save()
    return redirect('zobrazeni-navrhu-smluv')


def zamitnout_view(request, pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status = 'Zamítnuto'
    policyrecords.save()
    return redirect('zobrazeni-navrhu-smluv')


def dotazy_view(request):
    questions = models.Question.objects.all()
    return render(request, 'pojisteni/dotazy.html', {'questions': questions})


def odpovedet_view(request, pk):
    question = models.Question.objects.get(id=pk)
    questionForm = forms.QuestionForm(instance=question)

    if request.method == 'POST':
        questionForm = forms.QuestionForm(request.POST, instance=question)

        if questionForm.is_valid():
            admin_comment = request.POST.get('admin_comment')

            question = questionForm.save(commit=False)
            question.admin_comment = admin_comment
            question.save()

            return redirect('dotazy')
    return render(request, 'pojisteni/odpovedet.html', {'questionForm': questionForm})


def smazat_dotaz_view(request, pk):
    question = models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/dotazy')


def o_nas_view(request):
    return render(request, 'pojisteni/o_nas.html')


def kontakt_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'pojisteni/odeslano.html')
    return render(request, 'pojisteni/kontakt.html', {'form': sub})
