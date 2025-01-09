import pyvisa

class MercuryiTC:
    def _init_(self, resource_name="ASRL4::INSTR"):
        rm = pyvisa.ResourceManager()
        INSTR_ID = "IDN:OXFORD INSTRUMENTS:MERCURY ITC:224550324:2.6.04.000\n"
        try:
            self.instr = rm.open_resource(resource_name)
        except Exception as e:
            print(f"Error connecting to the instrument, the following exception has been raised:\n{e}")
            exit()
        try:
            response = self.instr.query('*IDN?')
            if response != INSTR_ID:
                print(f"Initialized instrument was {response}, not {INSTR_ID}")
                exit()
        except TimeoutError as e:
            print(f"There has been a problem stablishing communication with the instrument. The following exception has been raised:\n{e}")
            exit()
        print("Connection succesful")

    def query_temperature(self):
        return self.instr.query('READ:DEV:MB1.T1:TEMP:SIG:VOLT')
        
def query_mercury(mercury: MercuryiTC):
    return mercury.query_temperature()
