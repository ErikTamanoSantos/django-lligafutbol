from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CrearEquipForm

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

class CrearLligaForm(forms.Form):
    nom = forms.CharField(max_length=100)

def crearLliga(request):
    form = CrearLligaForm()
    if request.method == "POST":
        form = CrearLligaForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get("nom")
            valid = True
            
            if Lliga.objects.filter(nom=nom).exists():
                form.errors["nom"] = ["Aquesta lliga ja existeix!"]
                valid = False
            
            if valid:
                lliga = Lliga(nom=nom)
                lliga.save()
                return redirect('menu')
            
    return render(request, "crearLliga.html",{
                    "form": form,
            })

def crearEquip(request):
    if request.method == 'POST':
        form = CrearEquipForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get("nom")
            valid = True
            
            if Equip.objects.filter(nom=nom).exists():
                form.errors["nom"] = ["Aquest equip ja existeix!"]
                valid = False
            
            if valid:
                form.save()
                return redirect('menu')
    else:
        form = CrearEquipForm()
    return render(request, 'crearEquip.html', {'form': form})

class MenuEquipForm(forms.Form):
    equip = forms.ModelChoiceField(queryset=Equip.objects.all())
    
def menuEquip(request):
    form = MenuEquipForm()
    if request.method == "POST":
        form = MenuEquipForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def editarEquipos(request):
    return render(request, "edita_equip_ajax.html")

@login_required
def profile(request):
    user = request.user
    return HttpResponse("Profile: " + user.username + "<br> Nom "+ user.first_name + "<br> Cognom " + user.last_name + "<br> Email " + user.email)

def index(request):
    return render(request, 'index.html')

def classificacio(request, lliga_id):
    lliga = get_object_or_404(Lliga, pk=lliga_id)
    equips = lliga.equip_set.all()
    classi = []
 
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nom) )
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga,
                })