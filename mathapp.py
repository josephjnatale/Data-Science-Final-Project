from random import random
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import *
from kivy.graphics import *
from kivy.core.window import Window
kivy.require('1.9.0')
from PIL import *
from PIL.ImageOps import grayscale
import numpy as np
from numpy import interp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class PaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (0,0,0, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 80.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=25)

    def on_touch_move(self, touch):

        touch.ud['line'].points += [touch.x, touch.y]


class BGWidget(Widget):
    def __init__(self, **kwargs):
        super(BGWidget, self).__init__(**kwargs)

        with self.canvas:
                Color(1,1,1,1)
                Rectangle(pos=(30, 200), size=(280,280))
                Rectangle(pos=(480, 200), size=(280,280))
                Rectangle(pos=(325, 275), size=(140,140))
                

class PaintApp(App):


    def build(self):
        parent = Widget()

        self.painter = PaintWidget()
        self.rectBG = BGWidget()

       
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)

        savebtn = Button(text='Save', pos=(100, 0))
        savebtn.bind(on_release=self.screengrab)
       
        parent.add_widget(self.rectBG)
        parent.add_widget(self.painter)
        parent.add_widget(savebtn)
        parent.add_widget(clearbtn)


        return parent

    def clear_canvas(self, obj):
       self.painter.canvas.clear()

    def screengrab(self,*largs):

            sh = Window.screenshot("screenshot.png")
            ti = Image.open(sh)
            width, height = ti.size
            img=ti.copy()
            num1 = img.crop((30, 120, 310, 400))
            num1.save(sh[:-4]+"num1.png")
            num2 = img.crop((480, 120, 760, 400))
            num2.save(sh[:-4]+"num2.png")

            fullnum1 = Image.open(sh[:-4]+"num1.png")
            print(fullnum1.size)
            smallnum1 = fullnum1.resize((8,8), Image.BICUBIC )
            print(smallnum1.size)

            smallnum1gray= smallnum1.convert('L')
            smallnum1gray= np.array(smallnum1gray)
           
            print(smallnum1gray)
            fbit=np.floor(interp(smallnum1gray, [0,255],[16,0]))
           
            print(fbit)
            plt.imshow(smallnum1, cmap= plt.get_cmap('gray'))
            plt.show()
            return fbit, 0

'''
def rgb2gray(rgb):
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
 
    return gray

testimg = mpimg.imread("screenshot0001num1.png")
print("img size: ", testimg.size)

testimg = testimg.resize((28,28))
print("img size: ", testimg.size)

gray = rgb2gray(img)    
plt.imshow(gray, cmap = plt.get_cmap('gray'))
plt.show()

'''



paint = PaintApp()

paint.run()