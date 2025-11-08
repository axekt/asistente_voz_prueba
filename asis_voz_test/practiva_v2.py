import speech_recognition
import pyttsx3

# practicamos usando recognizer para reconocimiento de voz
recognizer = speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    print("Por favor prueba hablando en el micrófono...")
    audio = recognizer.listen(source)
    try:
        text=recognizer.recognize_google(audio, language="es-ES")
        print("Has dicho: " + text)
    except speech_recognition.UnknownValueError:
        print("No se pudo entender el audio.")
    except speech_recognition.RequestError as e:
        print("Error al solicitar resultados; {0}".format(e))
    except speech_recognition.WaitTimeoutError:
        print("Tiempo de espera agotado mientras se esperaba el audio.")
    

#ahora integramos pyttsx3 para síntesis de voz
engine = pyttsx3.init()
engine.say("Has dicho: " + text)
engine.runAndWait()


#logica si el usuario pide alguna acción

def accion_usuario(texto):
    texto = texto.lower()
    if "hora" in texto:
        from datetime import datetime
        ahora = datetime.now().strftime("%H:%M")
        respuesta = "la hora actual es " + ahora
    elif "fecha" in texto:
        from datetime import datetime
        hoy = datetime.now().strftime("%d/%m/%Y")
        respuesta = "la fecha de hoy es " + hoy
    else:
        respuesta = "No he entendido tu solicitud."
    engine.say(respuesta)
    engine.runAndWait()
    
def main():
    accion_usuario(text)