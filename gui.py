import tkinter as tk
import ttkbootstrap as ttk
import weather_api as wx
from PIL import Image, ImageTk
from datetime import datetime

class WeatherApp(ttk.Window):
    def __init__(self):
        super().__init__(themename='morph')
        self.title("Weather App")
        self.geometry("1024x768")
        self.resizable(False,False)
        #self.bg = tk.PhotoImage(file='bg.png')
        #self.bg_label = ttk.Label(self, image=self.bg)
        #self.bg_label.place(x=-2,y=-2)
        self.forecast_response = wx.forecast_api_call()
        self.image_paths = wx.get_condition_image(self.forecast_response)
        self.location = self.forecast_response['location_dict']['loc_name'] + ', ' + self.forecast_response['location_dict']['loc_region']
        self.current_time = self.forecast_response['location_dict']['loc_time']
        self.current_dict = self.forecast_response['current_dict']
        self.day1_dict = self.forecast_response['day_1_dict']
        self.day2_dict = self.forecast_response['day_2_dict']
        self.create_widgets()


    def create_widgets(self):

        self.title_label = ttk.Label(self, text="3-Day Forecast", font=('Arial',48))
        self.title_label.pack(pady=(180,10))

        self.forecast_frame = ttk.Frame(self, borderwidth=1, relief='solid')
        self.create_weather_icons()
        self.attach_forecast_data()
        self.forecast_frame.pack()

        # I guess I can show more useful data in current conditions?
        self.conditions_frame = ttk.Frame(self)
        self.attach_current_data()
        self.conditions_frame.pack()

        self.get_weather_button = ttk.Button(self, text="Debug Weather", command=self.debug_show_forecast_response, padding=30, bootstyle=('INFO', 'OUTLINE'))
        self.get_weather_button.pack(pady=(50,0))


    def create_weather_icons(self):
        
        self.forecast0_image = Image.open(self.image_paths[0])
        self.forecast0_image= self.forecast0_image.resize((128,128), Image.LANCZOS)
        self.display0 = ImageTk.PhotoImage(self.forecast0_image)
        self.forecast0_image_label = ttk.Label(self.forecast_frame, image=self.display0)
        self.forecast0_image_label.grid(column=0, row=1, padx=5, pady=(5,1))

        self.forecast1_image = Image.open(self.image_paths[1])
        self.forecast1_image= self.forecast1_image.resize((128,128), Image.LANCZOS)
        self.display1 = ImageTk.PhotoImage(self.forecast1_image)
        self.forecast1_image_label = ttk.Label(self.forecast_frame, image=self.display1)
        self.forecast1_image_label.grid(column=1, row=1, padx=5, pady=(5,1))

        self.forecast2_image = Image.open(self.image_paths[2])
        self.forecast2_image= self.forecast2_image.resize((128,128), Image.LANCZOS)
        self.display2 = ImageTk.PhotoImage(self.forecast2_image)
        self.forecast2_image_label = ttk.Label(self.forecast_frame, image=self.display2)
        self.forecast2_image_label.grid(column=2, row=1, padx=5, pady=(5,1))


    def attach_forecast_data(self):

        # TODO: HOW DO I PARSE THE DATES WTF
        self.current_date_formatted = datetime.strptime(self.current_time,'%Y-%m-%d %H:%M')
        self.day1_date_formatted = datetime.strptime(self.day1_dict['day_1_date'][0:10],'%Y-%m-%d')
        self.day2_date_formatted = datetime.strptime(self.day2_dict['day_2_date'][0:10],'%Y-%m-%d')


        self.forecast0_date_label = ttk.Label(self.forecast_frame, text=self.current_date_formatted.strftime('%a'), font=('Arial', 14))
        self.forecast1_date_label = ttk.Label(self.forecast_frame, text=self.day1_date_formatted.strftime('%a'), font=('Arial', 14))
        self.forecast2_date_label = ttk.Label(self.forecast_frame, text=self.day2_date_formatted.strftime('%a'), font=('Arial', 14))

        self.condition_text0 = self.current_dict['current_condition_dict']['text']
        self.condition_text1 = self.day1_dict['day_1_condition_dict']['text']
        self.condition_text2 = self.day2_dict['day_2_condition_dict']['text']

        self.temp0 = tk.StringVar(self,self.condition_text0 + ' ' + str(self.current_dict['current_temp_f']) + chr(176) + 'F')
        self.temp1 = tk.StringVar(self,self.condition_text1 + ' ' + str(self.day1_dict['day_1_avgtemp_f']) + chr(176) + 'F')
        self.temp2 = tk.StringVar(self,self.condition_text2 + ' ' + str(self.day2_dict['day_2_avgtemp_f']) + chr(176) + 'F')


        self.forecast0 = ttk.Label(self.forecast_frame, textvariable=self.temp0)
        self.forecast1 = ttk.Label(self.forecast_frame, textvariable=self.temp1)
        self.forecast2 = ttk.Label(self.forecast_frame,textvariable=self.temp2)

        self.forecast0_date_label.grid(column=0, row=0, pady=(1,5))
        self.forecast1_date_label.grid(column=1, row=0, pady=(1,5))
        self.forecast2_date_label.grid(column=2, row=0, pady=(1,5))
        self.forecast0.grid(column=0, row=2, pady=(1,10))
        self.forecast1.grid(column=1, row=2, pady=(1,10))
        self.forecast2.grid(column=2, row=2, pady=(1,10))


    def attach_current_data(self):
        self.location_label = ttk.Label(self.conditions_frame, text=self.location, font=('Arial',18))
        self.local_time_label = ttk.Label(self.conditions_frame, text=('Last updated: ' + self.current_time), font=('Arial',18))
        self.current_temp_label = ttk.Label(self.conditions_frame, text=(str(self.current_dict['current_temp_f']) + chr(176) + 'F'))
        self.current_sky_label = ttk.Label(self.conditions_frame, text=self.current_dict['current_condition_dict']['text'])

        self.location_label.pack(pady=(10,5))
        self.local_time_label.pack(pady=(5,5))
        self.current_temp_label.pack(pady=(5,5))
        self.current_sky_label.pack(pady=(5,5))
        

    def debug_show_forecast_response(self):
        wx.pp.pprint(self.forecast_response)
        print(self.location)


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()