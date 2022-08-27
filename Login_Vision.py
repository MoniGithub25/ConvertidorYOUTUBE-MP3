#SISTEMA DE REGISTRO Y LOGIN CON DETECCION Y RECONOCIMIENTO FACIAL en Python | Open cv | Tkinter


#LIBRERIAS
from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np

def registrar_usuario():
	usuario_info = usuario.get()
	contra_info = contra.get()

	archivo = open(usuario_info, "w")
	archivo.write(usuario_info + "\n")
	archivo.write(contra_info)
	archivo.close()

	#Limpiaremos los text variable
	usuario_entrada.delete(0, END)
	contra_entrada.delete(0,END)

	#Ahora le decimos al usuario que su registro ha sido exitoso
	Label(pantalla1, text = "Registro convencional exitoso", fg= "green", font= ("Calibri",11)).pack()



#FUNCION PARA ALMACENAR EL REGISTRO FACIAL

def registro_facial():
	#Vamos a capturar rostro
	cap = cv2.VideoCapture(0)
	while(True):
		ret, frame = cap.read()
		cv2.imshow('Registro facial', frame)
		if cv2.waitKey(1)== 27:
			break
	usuario_img = usuario.get()
	cv2.imwrite(usuario_img+".jpg", frame) #Guardamos la ultima captura del video como imagen y asignamos el nombre de usuario
	cap.release() #Cerrar
	cv2.destroyAllWindows()

	usuario_entrada.delete(0, END) #Limpiar los text variables
	contra_entrada.delete(0, END)
	Label(pantalla1, text = "Registro facial exitoso", fg= "green", font= ("Calibri", 11)).pack()

	#DETECTAMOS ROSTRO Y EXPORTAMOS PIXELES
	def reg_rostro(img, lista_resultados):
		data = pyplot.imread(img)
		for i in range(len(lista_resultados)):
			x1, y1, ancho, alto = lista_resultados[i]['box']
			x2, y2 = x1 + ancho, y1 + alto
			pyplot.subplot(1, len(lista_resultados), i+1)
			pyplot.axis('off')
			cara_reg = data[y1:y2, x1:x2]
			cara_reg =cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen en un tamaño 150x200
			cv2.imshow(usuario_img+".jpg", cara_reg)
			pyplot.imshow(data[y1:y2, x1:x2])
		pyplot.show()

	img = usuario_img+".jpg"
	pixeles = pyplot.imread(img)
	detector = MTCNN()
	caras = detector.detect_faces(pixeles)
	reg_rostro(img, caras)

#CREAR FUNCION DE REGISTRO
def registro():
	global usuario
	global contra
	global usuario_entrada
	global contra_entrada
	global pantalla1
	pantalla1 =Toplevel(pantalla)
	pantalla1.title("Registro")
	pantalla1.geometry("300x250")

	usuario = StringVar()
	contra = StringVar()

	Label(pantalla, text = "Registro facial: debe de asignar un usuario:").pack()
	Label(pantalla1, text = "Registro tradicional: debe asignar usuario y contraseña").pack()
	Label(pantalla1, text = "").pack()#ESPACIO
	Label(pantalla1, text = "Usario * ").pack()#Mostrar usuario
	usuario_entrada = Entry(pantalla1, textvariable = usuario) #Espacio para que el usuario ingrese info
	usuario_entrada.pack()
	Label(pantalla1, text = "Contraseña * ").pack()
	contra_entrada = Entry(pantalla1, textvariable = contra) #Espacio para que el usuario ingrese la contraseña
	contra_entrada.pack()
	Label(pantalla1, text= "").pack()#ESPACIO
	Button(pantalla1, text = "Registro Tradicional", width = 15, height = 1, command = registrar_usuario).pack()

	#BOTON REGISTRO FACIAL
	Label(pantalla1, text = "").pack()
	Button(pantalla1, text= "Registro Facial", width= 15, height = 1, command = registro_facial).pack()

#FUNCION PARA VERIFICAR LOS DATOS INGRESADOS AL LOGIN

def verificacion_login():
	log_usuario = verificacion_usuario.get()
	log_contra = verificacion_contra.get()

	usuario_entrada2.delete(0,END)
	contra_entrada2.delete(0, END)

	lista_archivos = os.listdir()
	if log_usuario in lista_archivos:
		archivo2 = open(log_usuario, "r")
		verificacion = archivo2.read().splitlines()
		if log_contra in verificacion:
			print("Inicio de sesion exitoso")
			Label(pantalla2, text= "Inicio de sesion exitoso", fg = "green", font= ("Calibri",11)).pack()
		else:
			print("Contraseña incorrecta, ingrese de nuevo")
			Label(pantalla2, text= "Contraseña incorrecta", fg = "red", font=("Calibri",11)).pack()
	else:
		print("Usuario no encontrado")
		Label(pantalla2, text ="Usuario no encontrado", fg = "red", font=("Calibri",11)).pack()



#FUNCION LOGIN FACIAL
def login_facial():
	
	cap = cv2.VideoCapture(0)
	while(True):
		ret, frame = cap.read()
		cv2.imshow('Login Facial', frame)
		if cv2.waitKey(1)==27:
			break
	usuario_login = verificacion_usuario.get()
	cv2.imwrite(usuario_login+"LOG.jpg", frame)
	cap.release()
	cv2.destroyAllWindows()

	usuario_entrada2.delete(0, END)#Limpiamos los text variables
	contra_entrada2.delete(0, END)

	#FUNCION PARA GUARDAR ROSTRO

	def log_rostro(img, lista_resultados):
		data = pyplot.imread(img)
		for i in range(len(lista_resultados)):
			x1, y1, ancho, alto = lista_resultados[i]['box']
			x2, y2 = x1 + ancho, y1 + alto
			pyplot.subplot(1, len(lista_resultados), i+1)
			pyplot.axis('off')
			cara_reg = data[y1:y2, x1:x2]
			cara_reg = cv2.resize(cara_reg, (150,200), interpolation = cv2.INTER_CUBIC)# GUARDAR IMAGEN
			cv2.imwrite(usuario_login+"LOG.jpg", cara_reg)
			return pyplot.imshow(data[y1:y2, x1:x2])
		pyplot.show()

	#DETECTAR ROSTRO

	img = usuario_login+"LOG.jpg"
	pixeles = pyplot.imread(img)
	detector = MTCNN()
	caras = detector.detect_faces(pixeles)
	log_rostro(img, caras)

	#FUNCION PARA COMPARAR LOS ROSTROS
	def orb_sim(img1, img2):
		orb = cv2.ORB_create()

		kpa, descr_a = orb.detectAndCompute(img1, None) #Crear descriptor 1 y extraer puntos clave
		kpb, descr_b = orb.detectAndCompute(img2, None) #Crear descriptor 2 y extraer puntos clave

		comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #Creamos comparador de fuerza

		matches = comp.match(descr_a, descr_b)

		regiones_similares = [i for i in matches if i.distance < 70]
		if len(matches) == 0:
			return 0
		return len(regiones_similares)/len(matches) #Exportamos el porcentaje de similitud

	#IMPORTAR IMAGENES Y LLAMAMOS A LA FUNCION PARA QUE LAS COMPARE
	im_archivos = os.listdir()
	if usuario_login+".jpg" in im_archivos:
		rostro_reg = cv2.imread(usuario_login+".jpg", 0)
		rostro_log = cv2.imread(usuario_login+"LOG.jpg", 0)
		similitud = orb_sim(rostro_reg, rostro_log)
		if similitud >= 0.80:
			Label(pantalla2, text ="Inicio de sesion exitoso", fg= "green", font=("Calibri",11)).pack()
			print("Bienvenido al sistema usuario: ", usuario_login)
			print("Compatibilidad con la foto del registro: ", similitud)
			if usuario_login == "CapitanaMonica":
				archivo = open("Cuaderno_de_Bitacora_Capitan.txt", "a")
				fecha= input("\nFecha estelar: ")
				archivo.write("Fecha estelar: ")
				archivo.write( fecha + '\n')
				texto = input("Entrada cuaderno de bitacora: \n>>")
				archivo.write(texto + '\n')
				archivo.close()
			else:
				archivo = open("Cuaderno_de_Bitacora_Tenientes", "a")
				archivo.write(str(usuario_login + '\n'))
				fecha = input("\nFecha estelar: ")
				archivo.write( fecha + '\n')
				texto = input("Entrada cuaderno de bitacora: \n>>")
				archivo.write(texto + '\n')
				archivo.close()

		else:
			print("Rostro incorrecto, Certifique su usuario")
			print("Compatibilidad con la foto del registro: ", similitud)
			Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font= ("Calibri",11)).pack()
	else:
		print("Usuario no encontrado")
		Label(pantalla2, text = "Usuario no encontrado", fg = "red", font=("Calibri",11)).pack()




#FUNCION QUE ASIGNAREMOS AL BOTON LOGIN

def login():
	global pantalla2
	global verificacion_usuario
	global verificacion_contra
	global usuario_entrada2
	global contra_entrada2

	pantalla2 = Toplevel(pantalla)
	pantalla2.title("Login")
	pantalla2.geometry("320x250") #CREAMOS LA VENTANA
	Label(pantalla2, text = "Login facial: debe de asignar un usuario").pack()
	Label(pantalla2, text = "Login tradicional: debe asignar usuario y contraseña").pack()
	Label(pantalla2, text = "").pack()

	verificacion_usuario = StringVar()
	verificacion_contra = StringVar()

	#INGRESAR DATOS
	Label(pantalla2, text = "Usuario * ").pack()
	usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
	usuario_entrada2.pack()
	Label(pantalla2, text = "Contraseña * ").pack()
	contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
	contra_entrada2.pack()
	Label(pantalla2, text= "").pack()
	Button(pantalla2, text= "Inicio de sesion tradicional", width = 20, height = 1, command = verificacion_login).pack()

	#CREAR BOTON PARA HACER LOGIN FACIAL
	Label(pantalla2, text= "").pack()
	Button(pantalla2, text = "Inicio de sesion facial", width = 20, height =1, command =login_facial).pack()




#FUNCION PANTALLA PRINCIPAL
def pantalla_principal():
	global pantalla
	pantalla = Tk()
	pantalla.geometry("300x250")
	pantalla.title("LOGIN DESPACHO TORRES PC")
	Label(text= "Login inteligente", bg= 'gray', width="300", height="2", font=("Verdana", 13)).pack()

	#CREAR BOTONES
	Label(text = "").pack()
	Button(text = "Iniciar sesion", width="30", height="2",command=login).pack()
	Label(text = "").pack()
	Button(text = "Registro", width="30", height="2", command=registro).pack()

	pantalla.mainloop()

pantalla_principal()



