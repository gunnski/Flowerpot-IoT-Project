from smbus2 import SMBus
import time

# Class implementation for the PCF8591 Analog to Digital converter board

class ADC_PCF8591:
    
    def __init__(self, BusNum=1, ADC_address=0x48):
        # initialize PCF8591
        self.bus = BusNum
        self.address = ADC_address       
 
        
    def read(self, AI_chan):
        # Read the analog input channel "AI_chan"
        with SMBus(self.bus) as i2c_bus:
            i2c_bus.write_byte(self.address, AI_chan)
            # Dummy read to start conversation.  Otherwise, only one CH is
            # read accurately.
            i2c_bus.read_byte(self.address)
            # Real data reading
            value = i2c_bus.read_byte(self.address)
            time.sleep(0.1)
            return value

        
    

