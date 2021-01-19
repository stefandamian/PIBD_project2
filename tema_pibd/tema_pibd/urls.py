"""tema_pibd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from scoala.views import home_view,\
    elevi_view, show_elev_view, add_elev_view, modify_elev_view, add_aranjament_to_elev_view, del_aranjament_to_elev_view,\
    discipline_view, show_disciplina_view, add_disciplina_view, modify_disciplina_view, add_aranjament_to_disciplina_view, del_aranjament_to_disciplina_view,\
    profesori_view, show_profesor_view, add_profesor_view, modify_profesor_view, add_disciplina_to_profesor_view, del_disciplina_to_profesor_view,\
    aranjamente_view, add_aranjament_view, del_aranjament_view, modify_aranjament_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('home/', home_view, name="home"),

    path('elevi/', elevi_view, name="elevi"),
    path('elev/<int:id>', show_elev_view, name="elev"),
    path('elev/add', add_elev_view, name="add_elev"),
    path('elev/<int:id>/modify', modify_elev_view, name="modify_elev"),
    path('elev/<int:id>/add_aranjament', add_aranjament_to_elev_view, name="add_aranjament_to_elev"),
    path('elev/<int:id>/del_aranjament', del_aranjament_to_elev_view, name="del_aranjament_to_elev"),

    path('discipline/', discipline_view, name="discipline"),
    path('disciplina/<int:id>', show_disciplina_view, name="disciplina"),
    path('disciplina/add', add_disciplina_view, name="add_disciplina"),
    path('disciplina/<int:id>/modify', modify_disciplina_view, name="modify_disciplina"),
    path('disciplina/<int:id>/add_aranjament', add_aranjament_to_disciplina_view, name="add_aranjament_to_disciplina"),
    path('disciplina/<int:id>/del_aranjament', del_aranjament_to_disciplina_view, name="del_aranjament_to_disciplina"),

    path('profesori/', profesori_view, name="profesori"),
    path('profesor/<int:id>', show_profesor_view, name="profesor"),
    path('profesor/add', add_profesor_view, name="add_profesor"),
    path('profesor/<int:id>/modify', modify_profesor_view, name="modify_profesor"),
    path('profesor/<int:id>/add_disciplina', add_disciplina_to_profesor_view, name="add_disciplina_to_profesor"),
    path('profesor/<int:id>/del_disciplina', del_disciplina_to_profesor_view, name="del_disciplina_to_profesor"),

    path('aranjamente/', aranjamente_view, name="aranjamente"),
    path('aranjament/add', add_aranjament_view, name="add_aranjament"),
    path('aranjament/del', del_aranjament_view, name="del_aranjament"),
    path('aranjament/iddisciplina=<int:iddisciplina>&idelev=<int:idelev>/modify', modify_aranjament_view, name="modify_aranjament")

]
