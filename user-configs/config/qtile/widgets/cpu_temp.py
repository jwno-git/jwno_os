from libqtile.widget import base

class CPUTempWidget(base.ThreadPoolText):
    def __init__(self, high_temp=75, high_foreground="#FF6B6B", caution_temp=65, caution_foreground="#FFD700", **config):
        super().__init__("", **config)
        self.high_temp = high_temp
        self.caution_temp = caution_temp
        self.high_foreground = high_foreground
        self.caution_foreground = caution_foreground
        self.normal_foreground = config.get('foreground', '#FFFFFF')
        
    def poll(self):
        try:
            with open('/sys/class/hwmon/hwmon5/temp1_input', 'r') as f:
                temp_raw = int(f.read().strip())
            temp_celsius = temp_raw / 1000
            
            # Change text color based on temperature
            temp_text = f"{temp_celsius:.1f}°C"
            
            if temp_celsius > self.high_temp:
                # Hot temperature - return colored text
                return f'<span color="{self.high_foreground}">{temp_text}</span>'
            elif temp_celsius > self.caution_temp:
                return f'<span color="{self.caution_foreground}">{temp_text}</span>'
            else:
                # Normal temperature
                return temp_text
                
        except Exception as e:
            return "ERROR"
