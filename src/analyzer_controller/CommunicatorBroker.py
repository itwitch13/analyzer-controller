import pyvisa
from .VISAresourceExtentions import *

# rm = pyvisa.ResourceManager('@py')
# print("rm: ", rm)
# list_resources = rm.list_resources()
# print("resources: ", list_resources)


# Script settings
ENABLE_SIGGEN = True
# ENABLE_SPECAN = True

siggen_interface = 'TCPIP::169.254.2.20::hislip0::INSTR'  # R%S SMF 100A
specan_interface = 'USB0::2733::205::101274::0'  # R%S FSW 85
vectan_interface = 'TCPIP::169.254.161.151::hislip0::INSTR'  # R%S ZNB 40

ENABLE_DATA_SAVE = True
f_Path_save = ''
f_Name_base = 'test_spectrum'

siggen_freq = 30000
siggen_power = 10          # power level in dBm

specan_start_freq = 20e9   # start frequency in Hz
specan_stop_freq = 85e9    # stop frequency in Hz
specan_step_freq = 20e6    # step frequency in Hz
specan_rbw = 50e3          # resolution bandwidth in Hz
specan_ref_level = 10.0    # ref level in dBm
specan_sweep_timeout_ms = 20000


# Connect to instruments
rm = pyvisa.ResourceManager('@py')
siggen = rm.open_resource('USB0::2733::110::104791::0::INSTR')

if ENABLE_SIGGEN == True:
    try:

        # siggen = VISA_Instrument(siggen_interface)  #Adjust the VISA Resource string to fit your instrument
        siggen.timeout = 3000   # Timeout for VISA Read Operations
        # specan.AddLFtoWriteEnd = false
        siggen_idn = siggen.query('*IDN?')
        print('\nInstrument Identification string:  ', siggen_idn)

    except Exception as e:
        print('\nError initializing the instrument: ', e)


# Set power and frequency, read the spectrum
try:
    # generator settings
    # siggen_freq = 40e9        # frequency in GHz
    # siggen_power = 10         # power level in dBm
    siggen.ext_clear_status()
    siggen.write('*RST;*CLS')   # Reset the instrument, clear the Error queue
    # siggen.Write('OUTPut1:STATe 0')    # Turn off the RF output
    siggen.ext_error_checking()      # Error Checking after Initialization block
    # -----------------------------------------------------------
    # Basic Settings:
    # -----------------------------------------------------------
    siggen.write('SOURce1:FREQuency:CW {}'.format(siggen_freq))     # Setting the output frequency
    print("freq set: ", siggen_freq)
    siggen.write('SOURce1:POWer:POWer {:,}'.format(siggen_power))     # Setting the output frequency
    # print("power: ", siggen_power)
    # siggen.write('OUTPut1:STATe 1{}'.format(siggen_power))              # Turn on the RF output
    #     specan.QueryString('*OPC?')            # Using *OPC? query waits until the instrument finished

    siggen.ext_error_checking()        # Error Checking after Basic Settings block

    siggen.close()                  # Closing the session to the instrument

# Error handling
except Exception as e:
    print("Error: ", e)
