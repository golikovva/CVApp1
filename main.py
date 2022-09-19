from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp


class MApp(App):
    def __init__(self):
        super().__init__()
        self.image = Image()
        self.capture = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.image)
        btn = Button(text='CLICK',
                     pos_hint={'center_x': .5, 'center_y': .5},
                     size_hint=(None, None))
        layout.add_widget(btn)

        Clock.schedule_interval(self.load_video, 1.0 / 30)
        return layout

    def load_video(self, obj):
        ret, frame = self.capture.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        # frame initialize
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


MApp().run()
