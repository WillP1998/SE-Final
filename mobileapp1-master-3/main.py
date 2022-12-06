from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout

from myfirebase import MyFirebase
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

import pyrebase

config = {
    "apiKey": "AIzaSyDSIHJVtxsqyjCdDztX7CNa-_JYXioUAIc",
    "authDomain": "fir-databse-a1d47.firebaseapp.com",
    "databaseURL": "https://fir-databse-a1d47-default-rtdb.firebaseio.com",
    "projectId": "fir-databse-a1d47",
    "storageBucket": "fir-databse-a1d47.appspot.com",
    "messagingSenderId": "121947075225",
    "appId": "1:121947075225:web:118e5c242dff926f27fe08",
    "measurementId": "G-XM6VLEW2P3"
}

firebase_auth = pyrebase.initialize_app(config)


class HomeScreen(Screen):
    pass


class FirstScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class EventScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignUpScreen(Screen):
    pass


class ForgotPasswordScreen(Screen):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


Window.size = (320, 600)


class MD3Card(MDCard):
    '''Implements a material design v3 card.'''


class Eventerly(MDApp):
    x = 10
    y = 15
    screen = None

    def build(self):
        self.my_firebase = MyFirebase()
        files = Builder.load_file("main.kv")
        self.screen = HomeScreen
        return files

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''

        def refresh_callback(interval):
            self.root.ids["home_screen"].ids["grid_layout"].clear_widgets()
            if self.x == 0:
                self.x, self.y = 15, 30
            else:
                self.x, self.y = 0, 15
            self.on_start()
            self.root.ids["home_screen"].ids["refresh_layout"].refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)

    def on_start(self):
        grid = self.root.ids["home_screen"].ids["grid_layout"]
        db = firebase_auth.database()
        users = db.child("Event").get()
        for user in users:
            grid.add_widget(
                MD3Card(
                    MDRelativeLayout(
                        MDLabel(
                            text=user.key().capitalize() + "\nLocation: " + user.val().get(
                                "location") + "\nDate: " + user.val().get("date") + "\nTime: " + user.val().get("time"),
                            color="grey",
                            pos=("12dp", "0dp"),
                        )
                    ),
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    padding="4dp",
                    size_hint=(None, None),
                    size=("270dp", "100dp"),
                    md_bg_color="#f6eeee"
                )
            )

    def change_screen(self, filename):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = filename
        pass

    def get_date(self, instance, value, date_range):
        self.root.ids["home_screen"].ids["date_label"].text = str(value)

    def on_date_cancel(self, instance, value):
        self.root.ids["home_screen"].ids["date_label"].text = "You clicked cancel!"

    def show_date_picker(self):
        date_dialog = MDDatePicker()

        date_dialog.bind(on_save=self.get_date, on_cancel=self.on_date_cancel)
        date_dialog.open()

    def get_time(self, instance, time):
        self.root.ids["home_screen"].ids["time_label"].text = str(time)

    def on_time_cancel(self, instance, time):
        self.root.ids["home_screen"].ids["time_label"].text = "You clicked cancel!"

    def show_time_picker(self):
        time_dialog = MDTimePicker()

        time_dialog.bind(on_cancel=self.on_time_cancel, time=self.get_time)
        time_dialog.open()

    def send_data(self, event, location, date, time):
        db = firebase_auth.database()
        data = {"location": location, "date": date, "time": time}
        db.child("Event").child(event).set(data)


if __name__ == "__main__":
    Eventerly().run()