import pyvisa
from .VISAresourceExtentions import *


class DeviceCommunicator(object):
    def __init__(self):
        self.siggen = ''
        self.siggen_idn = ''
        self.specan = ''
        self.specan_idn = ''

    def connect_generator(self):
        # Connect to instruments
        rm = pyvisa.ResourceManager('@py')
        self.siggen = rm.open_resource('USB0::2733::110::104791::0::INSTR')
        try:

            # siggen = VISA_Instrument(siggen_interface)  #Adjust the VISA Resource string to fit your instrument
            self.siggen.timeout = 3000  # Timeout for VISA Read Operations
            # specan.AddLFtoWriteEnd = false
            self.siggen_idn = self.siggen.query('*IDN?')
            print('\nInstrument Identification string:  ', self.siggen_idn)

        except Exception as e:
            print('\nError initializing the instrument: ', e)

    def connect_analyzer(self):
        # Connect to instruments
        rm = pyvisa.ResourceManager('@py')
        self.specan = rm.open_resource('USB0::2733::205::101274::0')
        try:
            self.specan.timeout = 3000  # Timeout for VISA Read Operations
            self.specan_idn = self.specan.query('*IDN?')
            print('\nInstrument Identification string:  ', self.specan_idn)

        except Exception as e:
            print('\nError initializing the instrument: ', e)

    def set_sweep_mode(self):
        try:
            self.siggen.ext_clear_status()
            self.siggen.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
            self.siggen.ext_error_checking()  # Error Checking after Initialization block
            # -----------------------------------------------------------
            self.siggen.write('FREQuency:MODE SWEep')
            self.siggen.ext_error_checking()  # Error Checking after Basic Settings block
            self.siggen.close()
        except Exception as e:
            print("Error: ", e)

    def set_frequencies_sweep(self, freqs):
        try:
            print("freq sweep: ", freqs)
            self.siggen.ext_clear_status()
            self.siggen.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
            # siggen.Write('OUTPut1:STATe 0')    # Turn off the RF output
            self.siggen.ext_error_checking()  # Error Checking after Initialization block
            # -----------------------------------------------------------
            # self.siggen.write('FREQuency:MODE LIST')
            self.siggen.write('FREQuency:STARt {}'.format(freqs['fstart']))
            self.siggen.write('FREQuency:STOP {}'.format(freqs['fstop']))
            self.siggen.write('FREQuency:SPAN {}'.format(freqs['fstep']))

            self.siggen.write('SWEep:TIME {}'.format(freqs['time']))
            # self.siggen.write('LIST:DWELL {}'.format(freqs['time']))
            self.siggen.ext_error_checking()  # Error Checking after Basic Settings block
            # self.siggen.close()  # Closing the session to the instrument

        except Exception as e:
            print("Error: ", e)

    def set_parameters_freq(self, siggen_freq):
        try:
            print("freq set: ", siggen_freq)
            self.siggen.ext_clear_status()
            self.siggen.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
            # siggen.Write('OUTPut1:STATe 0')    # Turn off the RF output
            self.siggen.ext_error_checking()  # Error Checking after Initialization block
            # -----------------------------------------------------------
            self.siggen.write('SOURce1:FREQuency:CW {}'.format(siggen_freq))  # Setting the output frequency
            self.siggen.ext_error_checking()  # Error Checking after Basic Settings block
            # self.siggen.close()  # Closing the session to the instrument

        except Exception as e:
            print("Error: ", e)

    def set_parameters_power(self, siggen_power):
        try:
            print("power: ", siggen_power)
            self.siggen.ext_clear_status()
            self.siggen.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
            # siggen.Write('OUTPut1:STATe 0')    # Turn off the RF output
            self.siggen.ext_error_checking()  # Error Checking after Initialization block

            self.siggen.write('SOURce1:POWer:POWer {:,}'.format(siggen_power))  # Setting the output frequency
            self.siggen.ext_error_checking()  # Error Checking after Basic Settings block
            # self.siggen.close()  # Closing the session to the instrument

        except Exception as e:
                print("Error: ", e)

    def set_frequencies_analyzer(self, freqs):
        try:
            print("freq sweep: ", freqs)
            self.siggen.ext_clear_status()
            self.siggen.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
            # siggen.Write('OUTPut1:STATe 0')    # Turn off the RF output
            self.siggen.ext_error_checking()  # Error Checking after Initialization block
            # -----------------------------------------------------------
            # self.siggen.write('FREQuency:MODE LIST')
            self.siggen.write('FREQuency:STARt {}'.format(freqs['fstart']))
            self.siggen.write('FREQuency:STOP {}'.format(freqs['fstop']))
            self.siggen.write('FREQuency:SPAN {}'.format(freqs['fstep']))

            # self.siggen.write('LIST:DWELL {}'.format(freqs['time']))
            self.siggen.ext_error_checking()  # Error Checking after Basic Settings block
            # self.siggen.close()  # Closing the session to the instrument

        except Exception as e:
            print("Error: ", e)