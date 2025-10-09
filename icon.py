from PIL import Image

img = Image.open("icon.png")
# opcionalno: napravi različite dimenzije u jednoj .ico datoteci
sizes = [(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]
img.save("app.ico", sizes=sizes)
