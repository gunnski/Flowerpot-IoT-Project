

class StepperMotor:
    '''
    For 28BYJ-48 stepper motor with 1/64 gear reduction and ULN2003 driver.
    '''
    
    def __init__(self, MotorPins=[22, 24, 26, 32]):
        self.GearRatio = 64
        self.StepAngle = 5.625
        self.IN1 = MotorPins[0]
        self.IN2 = MotorPins[1]
        self.IN3 = MotorPins[2]
        self.IN4 = MotorPins[3]
        self.dir = 'CW'
        self.StepDelay = 0.015
        self.degrees = 90
        self.DriveMode = 'full'
        self.mod = 4
    
    
    def setDriveMode(self, mode):
        if mode == 'full':
            self.DriveMode = 'full'
            self.mod = 4
            self.seq = [[1,1,0,0],
                        [0,1,1,0],
                        [0,0,1,1],
                        [1,0,0,1]]
        elif mode == 'wave':
            self.DriveMode = 'wave'
            self.mod = 4
            self.seq = [[0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1],
                        [1,0,0,0]]
        elif mode == 'half':
            self.DriveMode = 'half'
            self.mod = 8
            self.seq = [[1,0,0,1],
                         [1,0,0,0],
                         [1,1,0,0],
                         [0,1,0,0],
                         [0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,1]]            
            

    # Computed properties
    @property
    def StepsPerMotorShaftRev(self):
        return 360/self.StepAngle


    @property
    def pins(self):
        return [self.IN1, self.IN2, self.IN3, self.IN4]


    @property
    def DegreesPerStep(self):
        if self.GearRatio == 0:
            self.GearRatio = 1    # In case it was set to zero for a motor with no gearbox
        
        # steps needed for 1 revolution of the output shaft
        if self.DriveMode == 'full' or self.DriveMode == 'wave':
            self.StepsPerOutputRev = 0.5 * self.GearRatio * self.StepsPerMotorShaftRev
        else:
            self.StepsPerOutputRev = self.GearRatio * self.StepsPerMotorShaftRev
        return 360/self.StepsPerOutputRev
        
 