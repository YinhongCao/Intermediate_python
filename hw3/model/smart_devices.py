import json, abstractmethod
class Home:
    def __init__(self, address):
        self.address = address
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def print_devices(self):
        for device in self.devices:
            print(device.name)


class SmartDevice:
    def __init__(self, name, manufacturer):
        self.name = name
        self.manufacturer = manufacturer

    @abstractmethod
    def to_json(self):
        pass
    

class LightBulb(SmartDevice):
    def __init__(self, name, manufacturer, brightness):
        SmartDevice.__init__(self, name, manufacturer)
        self.brightness = brightness

    def adjust_brightness(self, value):
        self.brightness = value
        print("Brightness is set to "+str(value))

    def to_json(self):
        return json.dumps(self.__dict__)