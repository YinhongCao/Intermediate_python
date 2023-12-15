import json
class Home:
    def __init__(self, address, path):
        self.address = address
        self.file_path = path
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def print_devices(self):
        for device in self.devices:
            print(device.name)
    
    def delete(self, name, location):
        for i in range(len(self.devices)):
            device = self.devices[i]
            if (device.name == name) and (device.location == location):
                self.devices.pop(i)
                return
        print("There was no device to remove")

    def switch_power(self, name, location):
        for device in self.devices:
            if (device.name == name) and (device.location == location):
                device.flip_power()

    def to_json(self):
        json_str = json.dumps(self.__dict__)
        return json_str
    
    def save(self):
        with open(self.file_path,"w") as file_path :
            json.dump(self.to_json(), file_path)


class SmartDevice:
    def __init__(self, location, name, power):
        self.name = name
        self.location = location
        self.power = power

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def flip_power(self):
        self.power = not self.power
    
    def get_location(self):
        return self.location
    
class LightBulb(SmartDevice):
    def __init__(self, location, name, power):
        SmartDevice.__init__(self, location, name, power)
        self.brightness = 7

    def adjust_brightness(self, value):
        self.brightness = value
        print("Brightness is set to "+str(value))


class Thermostat(SmartDevice):
    def __init__(self, location, name, power):
        SmartDevice.__init__(self, location, name, power)
        self.temp = 71
        self.humidity = "35%"

    def get_temperature(self):
        return self.temp
    
class SmartVacuum(SmartDevice):
    def __init__(self, location, name, power):
        SmartDevice.__init__(self, location, name, power)
        self.working = False


