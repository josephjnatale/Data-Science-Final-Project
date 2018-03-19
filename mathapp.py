from random import random
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import *
from kivy.graphics import *
from kivy.core.window import Window
kivy.require('1.9.0')
from PIL import Image


class PaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
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






paint = PaintApp()

paint.run()