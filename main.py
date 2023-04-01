import tkinter as tk
import nmap
import requests


class Sidebar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Style the sidebar
        self.config(width=40, bg="white")
        self.pack(side="left", fill="y")

        # Create sidebar links with icons
        home_icon = tk.PhotoImage(file="ho.png")
        home_button = tk.Button(self, image=home_icon, bg="white", activebackground="white", bd=0, command=self.show_devices)
        home_button.image = home_icon # keep a reference to the image to avoid garbage collection
        home_button.pack(pady=10)

        settings_icon = tk.PhotoImage(file="se.png")
        settings_button = tk.Button(self, image=settings_icon, bg="white", activebackground="white", bd=0, command=lambda: self.show_text("Settings"))
        settings_button.image = settings_icon # keep a reference to the image to avoid garbage collection
        settings_button.pack(pady=10)

        help_icon = tk.PhotoImage(file="energ.png")
        help_button = tk.Button(self, image=help_icon, bg="white", activebackground="white", bd=0, command=lambda: self.show_text("Help"))
        help_button.image = help_icon # keep a reference to the image to avoid garbage collection
        help_button.pack(pady=10)

        # Add padding to main content
        self.main_padding = tk.Label(self.master, width=20, bg="#fff")
        self.main_padding.pack(side="right", fill="both", expand=True)

        # Get weather data from API and display it
        weather_data = self.get_weather_data()
        weather_label = tk.Label(self.master, text=weather_data, font=("Arial", 14), bg="#fff")
        weather_label.pack(pady=20)

        # Display weather icon based on current conditions
        if "cloudy" in weather_data.lower():
            weather_icon = tk.PhotoImage(file="cloudy.png")
            weather_image = tk.Label(self.master, image=weather_icon, bg="#fff")
            weather_image.image = weather_icon # keep a reference to the image to avoid garbage collection
            weather_image.pack(pady=10)

    def show_text(self, text):
        self.main_padding.config(text=text)

    def show_devices(self):
        devices = self.scan_network()
        device_list = "\n".join([f"IP Address: {device[0]}, MAC Address: {device[1]}" for device in devices])
        self.main_padding.config(text=device_list)

    def scan_network(self):
        nm = nmap.PortScanner()
        nm.scan(hosts="192.168.1.0/24", arguments="-sP")
        devices = []
        for ip, data in list(nm.all_hosts().items()):
            mac = data['addresses']['mac']
            if mac != '00:00:00:00:00:00':
                devices.append((ip, mac))
        return devices

    def get_weather_data(self):
        # AccuWeather API key and location code
        api_key = "AZlF4zGUbfeEV899ImXlJV0uGNNbqQMg"
        location_code = "1415349" # replace with your own location code

        # URL for current conditions API request
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_code}?apikey={api_key}&details=true"

        # Make API request and get response JSON
        response = requests.get(url)
        data = response.json()

        # Parse JSON to get temperature and weather text
        temperature = data[0]["Temperature"]["Metric"]["Value"]
        weather_text = data[0]["WeatherText"]

        # Create string with weather information
        weather_data = f"Temperatura: {temperature}°C\nPogoda: {weather_text}"

        return weather_data

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Smart Centrum")

    sidebar = Sidebar(root)
    root.mainloop()
