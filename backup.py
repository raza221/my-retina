from gtts import gTTS
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import subprocess
from PIL import Image, ImageTk
import cv2
import pytesseract
import sys
from playsound import playsound 

os.chdir(r"C:\Users\raza\Documents\PythonProjects\my-eyes")



def camera1():
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("Press 'Escape' when you are done.")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame!")
            break
        cv2.imshow("Press 'Escape' when you are done.", frame)
    
        k = cv2.waitKey(1)
        
        if k%256 == 32:
            # SPACE pressed
            img_name = (r"C:\Users\raza\Documents\PythonProjects\my-eyes\camera.png")
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            global picture
            picture = (r"C:\Users\raza\Documents\PythonProjects\my-eyes\camera.png")
        elif k%256 == 27:
            # ESC pressed
            break

    cam.release()
    
    cv2.destroyAllWindows()

def pickfile(): 
    global picture
    picture = askopenfilename()
    
root = tk.Tk()
root.title("MyRetina - Your Virtual Eyes")
root.geometry("700x800")
H = 700 
W = 800


image = ImageTk.PhotoImage (Image.open("background.png"))
bg = tk.Label(image=image)
bg.place(x=0,y=0, relwidth=1, relheight=1)


#canvas = tk.Canvas(root, height=H, width=W)
#canvas.pack()

#frame = tk.Frame(root, bg="#80c1ff")
#frame.place(relheight=1, relwidth=1)

#root.attributes("-alpha", 0.9)

button = tk.Button(bg, text ="Take Photo", bg = "black", fg="white", command=camera1)
button.pack(expand=True)

button = tk.Button(bg, text ="Choose from Photo Library", bg = "black", fg="white", command=pickfile)
button.pack(expand=True)

button = tk.Button(bg, text ="Exit", bg = "black", fg="red", command=exit)
button.pack(expand=True)

root.mainloop()

pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')


# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(picture)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
data = pytesseract.image_to_string(picture)
text_file = open("text.txt", "w")
text_file.write(data)
text_file.close()

#cv2.imshow('thresh', thresh)
cv2.waitKey()

fh = open("text.txt", "r")
myText = fh.read().replace("\n", " ")

language = 'en'
accent= 'co.uk'
output = gTTS(text=myText, lang=language, slow=False, tld=accent)
output.save("output.mp3")
fh.close()

playsound(r"C:\Users\raza\Documents\PythonProjects\my-eyes\output.mp3")
