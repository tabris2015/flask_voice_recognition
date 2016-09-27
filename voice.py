import app
import speech_recognition as sr
from datetime import datetime

recognizer = sr.Recognizer()

with sr.Microphone() as source:
	print "di algo..."
	audio = recognizer.listen(source)

text = ""

try:
    text = recognizer.recognize_sphinx(audio)
    print "tu dijiste: " + text
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

print "introduciendo a la base de datos..."
register = app.Text(text,datetime.utcnow())
app.db.session.add(register)
app.db.session.commit()

print "base de datos actualizada!"