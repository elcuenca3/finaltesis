from django.db import models


from .sistemafuzzy import obtener_dif_pregunta

import random


class Carrera(models.Model):
    idCarrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Materias(models.Model):
    idMateria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ciclo = models.IntegerField(null=False)
    idCarrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.idMateria} - {self.nombre}"


class Cuestionarios(models.Model):
    idCuestionario = models.AutoField(primary_key=True,unique=True)
    nombre = models.CharField(max_length=100)
    idMateria = models.ForeignKey(Materias, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Pregunta(models.Model):

	NUMER_DE_RESPUESTAS_PERMITIDAS = 1

	texto = models.TextField(verbose_name='Texto de la pregunta')
	dificultad = models.IntegerField(verbose_name='Dificultad pregunta', null=True)
	max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)
	tipo = models.TextField(verbose_name='Tipo de pregunta')
	unidad = models.IntegerField(verbose_name='Unidad a la que pertenece')
	cuestionario_id = models.ForeignKey(Cuestionarios,on_delete=models.CASCADE,verbose_name='Cuestionario')
	def __str__(self):
		return self.texto


class ElegirRespuesta(models.Model):

	MAXIMO_RESPUESTA = 3
	MINIMO_RESPUESTA = 2

	pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
	correcta = models.BooleanField(verbose_name='¿Es esta la pregunta correcta?', default=False)
	texto = models.TextField(verbose_name='Texto de la respuesta')

	def __str__(self):
		return self.texto

class  QuizUsuario(models.Model):
	usuario = models.TextField(verbose_name='Ip usuario')
	nombre = models.TextField(verbose_name='Nombre del usuario', null=True)
	puntaje_total = models.DecimalField(verbose_name='Puntaje Total', null=True, default=0.00, decimal_places=2, max_digits=10)
	num_p = models.IntegerField(verbose_name='Numero de  preguntas respondidas', default=0)
	totalpuntaje = models.DecimalField(verbose_name='total_pregunta',null=True, default=0.00, decimal_places=2, max_digits=10)

	def crear_intentos(self, pregunta):
		intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self, nombreUser=self)
		intento.save()

	def getNumP(self):
		respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
		return len(respondidas) + 1

	def obtener_nuevas_preguntas(self,id_cuestionario):

		dif = obtener_dif_pregunta()
		print("dif",dif)
		respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
		preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas, cuestionario_id=id_cuestionario)
		print("respondidas",respondidas)
		if len(respondidas) >= 15:
				return None
		
		try:

			return random.choice(preguntas_restantes.filter(dificultad=dif,cuestionario_id=id_cuestionario))
		except IndexError:
			print('obt fallo')
			print(random.choice(preguntas_restantes))
			return random.choice(preguntas_restantes.filter(cuestionario_id=id_cuestionario))

	def validar_intento(self, pregunta_respondida, respuesta_selecionada, dificultad, ayuda, tiempo):

		


		if respuesta_selecionada.correcta is True:
			pregunta_respondida.correcta = True
			pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
			pregunta_respondida.respuesta = respuesta_selecionada
			pregunta_respondida.dificultad = dificultad
			pregunta_respondida.uso_ayuda = ayuda
			calificacion = 1
			pregunta_respondida.tiempo_pregunta = tiempo

		else:
			pregunta_respondida.respuesta = respuesta_selecionada
			pregunta_respondida.dificultad = dificultad
			pregunta_respondida.uso_ayuda = ayuda
			calificacion = 0
			pregunta_respondida.tiempo_pregunta = tiempo

		self.totalpuntaje+= dificultad
		self.save()
		self.num_p += 1
		self.save()
		pregunta_respondida.save()

		self.actualizar_puntaje()

		return calificacion

	def actualizar_puntaje(self):
		puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(
			models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
	
		print('dificultad',PreguntasRespondidas.dificultad)
		

		self.puntaje_total = puntaje_actualizado
		self.save()

	def guardar_comentario(self, texto_comentario):
		comentario = ComentarioUsuario(comentario=texto_comentario, quizUser=self, nombreUser=self)
		comentario.save()

class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    nombreUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos_username', null=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    dificultad = models.IntegerField(verbose_name='Dificultad de la pregunta', null=True)
    uso_ayuda = models.BooleanField(verbose_name='¿Utilizo ayuda?', default=False)
    tiempo_pregunta = models.IntegerField(verbose_name='Tiempo de la pregunta', null=True)
    correcta = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)




class ComentarioUsuario(models.Model):
	quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='comentario')
	nombreUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='comentario_username', null=True)
	comentario = models.TextField(verbose_name='Comentario')

class QuizUsuario_Cuestionarios(models.Model):
    quiz_quizusuario = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE)
    quiz_cuestionarios = models.ForeignKey(Cuestionarios, on_delete=models.CASCADE)
    tiempo = models.DateField()
    estado = models.CharField(max_length=45)

    class Meta:
        unique_together = (('quiz_quizusuario', 'quiz_cuestionarios'),)