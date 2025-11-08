import speech_recognition
import pyttsx3

# practicamos usando pyttsx3 para síntesis de voz
engine = pyttsx3.init()
engine.say("Hola, este es un ejemplo de síntesis de voz usando pyttsx3.")
engine.runAndWait()
