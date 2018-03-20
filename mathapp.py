import numpy as np
import kivy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import *
from kivy.graphics import *
from kivy.core.window import Window
from random import random
from PIL import *
from PIL.ImageOps import grayscale
from numpy import interp
from sklearn import svm, datasets
from sklearn.metrics import accuracy_score
import glob
kivy.require('1.9.0')

#Build model for digit recognition
digits = datasets.load_digits()
clf = svm.SVC(gamma=0.001, C=100)
clf.fit(digits.data[:], digits.target[:])

#Build the model for operation recognition
arthm_imgs = []
arthm_val = []
arthm = []
    #add the '+' files with the key 1
for filename in glob.glob('data/add/*arthm.png'):
    im = Image.open(filename)
    arthm_imgs.append(im)
    im = np.floor(interp(im, [0, 255], [16,0]))
    arthm_val.append(im)
    arthm.append((im, 1))

    #add the '-' files with the key 2
for filename in glob.glob('data/sub/*arthm.png'):
    im = Image.open(filename)
    arthm_imgs.append(im)
    im = np.floor(interp(im, [0, 255], [16,0]))
    arthm_val.append(im)
    arthm.append((im, 2))
    
    #add the '*' files with the key 3
for filename in glob.glob('data/mul/*arthm.png'):
    im = Image.open(filename)
    arthm_imgs.append(im)
    im = np.floor(interp(im, [0, 255], [16,0]))
    arthm_val.append(im)
    arthm.append((im, 3))
    
    #add the '/' files with the key 4
for filename in glob.glob('data/div/*arthm.png'):
    im = Image.open(filename)
    arthm_imgs.append(im)
    im = np.floor(interp(im, [0, 255], [16,0]))
    arthm_val.append(im)
    arthm.append((im, 4))

clf2 = svm.SVC(gamma=0.001, C=100)
data = np.array([x[0] for x in arthm])
target = np.array([x[1] for x in arthm])

newdata=[]
for i in range(len(data)):
    newdata.append(data[i].ravel())

#print([newdata])
clf2.fit(newdata, target)


#create global values for predictions
pnum1, pnum2, parth =0,0,0
class PaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (0,0,0, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 80.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=20)

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

            #crop out the two number and symbol in white boxes and saved respectively
            num1 = img.crop((30, 120, 310, 400))
            num1.save(sh[:-4]+"num1.png")
            num2 = img.crop((480, 120, 760, 400))
            num2.save(sh[:-4]+"num2.png")

            arthm = img.crop((325,185, 465, 325))
            arthm.save(sh[:-4]+"arthm.png")

            #Open cropped images
            fullnum1 = Image.open(sh[:-4]+"num1.png")
            fullnum2 = Image.open(sh[:-4]+"num2.png")
            
            #Convert cropped images to 8px X 8px 
            smallnum1 = fullnum1.resize((8,8), Image.BILINEAR )
            smallnum2 = fullnum2.resize((8,8), Image.BILINEAR )
            smallarthm = arthm.resize((8,8), Image.BILINEAR)
          
          
            #Convert small images to gray scale and turn them into numpy arrays
            smallnum1gray= smallnum1.convert('L')
            smallnum1gray= np.array(smallnum1gray)
            smallnum2gray= smallnum2.convert('L')
            smallnum2gray= np.array(smallnum2gray)

            smallarthmgray = smallarthm.convert('L')
            smallarthmgray.save(sh[:-4]+"arthm.png")
            smallarthmgray = np.array(smallarthmgray)


            #convert 8 bit grayscale to 4 bit
            fbit1=np.floor(interp(smallnum1gray, [0,255],[16,0]))
            fbit2=np.floor(interp(smallnum2gray, [0,255],[16,0]))
            smallarthmgray=np.floor(interp(smallarthmgray, [0,255], [16,0]))

           # print(fbit2.ravel())
            
            #convert fbit's to single array instead of 2d(image)
            predarthm = clf2.predict([smallarthmgray.ravel()])
            pred1 = clf.predict([fbit1.ravel()])
            pred2=clf.predict([fbit2.ravel()])

            pnum1, pnum2, parth = pred1, pred2, predarthm
            print(pnum1, pnum2, parth)
            #print(digits.data[pred1])
            #print(digits.data[pred])
            print("answer:")
            if parth ==1:
            		print(pnum1+pnum2)
            		
            if parth ==2:
            		print(pnum1 - pnum2)

            if parth ==3:
            		print(pnum1 * pnum2)

            if parth ==4: 
            		print(pnum1 / pnum2)

            #add plot of drawn image vs what the model that it was
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

            #Show the plots
            plt.show()

            
            return pnum1, pnum2, parth





paint = PaintApp()

paint.run()