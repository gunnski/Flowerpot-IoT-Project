import time
from Flowerpot_Engine import*

ElapsedPumpTime=0 #seconds that the pump has run

percentSoilMoisture = read_SoilMoisture()
MinSoilMoisture = 25
WaterLevel = read_WaterLevel()
pumpRunTime = 2
maxPumpRunTime = 20
while True:
    print(percentSoilMoisture)
    
    if (percentSoilMoisture < MinSoilMoisture) and (ElapsedPumpTime < maxPumpRunTime):  #change the 20 and the 10
        pump_ON()
        time.sleep(pumpRunTime) #might need to change the 2 seconds
        pump_OFF()
        time.sleep(1)
        ElapsedPumpTime = ElapsedPumpTime + pumpRunTime
        print(f'The pump has run for {ElapsedPumpTime} seconds')
        
    time.sleep(1)
    
    # if (i > maxPumpRunTime) or (WaterLevel == "empty"):  #change the 20
    #     print('The resevoir needs to be refilled')
    #     i=0

    