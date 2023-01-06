import pyvisa as visa
from time import sleep



class AMI430:
    def __init__(self, addr):
        self._inst = visa.ResourceManager('@py').open_resource(addr)
        self._inst.read_termination = "\r\n"
        print(self._read())
        print(self._read())

    ##############################
    # Attributes
    ##############################

    @property
    def coil_constant(self):
        return self.query("COIL?")

    @coil_constant.setter
    def coil_constant(self, const):
        self._write("CONF:COIL {}".format(const))

    @property
    def voltage_limit(self):
        self._voltage_limit = self._query("VOLT:LIM?")
        return self._voltage_limit

    @voltage_limit.setter
    def voltage_limit(self, lim):
        self._write("CONF:VOLT:LIM {}".format(lim))

    @property
    def target_current(self):
        return self._query("CURR:TARG?")

    @target_current.setter
    def target_current(self, curr):
        #TODO: exception for out of range of magnets
        self._write("CONF:CURR:TARG {}".format(curr))

    @property
    def target_field(self):
        return self._query("FIELD:TARG?")

    @target_field.setter
    def target_field(self, field):
        self._write("CONF:FIELD:TARG {}".format(field))
    @property
    def ramp_rate_units(self):
        return self._query("RAMP:RATE:UNITS?")

    @ramp_rate_units.setter
    def ramp_rate_units(self, units):
        if units == "seconds" or units == 0:
            self._write('CONFigure:RAMP:RATE:UNITS {}'.format(0))
        elif units == "minutes" or units == 1:
            self._write('CONFigure:RAMP:RATE:UNITS {}'.format(1))

    @property
    def field_units(self):
        return self._query("FIELD:UNITS?")

    @field_units.setter
    def field_units(self, units):
        if units == "kilogauss" or units == 0:
            self._write('CONFigure:FIELD:UNITS {}'.format(0))
        elif units == "tesla" or units == 1:
            self._write('CONFigure:FIELD:UNITS {}'.format(1))

    @property
    def magnet_current(self):
        return self._query("CURR:MAG?")

    @property
    def supply_current(self):
        return self._query("CURR:SUPP?")

    @property
    def magnetic_field(self):
        return self._query("FIELD:MAG?")

    @property
    def state(self):
        STATES = {
            1: "RAMPING",
            2: "HOLDING",
            3: "PAUSED",
            4: "MANUAL UP",
            5: "MANUAL DOWN",
            6: "ZEROING CURRENT",
            7: "QUENCH detected",
            8: "AT ZERO CURRENT",
            9: "Heating Persistent Switch",
            10: "Cooling Persistent Switch"
        }
        return STATES[int(self._query("STATE?"))]

    ##############################
    # Methods
    ##############################

    def ramp_rate_field(self, segment):
        return self._query("RAMP:RATE:FIELD {}?".format(segment))

    def ramp_rate_field(self, segment, rate):
        self._write('CONFigure:RAMP:RATE:FIELD {} {}'.format(segment, rate))

    def identify(self):
        return self._query("*IDN?")

    def operation_complete(self):
        return self._query("*OPC?")

    def ramp(self):
        self._write('ramp')

    def pause(self):
        self._write('pause')

    def zero(self):
        self._write('zero')


    # def set_field(self):
    #
    # def set_current(self):
    #
    # def shutdown(self):
    #     # set current to zero
    #     #

    ##############################
    # Methods that send commands
    ##############################
    def _write(self, cmd):
        self._inst.write(cmd)

    def _read(self):
        return self._inst.read()

    def _query(self, cmd):
        return self._inst.query(cmd)

if __name__ == "__main__":
    #TODO: get addresses of magnets using *IDN?
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    for resource in resources:
        print('address: {}:\nname: {}'.format(resource, rm.open_resource(resource).query('*IDN?')))


    mag = AMI430("TCPIP0::192.168.0.41::7180::SOCKET")
    mag.target_current = 5
    mag.ramp_rate_current = 0.03
    mag.ramp()
    while mag.state != "HOLDING":
        sleep(5)
    print('Target field reached')
    mag.target_current = 0
    mag.ramp()
    while mag.state != "HOLDING":
        sleep(5)
    print('Magnet turned off')