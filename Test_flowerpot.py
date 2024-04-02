import time
from Flowerpot_Engine import*


# This program is for testing all functions of the smart flowerpot


try:   
    # Read light sensor (CH0 of the A/D)
    ans = input('\nRead light sensor (y/n)? ')
    if ans == 'y':
        for i in range(5):
            Light = read_Light()
            print (f'Light = {Light:0.2f}')
            time.sleep(1)
    
    # Read water level
    ans = input('\nRead water level sensor (y/n)? ')
    if ans == 'y':
        for i in range(5):
            waterLevel = read_WaterLevel()
            print(f'Water level: {waterLevel}')
            time.sleep(1)
        
    # Read soil moisture
    ans = input('\nRead soil moisture (y/n)? ')
    if ans == 'y':    
        for i in range(5):    
            SoilMoisture = read_SoilMoisture()
            print (f'Soil = {SoilMoisture:0.2f}')
            time.sleep(1)
    
    # Read temp and humidity
    ans = input('\nRead temp and humidity sensor (y/n)? ')
    if ans == 'y':    
        for i in range(5):        
            temp, hum = read_TempHum() 
            print(f'temperature = {temp:.2f} F,  humidity = {hum:.2f}%')
            time.sleep(1)
       
    # Turn pump on for short period
    ans = input('\nTurn pump on (y/n)? ')
    if ans == 'y':
        pumpRunning = pump_ON()
        time.sleep(0.5)
        pumpRunning = pump_OFF()
        
    # Test Left limit switch
    ans = input('\nTest LEFT limit switch (y/n)? ')
    if ans == 'y':
        for i in range(5):
            L_Lim = read_LeftLim()
            if L_Lim == True:
                print("Left switch is ON")
            else:
                print("Left switch is OFF")
            time.sleep(1)

    # Test Right limit switch
    ans = input('\nTest RIGHT limit switch (y/n)? ')
    if ans == 'y':
        for i in range(5):
            R_Lim = read_RightLim()
            if R_Lim == True:
                print("Left switch is ON")
            else:
                print("Left switch is OFF")
            time.sleep(1)

    
    # Home the base
    ans = input('\nReady to home the base (on right limit) (y/n)? ')
    if ans == 'y':
        while(not home_base()):
            # Wait until the base is at home position
            pass


    # Check LED and button
    ans = input('\nCheck the button and LED (y/n)? ')
    if ans == 'y':
        ledON = led_OFF()
        while True:
            # Loop to read button and turn LED on/off
            print("Click the button ...")
            time.sleep(1)

        
except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nBye...')
    