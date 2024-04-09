def lightToBase():
    import time
    
    delay = 5 # delay in seconds
    previousRun = 0
    now = time.time()
    rotateBaseDegrees = 1
    rotateBaseDirection = 'CW'
    rotateCW = True
    
    # Read the light and rotate base if conditions are met
    percentLight = read_Light()
    if (percentLight > rotateBaseLightThreshold) and ((now - previousRun > Delay)):
        previousRun = now
        while(not read_RightLim() or not read_LeftLim()):
            if (rotateCW):
                rotateBaseDirection = 'CW'      # set counterclockwise direction if value is:   True    
            elif (~rotateCW):
                rotateBaseDirection = 'CCW'     # set counterclockwise direction if value is:  not True
                
            rotateBase(rotateBaseLightDegrees, rotateBaseDirection, 's', 'half')
            
        if (read_RightLim() or read_LeftLim()):
            rotateCW = ~rotateCW                # change direction if limit is reached