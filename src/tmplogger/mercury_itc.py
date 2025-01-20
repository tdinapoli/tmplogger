import logging

import pyvisa


class MercuryiTC:
    def __init__(
        self,
        port="ASRL/dev/ttyACM0::INSTR",
        expected_id="IDN:OXFORD INSTRUMENTS:MERCURY ITC:224550324:2.6.04.000\n",
    ):
        rm = pyvisa.ResourceManager("@py")
        self.EXPECTED_INSTR_ID = expected_id
        self.instr = None

        try:
            self.instr = rm.open_resource(port)
            response = self.instr.query("*IDN?")
            if response.strip() != self.EXPECTED_INSTR_ID.strip():
                raise ValueError(f"Unexpected instrument ID: {response.strip()}")
            logging.info("Connection succesful.")
        except (pyvisa.VisaIOError, TimeoutError) as e:
            logging.error(
                f"Failed to connect to or communicate with the instrument: {e}"
            )
            raise
        except Exception as e:
            logging.error(f"An unexpected erorr ocurred during initialization: {e}")
            raise

    def query_temperature(self):
        try:
            response = self.instr.query("READ:DEV:MB1.T1:TEMP:SIG:TEMP")
            logging.info(f"Querying temperature: {response.strip()}")
            return response.strip().split(":")[-1][:-1]
        except (pyvisa.VisaIOError, TimeoutError) as e:
            logging.error(f"Error querying temperature: {e}")
            raise


def query_mercury(mercury: MercuryiTC):
    return mercury.query_temperature()
