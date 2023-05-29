import webbrowser
import pyaudio
import pyttsx3
import speech_recognition as sr
import pyjokes
import pywhatkit
import yfinance as yf
import datetime
import wikipedia

#escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    #almacenar el recognizer en variable
    r= sr.Recognizer()

    #configurar el microfono

    with sr.Microphone() as origen:

        #tiempo de espera desde que se activa el microfono
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print("Ya puedes hablar")

        #guardar el audio en variable
        audio= r.listen(origen)

        try:
            #buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-Co")

            #prueba de conversion
            print("Dijiste:" + pedido)

            #devolver a pedido
            return pedido

            #en caso que no comprenda el audio

        except sr.UnknownValueError():

            #prueba de que no comprendio el audio
            print("No entendi que dijiste")

            #devolver error
            return "sigo esperando"

        #en caso de no resolver el pedido
        except sr.RequestError():
                #prueba de que no comprendio el audio
            print("No entendi que dijiste")

            #devolver error
            return "sigo esperando"
        #error inesperado
        except sr.UnknownValueError():
            
            print("ups algo ha salido mal")

#opciones de voz/idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'



#funcion para que el asistente sea escuchado

def hablar(mensaje):

    #encender el motor de pyttsx3
    engine= pyttsx3.init()
    engine.setProperty('voice', id1)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#informar el dia de la semana
def pedir_dia():
    #crear la variable con datos de hoy
    dia= datetime.date.today()
    print(dia)

    #crear variable para el dia de la semana
    dia_semana= dia.weekday()
    print(dia_semana)

    #diccionario con nombres de los dias
    calendario= {0:'lunes',
                1:'martes',
                2:'miércoles',
                3:'jueves',
                4:'viernes',
                5:'sábado',
                6:'domingo'}

    #decir dia de la semana
    hablar(f'hoy es {calendario[dia_semana]}')

#informar que hora es
def pedir_hora():

    #crear una variable con datos de la hora
    hora= datetime.datetime.now()
    hora= f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
    #decir la hora
    hablar(hora)


#funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de hora
    hora=datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 19:
        momento= "Buenas noches"
    elif hora.hour >= 6 and hora.hour < 12:
        momento = 'Buen día'
    else:
        momento = "Buenas tardes"
    #decir saludo
    hablar(f"Hola {momento}, soy tu asistente personal. Por favor dime cómo te puedo ayudar?")


#funcion central del asistence
def pedir_cosas():

    #activar saludo inicial
    saludo_inicial()

    #variable de corte
    comenzar = True
    
    #loop central
    while comenzar:
        #activar el micro y guardar el pedido en variable

        pedido = transformar_audio_en_texto()

        if 'Abre Google' in pedido:
            hablar('Con gusto, abriendo google')
            webbrowser.open('https://www.google.com')
            continue

        elif 'Abre YouTube' in pedido:
            hablar('Con gusto, abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue

        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue

        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'Busca en Wikipedia' or 'Wikipedia'in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en Wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar('Wikipedia dice esto:')
            hablar(resultado)
            continue

        elif 'Busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido= pedido.replace('Busca en internet', '')
            pywhatkit.search(pedido)
            hablar('esto es lo que he encontrado')
            continue

        elif 'Reproducir' or 'Reproduce' or "Reproductor" in pedido:
            hablar("buena elección, ya empiezo a reproducirlo")
            pedido= pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            continue

        elif 'chiste' in pedido:
            hablar (pyjokes.get_joke('es'))
            continue

        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                        'Amazon':'AMZN',
                        'Google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, no la he encontrado')

        elif 'terminar' in pedido:
            hablar('Estoy para servirte, ten un buen día.')
            comenzar = False

pedir_cosas()
