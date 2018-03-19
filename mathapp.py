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
from sklearn import svm, datasets
from sklearn.metrics import accuracy_score

#Build model for digit recognition
digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100)
clf.fit(digits.data[:], digits.target[:])

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
        		#Left num
                Color(1,0,.8,1)
                Rectangle(pos=(20, 190), size=(300,300))
                Color(1,1,1,1)
                Rectangle(pos=(30, 200), size=(280,280)) 
                #Right num
                Color(1,0,.8,1)
                Rectangle(pos=(470, 190), size=(300,300))            
                Color(1,1,1,1)
                Rectangle(pos=(480, 200), size=(280,280))
                
                #symbol

                Color(0,1,.8,1)
                Rectangle(pos=(320, 270), size=(150,150))            
                Color(1,1,1,1)
                Rectangle(pos=(325, 275), size=(140,140))
                

class PaintApp(App):


    def build(self):
        parent = Widget()

        self.painter = PaintWidget()
        self.rectBG = BGWidget()

       
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)

        savebtn = Button(text='Solve', pos=(100, 0))
        savebtn.bind(on_release=self.screengrab)
       
        parent.add_widget(self.rectBG)
        parent.add_widget(self.painter)
        parent.add_widget(savebtn)
        parent.add_widget(clearbtn)


        return parent

    def clear_canvas(self, obj):
       self.painter.canvas.clear()

    def screengrab(self,*largs):
    		#take a screen shot
            sh = Window.screenshot("screenshot.png")
            ti = Image.open(sh)
            width, height = ti.size

            #copy image
            img=ti.copy()

            #crop out the two number in white boxes and saved respectively
            num1 = img.crop((30, 120, 310, 400))
            num1.save(sh[:-4]+"num1.png")
            num2 = img.crop((480, 120, 760, 400))
            num2.save(sh[:-4]+"num2.png")

            #Open cropped images
            fullnum1 = Image.open(sh[:-4]+"num1.png")
            fullnum2 = Image.open(sh[:-4]+"num2.png")
            
            #Convert cropped images to 8px X 8px 
            smallnum1 = fullnum1.resize((8,8), Image.BILINEAR )
            smallnum2 = fullnum2.resize((8,8), Image.BILINEAR )
          
          
            #Convert small images to gray scale and turn them into numpy arrays
            smallnum1gray= smallnum1.convert('L')
            smallnum1gray= np.array(smallnum1gray)
            smallnum2gray= smallnum2.convert('L')
            smallnum2gray= np.array(smallnum2gray)

            #convert 8 bit grayscale to 4 bit
            fbit1=np.floor(interp(smallnum1gray, [0,255],[16,0]))
            fbit2=np.floor(interp(smallnum2gray, [0,255],[16,0]))
           # print(fbit2.ravel())
            
            #convert fbit's to single array instead of 2d(image)
            pred1 = clf.predict([fbit1.ravel()])
            pred2=clf.predict([fbit2.ravel()])
            print(pred1, pred2)
            ftoup1 = fbit1, pred1
            ftoup2 = fbit2, pred2

            #print(digits.data[pred1])
            #print(digits.data[pred])
            plt.figure(figsize=(14,8))
            for index, (image, label) in enumerate(zip([fbit1, fbit2], [pred1, pred2])):
                plt.subplot(2, 2, index + 1)
                plt.imshow(image, cmap= plt.get_cmap('gray'))       
                plt.title('Prediction: %i\n' % label, fontsize = 15  )   
                plt.axis('off')

            plt.subplot(2,2, 3)
            plt.imshow(np.reshape(digits.data[pred1],(-1, 8)), cmap = plt.get_cmap('gray'))
            plt.title('similar to: %i\n' % pred1)
            plt.axis('off')
            plt.subplot(2,2, 4)
            plt.imshow(np.reshape(digits.data[pred2],(-1, 8)), cmap = plt.get_cmap('gray'))
            plt.title('similar to: %i\n' % pred2)
            plt.axis('off')
            plt.show()

            
            return fbit1, fbit2





paint = PaintApp()

paint.run()