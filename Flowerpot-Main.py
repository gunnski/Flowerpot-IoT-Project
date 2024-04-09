import time
from Flowerpot_Engine import*

LightThreshold = 20 # light sensor threshold in percent (%)
rotateBaseDirection = 'CW' # Set initial direction to clockwise
rotateBaseDegrees = 1 # Base rotation amount per interval; keep this amount low

baseDelay = 60 # delay for checking the light to run base rotation
pumpDelay = 60 # delay for checking the moisture to run pump

previousBaseRun = time.time() # Initialize; for checking if base rotation functions should occur
previousPumpRun = time.time() # Initialize; for checking if pump functions should occur

now = time.time() # Initialize current time

totalPumpTime = 0 # seconds that the pump has run; for measuring if water needs refilled
maxPumpTime = 20 # when the pump theoretically runs out of water
pumpRunTime = 1 # Amount of time the pump will run per interval

MoistureThreshold = 90 # Threshold value for soil moisture

# Check that there is water in the tank before proceeding
waterLevel = read_WaterLevel()
while (waterLevel == "empty"):
    print("Please add water to continue.")
    time.sleep(2)
    waterLevel = read_WaterLevel()

print("Homing base...")
led_ON()
home_base()
led_OFF()
sleep.time(1)

print("Startup is complete. \n Times up! Let's do this!")

try:
    while True:
        now = time.time() # Update now time
        # print(now)
        percentLight = read_Light() # Read the light value
        # print("read light")
        # print(percentLight)
        # Check elpased time for base rotation funtion
        percentSoilMoisture = read_SoilMoisture() # read the soil moisture
        # print("read moisture")
        # print(percentSoilMoisture)
        waterLevel = read_WaterLevel() # read the water level sensor
        # print("read water level")
        # print(WaterLevel)
        
        # Check to run the base rotation
        if (percentLight > LightThreshold) and ((now - previousBaseRun > baseDelay)):
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
                
        # Check to run the pump
        if (percentSoilMoisture > MoistureThreshold) and ((now - previousPumpRun > pumpDelay)) and (waterLevel == "full"):
            # Moisture Control part
            print("Pumping...")
            pump_ON()
            time.sleep(pumpRunTime)
            pump_OFF()
            totalPumpTime = totalPumpTime + pumpRunTime
            print(f'The pump has run for {i} seconds')

            if (totalPumpTime > maxPumpTime) or (waterLevel == "empty"):
                print('The resevoir needs to be refilled')    
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nBye...')
    
