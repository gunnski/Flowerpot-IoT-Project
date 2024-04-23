import RPi.GPIO as GPIO
from StepperMotor_Class import StepperMotor
import time, AHT20, ADC_PCF8591

from PCF8591_class import PCF8591
import paho.mqtt.client as MyMqtt
import json, time
import requests

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)    # Number GPIOs by header pin locations
GPIO.setwarnings(False)     # Turn of GPIO warnings

pump = False

# Initialize variables and MQTT details
iot_hub = "demo.thingsboard.io"
port = 1883
username = "hb7xsqngvnn93d6stmum"               # <==== Enter your device token from TB here
password = ""
TelemetryTopic = "v1/devices/me/telemetry"
RPCrequestTopic = 'v1/devices/me/rpc/request/+'
AttributesTopic = "v1/devices/me/attributes"

rotateBaseDirection = 'CW'

# This module contains all initializations and functions
# for the smart Flowerpot

# Devices (pins are for the LAB prototype)
WaterLevelPin = 12    # Pin number on the header (GPIO 18)
PumpPin = 36    # Pin number on the header (GPIO 16)
LedPin = 8    # Pin number on the header (UART0 TX)
ButtonPin = 16   # Pin number on the header (GPIO 23)
LeftLim = 7    # Pin number on the header (GPIO 4)
RightLim = 18   # Pin number on the header (GPIO 24)

# Define LED state variable
ledON = False

# Base motor pins
IN1 = 22
IN2 = 24
IN3 = 26
IN4 = 32
MotorPins = [IN1, IN2, IN3, IN4]

# I2C bus connections for ADC and AHT20
bus = 1

# set up the ADC device
ADC_address = 0x48   # ADC board
A0_chan = 0x40       # A0 input    (Light sensor)
A1_chan = 0x41       # A1 input    (Soil misture sensor)
A2_chan = 0x42       # A2 input
A3_chan = 0x43       # A3 input
ADC = ADC_PCF8591.ADC_PCF8591()

# set up AHT20 device for temperature and humidity
AHT20_address = 0x38   # AHT20 sensor board
aht20 = AHT20.AHT20(bus, AHT20_address)

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
GPIO.setwarnings(False)     # Turn of GPIO warnings

# Initialize water level sensor
GPIO.setup(WaterLevelPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin mode as input
# Initialize pump relay
GPIO.setup(PumpPin, GPIO.OUT, initial=GPIO.LOW)   # Set pin mode as output and turn off pump
# Initialize LED
GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.LOW)   # Set pin mode as output and turn off LED
# Initialize Button
GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin mode as input
# Initialize Left limit switch
GPIO.setup(LeftLim, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin mode as input
# Initialize Right limit switch
GPIO.setup(RightLim, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set pin mode as input

# MQTT on_connect callback function
def on_connect(client, userdata, flags, rc):
    print("rc code:", rc)
    client.subscribe(RPCrequestTopic)
    client.publish(AttributesTopic, json.dumps({"PumpRunning": pump}), 1)

# MQTT on_message callback function
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        data = json.loads(msg.payload)
        if data['method'] == 'setValue':
            params = data['params']
            # Turn the pump on/off
            setValue(params)

# Function will set the Pump value
def setValue(params):
    if params == True:
        # Turn pump ON
        GPIO.output(PumpPin, GPIO.HIGH)
        pump = True
        # Update the ClientAttribute "PumpRunning" on the TB dashboard
        client.publish(AttributesTopic, json.dumps({"PumpRunning": pump}), 1)

    elif params == False:
        # Turn pump OFF
        GPIO.output(PumpPin, GPIO.LOW)
        pump = False
        # Update the ClientAttribute "PumpRunning" on the TB dashboard
        client.publish(AttributesTopic, json.dumps({"PumpRunning": pump}), 1)

def button_callback(ButtonPin):
    # Read button
    global ledON
    if GPIO.input(ButtonPin) == False and not ledON:
        # Button was pressed and LED was off
        # Turn LED ON
        print("  turn led ON .............")
        ledON = led_ON()
        time.sleep(1)
    elif GPIO.input(ButtonPin) == False and ledON:
        # Button was pressed and LED was already on
        # Turn LED off
        print("    turn led OFF .............")
        ledON = led_OFF()
        time.sleep(1)
                

# Set up event detection on the ButtonPin.  Signal goes low when button is pressed
GPIO.add_event_detect(ButtonPin, GPIO.FALLING, callback=button_callback, bouncetime=100)


def read_Light():
    # Read light sensor (CH0 of the A/D)
    raw_value = ADC.read(A0_chan)
    # Convert into percentage
    percentLight = round((raw_value/255)*100, 2)
    return percentLight


def read_WaterLevel():
    # Read water level sensor (T/F)
    if GPIO.input(WaterLevelPin):
        return False
    elif not GPIO.input(WaterLevelPin):
        return True
     
     
def read_SoilMoisture():
    # Read soil moisture sensor (CH1 of the A/D)
    raw_value = ADC.read(A1_chan)
    # Convert into percentage
    percentSoilMoisture = round((raw_value/255)*100, 2)
    return percentSoilMoisture


def read_TempHum():
    # Read the temprature and humidity from the AHT20 sensor
    temperature = aht20.get_temperature()
    humidity = aht20.get_humidity()
    return temperature, humidity


def pump_ON():
    # Turn the pump on
    GPIO.output(PumpPin, GPIO.HIGH)
    return True


def pump_OFF():
    # Turn the pump offpump
    GPIO.output(PumpPin, GPIO.LOW)
    return False


def led_ON():
    # Turn the LED on
    GPIO.output(LedPin, GPIO.HIGH)
    return True


def led_OFF():
    # Turn the LED off
    GPIO.output(LedPin, GPIO.LOW)
    return False


def read_LeftLim():
    # Read Left limit switch (T/F)
    if GPIO.input(LeftLim):
        return True
    elif not GPIO.input(LeftLim):
        return False


def read_RightLim():
    # Read Right limit switch (T/F)
    if GPIO.input(RightLim):
        return True
    elif not GPIO.input(RightLim):
        return False


def home_base():
    # Rotate the base until the right limit switch is clicked.
    # Then, rotate back 90 deg to the center of the range
    speed = 's'
    while(not read_RightLim()):
        # rotate the base until the right limit switch is triggered
        rotateBase(1, 'CW', speed, 'full')
    print("Base is at HOME")
    # Move back to center of the range
    print("Moving back to center of the range")
    time.sleep(1)
    rotateBase(90, 'CCW', speed, 'full')
    return True
            


def GPIO_MotorSetup(BaseMotor):
    # Set up the GPIO for Stepper motor
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(BaseMotor.IN1, GPIO.OUT)
    GPIO.setup(BaseMotor.IN2, GPIO.OUT)
    GPIO.setup(BaseMotor.IN3, GPIO.OUT)
    GPIO.setup(BaseMotor.IN4, GPIO.OUT)


def rotateBase(degrees, direction, speed, mode):
    # Rotate the base platform through desired steps in the
    # specified direction
    global MotorPins
    
    #Create the motor and set up pins
    BaseMotor = StepperMotor(MotorPins)
    GPIO_MotorSetup(BaseMotor)
    
    # Motion parameters
    BaseMotor.setDriveMode(mode)
    BaseMotor.dir = direction
    BaseMotor.degrees = float(degrees)
    numSteps = round(abs(BaseMotor.degrees/BaseMotor.DegreesPerStep))
    #print('numSteps = ', numSteps)
    #print('mode = ', BaseMotor.DriveMode)
    
    # Set the speed (delay)
    if speed == 's':
        BaseMotor.StepDelay = 0.015
    elif speed == 'f':
        BaseMotor.StepDelay = 0.002
    
    # Rotate    
    for i in range(numSteps):
        # Write each step pattern to all 4 pins at once. (% (modulo) is used to
        # prevent running out of the number of rows in step sequence)
        if BaseMotor.dir == 'CW':
            GPIO.output(BaseMotor.pins, BaseMotor.seq[i % BaseMotor.mod])
            #print(f"CW, step= {i:<3}, mod= {(i % MotorModulo)}, pins= {MotorSeq[i % MotorModulo]}")
        else:
            GPIO.output(BaseMotor.pins, BaseMotor.seq[-(i+1) % BaseMotor.mod])
            #print(f"CCW, step= {i:<3}, mod= {-(i+1) % MotorModulo}, pins= {MotorSeq[-(i+1) % MotorModulo]}")
        time.sleep(BaseMotor.StepDelay)            

 # Turn off all pins (to prevent heating of the motor and driver)
    GPIO.output(BaseMotor.pins, [0,0,0,0])
    
def getWeather():

    # Weather station at the PDX Airport
    latitude = '45.5958'
    longitude = '-122.6093'
    office = 'PQR'
    gridX = '115'
    gridY = '106'

    # URL and query elements for the NOAA Web site
    base_url = 'https://api.weather.gov/gridpoints/'
    full_url = base_url + office + '/' + gridX + ',' + gridY + '/forecast'


    # GET the response from the NWS server
    WeatherData = requests.get(full_url)
    # print(WeatherData.text)
    

    with open('WeatherData.json', 'r') as f:
        WeatherData = json.load(f)
        
    name = WeatherData['properties']['periods'][0]['name']
    temp = WeatherData['properties']['periods'][0]['temperature']
    value = WeatherData['properties']['periods'][0]['relativeHumidity']['value']
    print(f'Name = {name}, Temp = {temp}, Humidity = {value}')
