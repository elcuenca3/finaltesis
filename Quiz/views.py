import datetime
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from Quiz.sistemafuzzy import sistemaFuzzy
from .forms import RegistroFormulario, UsuarioLoginFormulario
from .models import Carrera, QuizUsuario, Pregunta, PreguntasRespondidas, ElegirRespuesta, Materias, Cuestionarios, QuizUsuario_Cuestionarios
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.serializers import serialize


array = []
sec = 1800
t_pregunta = 0
ultima = 0
pregunta = None
getP = True
bandera = False
nombre_usuario = ''
tiempo_actual = timezone.now()
estado = "completo"
cuestionario_id= 1
puntajet=0


def inicio(request):
    global nombre_usuario
    try:
        QuizUser = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
    except:
        QuizUser= None
        print(QuizUser)
    return render(request, 'inicio.html')


def tablero(request):
    global nombre_usuario
    try:
        QuizUser = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
        n_preguntas = QuizUser.num_p
    except:
        n_preguntas = 0

    total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usaurios_quiz.count()

    context = {
        'user': nombre_usuario,
        'usuario_quiz': total_usaurios_quiz,
        'contar_user': contador
    }

    if n_preguntas >= 20:

        codigo = get_client_ip(request) + '.' + nombre_usuario
        context = {
            'user': nombre_usuario,
            'usuario_quiz': total_usaurios_quiz,
            'contar_user': contador,
            'codigo': 'Su código es: ' + codigo
        }


    return render(request, 'play/tablero.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def resultado(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado.html', context)
def resultado1(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado1.html', context)
def resultado2(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida,


    }
    return render(request, 'play/resultado2.html', context)


def sinTiempo(request):

    return render(request, 'play/sinTiempo.html')


def comentario(request):

    QuizUser = QuizUsuario.objects.get(
        usuario=get_client_ip(request), nombre=nombre_usuario)
    coment = request.POST.get('comentario')

    context = {
        'bandera': False
    }

    if request.method == 'POST':
        QuizUser.guardar_comentario(coment)
        context = {
            'bandera': True,
            'gracias': 'Gracias por tu comentario'
        }

    return render(request, 'comentario.html', context)


def materia(request):
    materias = Materias.objects.all()
    return render(request, 'materia.html', {'materias': materias})


def obtenerCorrecta(pregunta_id, respuesta):

    correcta = respuesta.objects.filter(
        pregunta=pregunta_id, correcta=True).get()

    return correcta

# pruebas


@login_required
def lista_carreras(request):
    carreras = Carrera.objects.all()
    return render(request, 'lista_carreras.html', {'carreras': carreras})


@login_required
def lista_materias(request, id_carrera):
    carrera = get_object_or_404(Carrera, pk=id_carrera)
    materias = Materias.objects.filter(idCarrera=carrera)
    return render(request, 'lista_materias.html', {'materias': materias})


@login_required
def lista_cuestionarios(request, id_materia):
    materia = get_object_or_404(Materias, pk=id_materia)
    cuestionarios = Cuestionarios.objects.filter(idMateria=materia)
    return render(request, 'lista_cuestionarios.html', {'cuestionarios': cuestionarios})


@login_required
def lista_preguntas(request, id_cuestionario):
    global cuestionario_id
    cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
    cuestionario_id = cuestionario.idCuestionario
    preguntas = Pregunta.objects.filter(cuestionario_id=cuestionario)
    print(cuestionario.nombre)
    return render(request, 'lista_preguntas.html', {'cuestionarios': preguntas,'id_cuestionario': cuestionario_id})



# Importa los modelos y vistas necesarios al principio del archivo views.py

# ... (código existente)
# def obtener_nombre_usuario(nombre_usuario):
#     nombre_base = nombre_usuario
#     contador = 1

#     # Verificar si el nombre de usuario ya existe en la base de datos
#     while QuizUsuario.objects.filter(nombre=nombre_usuario).exists():
#         nombre_usuario = f"{nombre_base}_{contador}"
#         contador += 1

#     return nombre_usuario

def completar_cuestionario(quiz_usuario, cuestionario):
    # Agregar un registro a QuizUsuario_Cuestionarios
    tiempo_actual = datetime.now()
    nuevo_registro = QuizUsuario_Cuestionarios.objects.create(
        quiz_quizusuario=quiz_usuario,
        quiz_cuestionarios=cuestionario,
        tiempo=tiempo_actual,
        estado='completado'
    )
    nuevo_registro.save()

def jugar(request, id_cuestionario):
    global array
    global sec
    global t_pregunta
    global ultima
    global getP
    global bandera
    global nombre_usuario
    global pregunta
    global cuestionario_id
    global puntajet

    numlis=20
    # pregunta = Pregunta.objects.filter(cuestionario_id=id_cuestionario)
    

    try:
        quiz_user = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
    except QuizUsuario.DoesNotExist:
        quiz_user = QuizUsuario.objects.filter(
            usuario=get_client_ip(request)).last()
        # nombre_usuario = quiz_user.nombre
    id_cues=id_cuestionario
    if quiz_user.num_p==15:
        print("secumplio")
        getP=True
        print("array",array)

        print("arrayLen",len(array))
        
        # quiz_user.nombre=obtener_nombre_usuario(quiz_user.nombre)
        print(quiz_user.nombre)
        quiz_user.num_p=0
    else:

        print("no se culplio")
    print(pregunta)
    context = {
        'pregunta': pregunta,
        'n_pregunta': quiz_user.num_p+ 1,
        'array': len(array),
        'id_cuestionario' : id_cues,
        'sec': sec,
    }
    if request.GET.get('bandera', False):
        bandera = True
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')
        print(pregunta_pk)
        if respuesta_pk is None:
            return render(request, 'play/jugar.html', context)

        ultima = t_pregunta
        quiz_user.crear_intentos(pregunta)
        pregunta_respondida = quiz_user.intentos.select_related('pregunta').filter(pregunta__pk=pregunta_pk).last()
        # pregunta_respondida = PreguntasRespondidas.objects.filter(
        #     quizUser=quiz_user, pregunta__pk=pregunta_pk).last()

        opcion_seleccionada = ElegirRespuesta.objects.get(pk=respuesta_pk)
        array.append(pregunta_respondida)

        dificultad = pregunta.dificultad

        calificacion = quiz_user.validar_intento(
            pregunta_respondida, opcion_seleccionada, dificultad, bandera, ultima)

        sistemaFuzzy(calificacion, ultima, bandera, dificultad)

        getP = True
        bandera = False
        if id_cues==2:
            return redirect('resultado1', pregunta_respondida.pk)
        if id_cues==3:
            return redirect('resultado2', pregunta_respondida.pk)
        else:
            return redirect('resultado', pregunta_respondida.pk)

    else:
        if len(array) <= 15 and getP:
            pregunta = quiz_user.obtener_nuevas_preguntas(id_cues)
            escri= str(id_cues)
            print("cuestionario",escri)
            if pregunta is None:
                QuizUsuario.objects.get_or_create(
                        usuario= get_client_ip(request), nombre=quiz_user.nombre+escri)
                array = []
                quiz_usuario = QuizUsuario.objects.get(id=quiz_user.id)  # Reemplaza usuario_id por el ID del usuario
                cuestionario = Cuestionarios.objects.get(idCuestionario=id_cues)  # Reemplaza cuestionario_id por el ID del cuestionario
                nueva_entrada = QuizUsuario_Cuestionarios(
                quiz_quizusuario=quiz_usuario,
                quiz_cuestionarios=cuestionario,
                tiempo=tiempo_actual,  # Guardar la hora actual
                estado="Completado",
                )
                nueva_entrada.save()
                return render(request, 'play/jugar.html', {'array': numlis})
            getP = False
        else:
            context = {
                'n_pregunta': quiz_user.num_p + 1,
                'array': len(array),
                'sec': sec,
            }

    try:
        correcta = obtenerCorrecta(pregunta.id, ElegirRespuesta)
        print("correcta",correcta)
    except AttributeError:
        quiz_user = None 
        context = {
            'array': 15
        }
        return render(request, 'play/jugar.html', context)

    context = {
        'pregunta': pregunta,
        'n_pregunta': quiz_user.num_p + 1,
        'array': len(array),
        'sec': sec,
        'correcta': correcta,
    }

    sec = request.GET.get('sec', None)

    if sec is not None:
        t_pregunta = 1800 - int(sec) - ultima

    return render(request, 'play/jugar.html', context)

# login and register


def salir(request):
    global nombre_usuario
    try:
        QuizUser = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
    except:
        QuizUser= None
        print(QuizUser)
    logout(request)
    return redirect('inicio')


def register(request):

    data = {
        'form': RegistroFormulario()
    }

    if request.method == 'POST':
        user_creation_form = RegistroFormulario(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            try:
                QuizUsuario.objects.get_or_create(
                    usuario=get_client_ip(request), nombre=user_creation_form.cleaned_data['username'])
            except:
                context = {
                    'alerta': 'Ingrese otro nombre de usuario'
                }
                return render(request, 'registration/register.html', context)
            return redirect('inicio')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


def mostrar_preguntas(request, idrespueta):
    # Obtener la cadena JSON de preguntas filtradas almacenada en la sesión
    cuestionario = get_object_or_404(Cuestionarios, pk=idrespueta)
    preguntas = ElegirRespuesta.objects.filter(ElegirRespuesta_id=cuestionario)
    preguntas_json = request.session.get('preguntas_filtradas')

    # Convertir la cadena JSON a objetos Python (siempre y cuando sea válido)
    preguntas_filtradas = []
    if preguntas_json:
        preguntas_filtradas = json.loads(preguntas_json)

    # Pasar las preguntas filtradas a la plantilla HTML
    context = {
        'preguntas_filtradas': preguntas_filtradas
    }

    return render(request, 'prueba.html', context)


def mostrar(request, id_cuestionario):
    global array
    global sec
    global t_pregunta
    global ultima
    global getP
    global bandera
    global nombre_usuario
    global pregunta

    cuestionario = get_object_or_404(Cuestionarios, pk=id_cuestionario)
    preguntas = Pregunta.objects.filter(cuestionario_id=cuestionario)
    respuestas = ElegirRespuesta.objects.filter(
        pregunta__cuestionario_id=cuestionario)

    try:
        quiz_user = QuizUsuario.objects.get(
            usuario=get_client_ip(request), nombre=nombre_usuario)
    except QuizUsuario.DoesNotExist:
        quiz_user = QuizUsuario.objects.filter(
            usuario=get_client_ip(request)).last()
        nombre_usuario = quiz_user.nombre
    context = {
        'preguntas': preguntas,
        'respuestas': respuestas,
        'indice_pregunta': 0  # Esto se utilizará para rastrear la pregunta actual
    }
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')

        if respuesta_pk is None:
            return render(request, 'play/jugar.html', context)

        ultima = t_pregunta
        quiz_user.crear_intentos(pregunta)
        pregunta_respondida = PreguntasRespondidas.objects.filter(
            quizUser=quiz_user, pregunta__pk=pregunta_pk).last()

        opcion_seleccionada = ElegirRespuesta.objects.get(pk=respuesta_pk)
        array.append(pregunta_respondida)

        dificultad = pregunta.dificultad

        calificacion = quiz_user.validar_intento(
            pregunta_respondida, opcion_seleccionada, dificultad, bandera, ultima)

        sistemaFuzzy(calificacion, ultima, bandera, dificultad)

        getP = True
        bandera = False

        return redirect('resultado', pregunta_respondida.pk)

    else:
        if len(array) <= 20 and getP:
            pregunta = quiz_user.obtener_nuevas_preguntas()
            if pregunta is None:
                return render(request, 'play/jugar.html', {'array': 20})
            getP = False
        else:
            context = {
                'n_pregunta': quiz_user.num_p + 1,
                'array': len(array),
                'sec': sec,
            }

    return render(request, 'mostrar.html', context)


# graficas
from django.shortcuts import render
from .models import QuizUsuario_Cuestionarios

def mostrar_grafica(request):
    # Obtener los datos de la base de datos
    datos_grafica_pastel = QuizUsuario_Cuestionarios.objects.values_list('quiz_cuestionarios_id', flat=True)
    datos_grafica_pastel = list(datos_grafica_pastel)

    # Realizar algún procesamiento si es necesario para tus datos
    # Puedes realizar algún procesamiento adicional aquí si es necesario

    # Convertir los datos a un formato adecuado para la gráfica (por ejemplo, a JSON)
    datos_grafica_pastel = json.dumps(datos_grafica_pastel)

    context = {
        'datos_grafica_pastel': datos_grafica_pastel
    }
    return render(request, 'mostrar_grafica.html',context)


