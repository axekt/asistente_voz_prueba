import speech_recognition
import pyttsx3
import webbrowser
from datetime import datetime
import requests

#creacion asistente de voz 
def crear_asistente_voz():
    recognizer = speech_recognition.Recognizer()
    engine = pyttsx3.init()
    return recognizer, engine
    
recognizer, engine = crear_asistente_voz()

def escuchar_comando():
    with speech_recognition.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language="es-ES")
        print(f"Comando reconocido: {comando}")
        return comando
    except speech_recognition.UnknownValueError:
        print("No se entendió el comando.")
        return ""
    except speech_recognition.RequestError:
        print("Error al solicitar resultados del servicio de reconocimiento.")
        return ""
def obtener_hora():
    """Devuelve la hora actual en formato legible."""
    ahora = datetime.now()
    return ahora.strftime("%H:%M:%S")

def obtener_clima(ciudad="Madrid"):
    """Obtiene el clima de una ciudad (requiere API key de OpenWeatherMap)."""
    API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu API key de https://openweathermap.org/
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"{desc}, {temp} grados"
    except requests.RequestException as e:
        return f"No pude obtener el clima: {str(e)}"
    except KeyError:
        return "Error al procesar la respuesta del clima."

def obtener_noticias(tema="F1"):
    """Obtiene las últimas noticias de un tema (requiere API key de NewsAPI)."""
    API_KEY = "TU_NEWSAPI_KEY_AQUI"  # Reemplaza con tu API key de https://newsapi.org/
    url = f"https://newsapi.org/v2/everything?q={tema}&sortBy=publishedAt&language=es&pageSize=3&apiKey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data['totalResults'] == 0:
            return f"No encontré noticias sobre {tema}."
        articulos = data['articles'][:3]  # Primeros 3 artículos
        respuesta = f"Últimas noticias de {tema}: "
        for i, art in enumerate(articulos, 1):
            respuesta += f"{i}. {art['title']}. "
        return respuesta
    except requests.RequestException as e:
        return f"No pude obtener las noticias: {str(e)}"
    except KeyError:
        return "Error al procesar las noticias."

def responder_comando(comando):
    if "hola" in comando.lower():
        respuesta = "Hola, ¿en qué puedo ayudarte?"
    elif "cómo estás" in comando.lower():
        respuesta = "Estoy bien, gracias por preguntar."
    elif "qué hora es" in comando.lower() or "hora" in comando.lower():
        respuesta = f"Son las {obtener_hora()}"
    elif "clima" in comando.lower() or "tiempo" in comando.lower() or "lluvia" in comando.lower():
        respuesta = obtener_clima()
    elif "noticias" in comando.lower() or "noticia" in comando.lower():
        # Extrae el tema de las noticias (ej: "noticias de F1" -> "F1")
        tema = comando.lower().replace("noticias", "").replace("noticias de", "").replace("dame", "").replace("últimas", "").strip()
        if not tema or tema == "de":
            tema = "general"
        respuesta = obtener_noticias(tema)
    else:
        respuesta = "No entendí el comando."
    engine.say(respuesta)
    engine.runAndWait()
    return respuesta

#logica si el usuario pide alguna acción esta sera buscada en google
def buscar_en_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

#main 
if __name__ == "__main__":
    comando = escuchar_comando()
    if comando:
        if "buscar" in comando.lower():
            termino_busqueda = comando.lower().replace("buscar", "").strip()
            buscar_en_google(termino_busqueda)
        else:
            responder_comando(comando)