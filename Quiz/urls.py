from django.urls import path

from .views import (
    inicio,
    jugar,
    sinTiempo,
    tablero,
    sinTiempo,
    resultado,
    resultado1,
    resultado2,
    comentario,
    lista_carreras,
    lista_cuestionarios, lista_materias, lista_preguntas,
    salir,register,mostrar_preguntas,mostrar,mostrar_grafica)

urlpatterns = [

    path('', inicio, name='inicio'),
    path('tablero/', tablero, name='tablero'),
    # path('jugar/', jugar, name='jugar'),
    path('jugar/<int:id_cuestionario>/', jugar, name='jugar'),
    path('sinTiempo/', sinTiempo, name='sinTiempo'),
    path('mostrar_graficas/', mostrar_grafica, name='graficas'),

    path('resultado/<int:pregunta_respondida_pk>', resultado, name='resultado'),
    path('resultado1/<int:pregunta_respondida_pk>', resultado1, name='resultado1'),
    path('resultado2/<int:pregunta_respondida_pk>', resultado2, name='resultado2'),
    path('comentario/', comentario, name='comentario'),
    path('carreras/', lista_carreras, name='lista_carreras'),
    path('materias/<int:id_carrera>/', lista_materias, name='lista_materias'),
    path('cuestionarios/<int:id_materia>/',
            lista_cuestionarios, name='lista_cuestionarios'),
    path('preguntas/<int:id_cuestionario>/',
            lista_preguntas, name='lista_preguntas'),
    path('logout/', salir, name='exit'),
    path('register/', register, name='register'),
    path('prueba/',mostrar_preguntas,name='prueba'),
    path('mostrar/<int:id_cuestionario>/',mostrar, name='mostrar'),
    path('mostrar/<int:id_cuestionario>/',mostrar, name='mostrar'),


]

