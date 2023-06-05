import tkinter as tk
import ttkbootstrap as ttk

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("1024x768")
        
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="WEATHER")
        self.title_label.pack()

        self.weather_frame = ttk.Frame(self)
        self.forecast = ttk.Label(self.weather_frame, text='FORECAST HERE')
        self.forecast.pack()
        self.weather_frame.pack()

        self.conditions_frame = ttk.Frame(self)
        self.conditions = ttk.Label(self.conditions_frame, text='CURRENT WEATHER CONDITIONS')
        self.conditions.pack()
        self.conditions_frame.pack()

        self.get_weather_button = ttk.Button(self, text="Get Weather")
        self.get_weather_button.pack()

        self.weather_label = ttk.Label(self, text="")
        self.weather_label.pack()

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()