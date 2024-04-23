import time
import csv
import datetime
from Flowerpot_Engine import*

from PCF8591_class import PCF8591
import paho.mqtt.client as MyMqtt
import json, time




# Initialize GPIO
GPIO.setmode(GPIO.BOARD)    # Number GPIOs by header pin locations
GPIO.setwarnings(False)     # Turn of GPIO warnings

# Initialize variables and MQTT details
iot_hub = "demo.thingsboard.io"
port = 1883
username = "hb7xsqngvnn93d6stmum"               # <==== Enter your device token from TB here
password = ""
TelemetryTopic = "v1/devices/me/telemetry"
RPCrequestTopic = 'v1/devices/me/rpc/request/+'
AttributesTopic = "v1/devices/me/attributes"

client = MyMqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)
client.connect(iot_hub, port)
client.loop_start()
print("Connection successful")

lightThreshold = 20 # light sensor threshold in percent (%)
rotateBaseDirection = 'CW' # Set initial direction to clockwise
rotateBaseDegrees = 5 # Base rotation amount per interval; keep this amount low

baseDelay = 10 # delay for checking the light to run base rotation
pumpDelay = 30 # delay for checking the moisture to run pump
DataDelay = 4


previousBaseRun = time.time() # Initialize; for checking if base rotation functions should occur
previousPumpRun = time.time() # Initialize; for checking if pump functions should occur
previousDataDump = time.time()

now = time.time() # Initialize current time
currenttime = datetime.datetime.now() # UTC to local time

totalPumpTime = 0 # seconds that the pump has run; for measuring if water needs refilled
maxPumpTime = 100 # when the pump theoretically runs out of water
pumpRunTime = 4 # Amount of time the pump will run per interval
pump = False

moistureThreshold = 80 # Threshold value for soil moisture

# Check that there is water in the tank before proceeding
# waterLevel = read_WaterLevel()
# while (waterLevel == "empty"):
#     print("Please add water to continue.")
#     time.sleep(2)
#     waterLevel = read_WaterLevel()

# print("Homing base...")
# led_ON()
# home_base()
# led_OFF()
# time.sleep(1)

print("Startup is complete. \n Times up! Let's do this!")

try:
    i=1
    while True:
        now = time.time() # Update now time
        # print(now)
        percentLight = read_Light() # Read the light value
        print("read light")
        print(percentLight)
        
        percentSoilMoisture = read_SoilMoisture() # read the soil moisture
        print("read moisture")
        print(percentSoilMoisture)
        
        waterLevel = read_WaterLevel() # read the water level sensor
        print("read water level")
        print(waterLevel)
        
        temperature, humidity = read_TempHum()
        print("Temperature: ")
        print(temperature)
        print("Humidity: ")
        print(humidity)
        
        # Check to run the base rotation
        if (percentLight > lightThreshold) and ((now - previousBaseRun > baseDelay)):
            previousBaseRun = now
            # Check if limits have been reached
            if(read_RightLim() or read_LeftLim()):
                print("Limit Reached")
                
                # If so, flip/flop rotation direction
                if (rotateBaseDirection == 'CCW'):
                    rotateBaseDirection = 'CW'
                    rotateBase(10, rotateBaseDirection, 's', 'half') # Back off the limit switch
                elif (rotateBaseDirection == 'CW'):
                    rotateBaseDirection = 'CCW'
                    rotateBase(10, rotateBaseDirection, 's', 'half') # Back off the limit switch
            else:
                print("Rotating...")
                rotateBase(rotateBaseDegrees, rotateBaseDirection, 's', 'half') # rotate base per defined variables
        else:
            print("base skipped")
                
        # Check to run the pump
        
        if (percentSoilMoisture < moistureThreshold) and ((now - previousPumpRun > pumpDelay)): 
            # Moisture Control part

            if (totalPumpTime > maxPumpTime) or (waterLevel == False):
                print('The resevoir needs to be refilled')
                print("pump skipped")
                pump = False
            elif (pump == True):
                pump = False
            else:
                print("Pumping...")
                previousPumpRun = now
                pump_ON()
                pump = True
                time.sleep(pumpRunTime)
                pump_OFF()
                
                totalPumpTime = totalPumpTime + pumpRunTime
                print(f'The pump has run for {totalPumpTime} seconds')
        else:
            print("pump skipped")
            pump = False
            
        if ((now - previousDataDump) > DataDelay):
            currenttime = datetime.datetime.now() # UTC to local time
            previousDataDump = now
            # Convert data into JSON to send to MQTT server
            # First format data as a dictionary
            data_out = {"Packet":i, "Light":percentLight, "Temperature":temperature, "humidity": humidity, "Moisture": percentSoilMoisture, "Water Level":waterLevel, "Pump Time": totalPumpTime, "PumpRunning": pump}
            print("data_out=",data_out)
            JSON_data_out = json.dumps(data_out)    # Convert to JSON format
            All_data = {"Packet":i, "Light":percentLight, "Temperature":temperature, "humidity": humidity, "Moisture": percentSoilMoisture, "Water Level":waterLevel, "Pump Time": totalPumpTime, "PumpRunning": pump, "CurrentTime": currenttime}
            # open the file in the write mode
            f = open('/home/pi/Downloads/flowerpot.csv', 'a')
            # create the csv writer
            writer = csv.writer(f)
            writer.writerow(All_data)
            writer.writerow(All_data.values())
            
            getWeather()
            # print(f'Name = {name}, Temp = {temp}, Humidity = {value}')
            
            # Publish data to MQTT server
            client.publish(TelemetryTopic, JSON_data_out, 0)
            time.sleep(3)
            print('---------------------------')
            i=i+1
                
            time.sleep(1)
        
        time.sleep(1)
       
except KeyboardInterrupt:
    pump_OFF()
    GPIO.cleanup()
    print('\nBye...')
    
