import time
from Flowerpot_Engine import*

# The following global variables pertain to the Light-to-Base-Rotation functionality
measureLightMillis = millis()
rotateBaseDelay = 60 # delay of light sensor measurement in seconds
rotateBaseLightThreshold = 50.00 # light sensor threshold for rotating plant base
rotateBaseLightDegrees = 1 # amount of rotation per rotateBaseDelay in degrees
rotateDefaultDirection = True # set the  base rotation direction
rotateBaseDirection = 'CW'
Left_Limit = False
Right_Limit = False

home_base()
led_ON()

try:
    # rotate base every so often if light value is continously above 50%
    percentLight = read_Light()
    if (percentLight > rotateBaseLightThreshold) and ((measureLightMillis - milis()) > rotateBaseDelay):
        Left_Limit = read_LeftLim()
        Right_Limit = read_RightLim()
        if (~LeftLimit and ~RightLimit):
            if (rotateDefaultDirection):
                rotateBaseDirection = 'CW'   # set counterclockwise direction if value is:   True
            elif (~rotateDefaultDirection):
                rotateBaseDirection = 'CCW'  # set counterclockwise direction if value is:  not True
            # rotate base if 1) light, 2) elapsed time, and 3) limit state conditions are met
            # base rotation is always slow here and in half-step mode
            rotateBase(rotateBaseLightDegrees, rotateBaseDirection, 's', 'half')
        else:
            rotateDefaultDirection = ~rotateDefaultDirection # change direction if limit is reached
    else:
        measureLightMillis = millis()



except KeyboardInterrupt:
    GPIO.cleanup()
    print('\nBye...')
