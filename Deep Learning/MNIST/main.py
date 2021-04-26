#Importing Libraries
import numpy as np
from keras.models import load_model
from PIL import ImageGrab, Image
import win32gui
from tkinter import *
import tkinter as tk

# Loading Model
model = load_model('mnist_copy.h5')

# Function to predict from input image
def predict_digit(img):
    """[summary]

    Args:
        img ([image]): Image to be predicted

    Returns:
        [array]: [description]
    """

    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")  #Canvas to write
        self.label = tk.Label(self, text=" <--Draw", font=("Helvetica", 48))                  # The "Draw" test
        self.classify_btn = tk.Button(self, text = "Predict", command = self.classify_handwriting)   #Button to submit for prediction
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)       # Clear Button
       
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
    
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a,b,c,d = rect
        rect=(a+4,b+4,c-4,d-4)
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white')

       
app = App()
mainloop()