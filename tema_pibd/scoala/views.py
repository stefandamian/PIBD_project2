from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import math

from .models import Elev, Profesor, Disciplina, Aranjament

# Create your views here.

def home_view(request):
    context = {"title":"Home"
               }
    return render(request, "index.html", context)

    '''elevi'''

def elevi_view(request):
    context = {"title": "Elevi",
               "elevi": Elev.objects.all()
               }
    return render(request, "lista_elevi.html", context)

def show_elev_view(request, id):
    iduri=[]
    for id_dis, id_elev in Aranjament.all():
        if id_elev == id:
            iduri.append(id_dis)
    discipline = [Disciplina.objects.get(iddisciplina=id) for id in iduri]

    context = {"title": "Vizualizare Elev",
               "elev": Elev.objects.get(idelev=id),
               "discipline": discipline
    }
    return render(request, "vizualizare_elev.html", context)

def add_elev_view(request):
    valid_entry = request.POST.get("nume") != "" and request.POST.get("prenume") != ""
    if request.method == "POST" and valid_entry:
        elev = Elev.objects.create(nume=request.POST.get("nume"),
                                   prenume=request.POST.get("prenume"),
                                   an=request.POST.get("an"))
        return HttpResponseRedirect(f'/elev/{elev.idelev}')
    else:
        context = {"title": "Adaugare Elev",
                   "id": 0,
                   "nume": "",
                   "prenume": "",
                   "an": 0,
                   "ani": range(1, 5),
                   "modificare": False
        }

        return render(request, "modificare_elev.html", context)

def modify_elev_view(request, id):
    elev = Elev.objects.get(idelev=id)
    valid_entry = request.POST.get("nume") != "" and  request.POST.get("prenume") != ""
    if request.method == "POST" and valid_entry:
        if request.POST.get("stergere") == "True":
            elev.delete()
            return HttpResponseRedirect('/elevi')
        else:
            elev.nume = request.POST.get("nume")
            elev.prenume = request.POST.get("prenume")
            elev.an = request.POST.get("an")
            elev.save()
            return HttpResponseRedirect(f'/elev/{elev.idelev}')
    else:
        context = {"title": "Modificare Elev",
                   "id": elev.idelev,
                   "nume": elev.nume,
                   "prenume": elev.prenume,
                   "an": elev.an,
                   "ani": range(1, 5),
                   "modificare": True
        }

        return render(request, "modificare_elev.html", context)

def add_aranjament_to_elev_view(request, id):
    ids_discipline = request.POST.getlist("iddisciplina")
    if request.method == "POST" and ids_discipline:
        for id_disciplina in ids_discipline:
            Aranjament.add(int(id_disciplina), id)
        return HttpResponseRedirect(f'/elev/{id}')
    else:
        iduri = []
        for id_dis, id_elev in Aranjament.all():
            if id_elev == id:
                iduri.append(str(id_dis))
        print(",".join(iduri))
        discipline = Disciplina.objects.raw("select * from discipline where iddisciplina not in (" + ",".join(iduri) + ");") if len(iduri) > 0 else Disciplina.objects.all()
        context = {"title": "Adaugare Aranjament Disciplina-Elev",
                   "elev": Elev.objects.get(idelev=id),
                   "discipline_disponibile": discipline,
                   "add": True
                   }
        return render(request, "adaugare_aranjament_disciplina-elev.html", context)

def del_aranjament_to_elev_view(request, id):
    ids_discipline = request.POST.getlist("iddisciplina")
    if request.method == "POST" and ids_discipline:
        for id_disciplina in ids_discipline:
            Aranjament.delete(int(id_disciplina), id)
        return HttpResponseRedirect(f'/elev/{id}')
    else:
        iduri = []
        for id_dis, id_elev in Aranjament.all():
            if id_elev == id:
                iduri.append(id_dis)
        discipline = [Disciplina.objects.get(iddisciplina=id) for id in iduri]
        context = {"title": "Stergere Aranjament Disciplina-Elev",
                   "elev": Elev.objects.get(idelev=id),
                   "discipline_disponibile": discipline,
                   "add": False
                   }
        return render(request, "adaugare_aranjament_disciplina-elev.html", context)

    '''discipline'''

def discipline_view(request):
    context = {"title": "Discipline",
               "discipline": Disciplina.objects.all(),
               "nr_elevi": [sum([1 if arj[0] == disciplina.iddisciplina else 0 for arj in Aranjament.all()]) for disciplina in Disciplina.objects.all()]
               }
    return render(request, "lista_discipline.html", context)

def show_disciplina_view(request, id):
    iduri = []
    for id_dis, id_elev in Aranjament.all():
        if id_dis == id:
            iduri.append(id_elev)
    elevi = [Elev.objects.get(idelev=id) for id in iduri]

    context = {"title": "Vizualizare Profesor",
               "disciplina": Disciplina.objects.get(iddisciplina=id),
               "elevi": elevi
    }
    return render(request, "vizualizare_disciplina.html", context)

def add_disciplina_view(request):
    valid_entry = request.POST.get("nume") != ""
    if request.method == "POST" and valid_entry:
        profesor = Profesor.objects.get(idprofesor=int(request.POST.get("idprofesor")))
        disciplina = Disciplina.objects.create(nume=request.POST.get("nume"),
                                               profesor=profesor)
        return HttpResponseRedirect(f'/disciplina/{disciplina.iddisciplina}')
    else:
        context = {"title": "Adaugare Disciplina",
                   "id": 0,
                   "nume": "",
                   "idprofesor": 0,
                   "profesori": Profesor.objects.all(),
                   "modificare": False
        }

        return render(request, "modificare_disciplina.html", context)

def modify_disciplina_view(request, id):
    disciplina = Disciplina.objects.get(iddisciplina=id)
    valid_entry = request.POST.get("nume") != ""
    if request.method == "POST" and valid_entry:
        if request.POST.get("stergere") == "True":
            disciplina.delete()
            return HttpResponseRedirect('/discipline')
        else:
            disciplina.nume = request.POST.get("nume")
            disciplina.profesor = Profesor.objects.get(idprofesor=request.POST.get("idprofesor"))
            disciplina.save()
            return HttpResponseRedirect(f'/disciplina/{disciplina.iddisciplina}')
    else:
        context = {"title": "Modificare Elev",
                   "id": disciplina.iddisciplina,
                   "nume": disciplina.nume,
                   "idprofesor": disciplina.profesor.idprofesor,
                   "profesori": Profesor.objects.all(),
                   "modificare": True
        }

        return render(request, "modificare_disciplina.html", context)

def add_aranjament_to_disciplina_view(request, id):
    ids_elevi = request.POST.getlist("idelev")
    if request.method == "POST" and ids_elevi:
        for id_elev in ids_elevi:
            Aranjament.add(id, int(id_elev))
        return HttpResponseRedirect(f'/disciplina/{id}')
    else:
        iduri = []
        for id_dis, id_elev in Aranjament.all():
            if id_dis == id:
                iduri.append(str(id_elev))
        print(",".join(iduri))
        elevi = Elev.objects.raw("select * from elevi where idelev not in (" + ",".join(iduri) + ");") if len(iduri) > 0 else Elev.objects.all()
        context = {"title": "Adaugare Aranjament Elev-Disciplina",
                   "disciplina": Disciplina.objects.get(iddisciplina=id),
                   "elevi_disponibili": elevi,
                   "add": True
                   }
        return render(request, "adaugare_aranjament_elev-disciplina.html", context)

def del_aranjament_to_disciplina_view(request, id):
    ids_elevi = request.POST.getlist("idelev")
    if request.method == "POST" and ids_elevi:
        for id_elev in ids_elevi:
            Aranjament.delete(id, int(id_elev))
        return HttpResponseRedirect(f'/disciplina/{id}')
    else:
        iduri = []
        for id_dis, id_elev in Aranjament.all():
            if id_dis == id:
                iduri.append(id_elev)
        elevi = [Elev.objects.get(idelev=id) for id in iduri]
        context = {"title": "Stergere Aranjament Elev-Disciplina",
                   "disciplina": Disciplina.objects.get(iddisciplina=id),
                   "elevi_disponibili": elevi,
                   "add": False
                   }
        return render(request, "adaugare_aranjament_elev-disciplina.html", context)

    '''profesori'''

def profesori_view(request):
    context = {"title": "Profesori",
               "profesori": Profesor.objects.all(),
               "nr_discipline": [sum([1 if dis.profesor.idprofesor == prof.idprofesor else 0 for dis in Disciplina.objects.all()]) for prof in Profesor.objects.all()]
               }
    return render(request, "lista_profesori.html", context)

def show_profesor_view(request, id):
    discipline = Disciplina.objects.raw(f"select * from discipline where idprofesor = {id};")
    context = {"title": "Vizualizare Profesor",
               "profesor": Profesor.objects.get(idprofesor=id),
               "discipline": discipline,
               "nr_elevi": [sum([1 if arj[0] == disciplina.iddisciplina else 0 for arj in Aranjament.all()]) for disciplina in discipline]
    }
    return render(request, "vizualizare_profesor.html", context)

def add_profesor_view(request):
    valid_entry = request.POST.get("nume") != "" and request.POST.get("prenume") != ""
    if request.method == "POST" and valid_entry:
        profesor = Profesor.objects.create(nume=request.POST.get("nume"),
                                   prenume=request.POST.get("prenume"))
        return HttpResponseRedirect(f'/profesor/{profesor.idprofesor}')
    else:
        context = {"title": "Adaugare Profesor",
                   "nume": "",
                   "prenume": "",
                   "modificare": False
        }

        return render(request, "modificare_profesor.html", context)

def modify_profesor_view(request, id):
    profesor = Profesor.objects.get(idprofesor=id)
    valid_entry = request.POST.get("nume") != "" and  request.POST.get("prenume") != ""
    if request.method == "POST" and valid_entry:
        if request.POST.get("stergere") == "True":
            profesor.delete()
            return HttpResponseRedirect('/profesori')
        else:
            profesor.nume = request.POST.get("nume")
            profesor.prenume = request.POST.get("prenume")
            profesor.save()
            return HttpResponseRedirect(f'/profesor/{profesor.idprofesor}')
    else:
        context = {"title": "Modificare Profesor",
                   "nume": profesor.nume,
                   "prenume": profesor.prenume,
                   "modificare": True
        }

        return render(request, "modificare_profesor.html", context)

def add_disciplina_to_profesor_view(request, id):
    profesor = Profesor.objects.get(idprofesor=id)
    nume_disciplina = request.POST.get("numeDisciplina")
    if request.method == "POST" and nume_disciplina:
        Disciplina.objects.create(nume=nume_disciplina, profesor=profesor)
        return HttpResponseRedirect(f'/profesor/{id}')
    else:
        context = {"title": "Adaugare Disciplina pentru Profesor",
                   "profesor": profesor
                   }
        return render(request, "adaugare_disciplina-profesor.html", context)

def del_disciplina_to_profesor_view(request, id):
    ids_discipline = request.POST.getlist("idDiscipline")
    if request.method == "POST" and ids_discipline:
        for id_disciplina in ids_discipline:
            Disciplina.objects.get(iddisciplina=id_disciplina).delete()
        return HttpResponseRedirect(f'/profesor/{id}')
    else:
        context = {"title": "Stergere Disciplina pentru Profesor",
                   "profesor": Profesor.objects.get(idprofesor=id),
                   "discipline": Disciplina.objects.raw(f"select * from discipline where idprofesor = {id};")
                   }
        return render(request, "stergere_disciplina-profesor.html", context)

    '''aranjamente'''

def aranjamente_view(request):
    context = {"title": "Aranjamente",
               "aranjamente": Aranjament.all(),
               "elevi": [Elev.objects.get(idelev=arj[1]) for arj in Aranjament.all()],
               "discipline": [Disciplina.objects.get(iddisciplina=arj[0]) for arj in Aranjament.all()]
               }
    return render(request, "lista_aranjamente.html", context)

def add_aranjament_view(request):
    fail = False
    if request.method == "POST":
        idelev = int(request.POST.get("idelev"))
        iddisciplina = int(request.POST.get("iddisciplina"))
        if not Aranjament.exist(iddisciplina=iddisciplina, idelev=idelev):
            Aranjament.add(iddisciplina=iddisciplina, idelev=idelev)
            return HttpResponseRedirect('/aranjamente')
        else:
            fail = True

    context = {"title": "Adaugare Aranjament",
               "idelev": 0,
               "iddisciplina": 0,
               "elevi": Elev.objects.all(),
               "discipline": Disciplina.objects.all(),
               "fail": fail
               }
    return render(request, "modificare_aranjament.html", context)

def modify_aranjament_view(request, iddisciplina, idelev):
    fail = False
    if request.method == "POST":
        idelev_new = int(request.POST.get("idelev"))
        iddisciplina_new = int(request.POST.get("iddisciplina"))
        if not Aranjament.exist(iddisciplina=iddisciplina_new, idelev=idelev_new):
            Aranjament.modify(iddisciplina_old=iddisciplina, idelev_old=idelev,
                              iddisciplina_new=iddisciplina_new, idelev_new=idelev_new)
            return HttpResponseRedirect('/aranjamente')
        else:
            fail = True

    context = {"title": "Modificare Aranjament",
               "idelev": idelev,
               "iddisciplina": iddisciplina,
               "elevi": Elev.objects.all(),
               "discipline": Disciplina.objects.all(),
               "fail": fail
               }
    return render(request, "modificare_aranjament.html", context)

def del_aranjament_view(request):
    if request.method == "POST":
        ids_zipped = request.POST.getlist("iddisciplina_idelev")
        for ids in ids_zipped:
            ids = ids.split("_")
            print(ids)
            Aranjament.delete(iddisciplina=int(ids[0]), idelev=int(ids[1]))
        if len(ids_zipped) > 0 :
            return HttpResponseRedirect('/aranjamente')

    context = {"title": "Stergere Aranjamente",
               "aranjamente": Aranjament.all(),
               "elevi": [Elev.objects.get(idelev=id_elev) for id_dis, id_elev in Aranjament.all()],
               "discipline": [Disciplina.objects.get(iddisciplina=id_dis) for id_dis, id_elev in Aranjament.all()],
               }
    return render(request, "stergere_aranjamente.html", context)