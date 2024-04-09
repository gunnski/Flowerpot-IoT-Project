import time
from Flowerpot_Engine import*

#home_base()
led_ON()

delay = 60 # delay in seconds
rotateBaseDirection = 'CW'
rotateBaseDegrees = 1

previousRun = time.time()
now = time.time()

rotateBaseLightThreshold = 20

i=0 #seconds that the pump has run


MinSoilMoisture = 90
WaterLevel = read_WaterLevel()
pumpRunTime = 1
maxPumpRunTime = 20



print("Setup Complete")

try:
    while True:
    
        percentLight = read_Light()
        # print("read light")
        # print(percentLight)
        
        now = time.time()
        # print(now)
        
        # Check elpased time for base rotation funtion
        if (percentLight > rotateBaseLightThreshold) and ((now - previousRun > delay)):
            previousRun = now
            # print(previousRun)
            if(read_RightLim() or read_LeftLim()):
                print("limit reached")
                if (rotateBaseDirection == 'CCW'):
                    rotateBaseDirection = 'CW'
                    
                    rotateBase(10, rotateBaseDirection, 's', 'half')
                    
                elif (rotateBaseDirection == 'CW'):
                    rotateBaseDirection = 'CCW'

                    rotateBase(10, rotateBaseDirection, 's', 'half')
                
            else:
                print("rotating")
                
                rotateBase(rotateBaseDegrees, rotateBaseDirection, 's', 'half')

        percentSoilMoisture = read_SoilMoisture()
        print(percentSoilMoisture)
        # Moisture Control part
        if (percentSoilMoisture < MinSoilMoisture) and (i < maxPumpRunTime):
            pump_ON()
            time.sleep(pumpRunTime)
            pump_OFF()
            time.sleep(2)
            i=i+pumpRunTime
            print(f'The pump has run for {i} seconds')
            
        if (i > maxPumpRunTime) or (WaterLevel == "empty"):
            
            print('The resevoir needs to be refilled')
            i=0

except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nBye...')
    
