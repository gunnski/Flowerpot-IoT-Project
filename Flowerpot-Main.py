import time
from Flowerpot_Engine import*

# The following global variables pertain to the Light-to-Base-Rotation functionality
start_time = time.time()
end_time = 0
elapsed_time = 0
rotateBaseDelay = 2 # delay of light sensor measurement in seconds
rotateBaseLightThreshold = 50.00 # light sensor threshold for rotating plant base
rotateBaseLightDegrees = 2 # amount of rotation per rotateBaseDelay in degrees
rotateDefaultDirection = True # set the  base rotation direction
rotateBaseDirection = 'CW'
Left_Limit = False
Right_Limit = False

#home_base()
led_ON()


i=0 #seconds that the pump has run
percentSoilMoisture = read_SoilMoisture()

MinSoilMoisture = 10
WaterLevel = read_WaterLevel()
pumpRunTime = 2
maxPumpRunTime = 20
print("Setup Complete")

try:
    while True:
        # rotate base every so often if light value is continously above 50%
        percentLight = read_Light()
        print(percentLight)
        print(start_time)
        elapsed_time = end_time - start_time
        measureLightMillis = start_time
        if (percentLight > rotateBaseLightThreshold) and ((start_time - end_time) > rotateBaseDelay):
            print(elapsed_time)
            print("Proceeding...")

                # rotate base if 1) light, 2) elapsed time, and 3) limit state conditions are met
                # base rotation is always slow here and in half-step mode
                
            rotateBase(rotateBaseLightDegrees, rotateBaseDirection, 's', 'half')
            print('rotating')
            print(rotateBaseDirection)
                
            Left_Limit = read_LeftLim()
            Right_Limit = read_RightLim()
            
            if (Left_Limit or Right_Limit):
                if (rotateDefaultDirection):
                    rotateBaseDirection = 'CCW'   # set counterclockwise direction if value is:   True
                    rotateDefaultDirection = ~rotateDefaultDirection
                elif (~rotateDefaultDirection):
                    rotateBaseDirection = 'CW'  # set counterclockwise direction if value is:  not True
                    rotateDefaultDirection = ~rotateDefaultDirection # change direction if limit is reached
        else:
            end_time = time.time()
            elapsed_time = 0
            print(elapsed_time)
            time.sleep(5)
        
        
    #     # Moisture Control part
    #     if (percentSoilMoisture < MinSoilMoisture) and (i < maxPumpRunTime):  #change the 20 and the 10
    #         pump_ON()
    #         sleep(pumpRunTime) #might need to change the 2 seconds
    #         pump_OFF()
    #         sleep()
    #         i=i+pumpRunTime
    #         print(f'The pump has run for {i} seconds')
    #     if (i > maxPumpRunTime) or (WaterLevel == "empty"):  #change the 20
    #         print('The resevoir needs to be refilled')
    #         i=0


except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nBye...')
