# B26 Lab Code
# Last Update: 2/3/15

import serial

class MDT693A:

    def __init__(self, port = 7, baudrate=115200, timeout = .1):
        # The serial connection should be setup with the following parameters:
        # 8 data bits, No parity bit, 1 stop bit, no hardware
        # handshake. These are all default for Serial and therefore not input
        # below
        self.ser = serial.Serial(port = port, baudrate=baudrate, timeout = timeout)

    # get the voltage on the x-axis port of the piezo controller
    def getXVoltage(self):
        assert self.ser.isOpen()

        self.ser.write('XR?\r')
        xVoltage = self.ser.readline()[6:-2].strip()

        return float(xVoltage)

    # get the voltage on the y-axis port of the piezo controller
    def getYVoltage(self):
        assert self.ser.isOpen()

        self.ser.write('YR?\r')
        yVoltage = self.ser.readline()[6:-2].strip()

        return float(yVoltage)

    # get the voltage on the z-axis port of the piezo controller
    def getZVoltage(self):
        assert self.ser.isOpen()

        self.ser.write('ZR?\r')
        zVoltage = self.ser.readline()[6:-2].strip()

        return float(zVoltage)

    # set the voltage on the x-axis port of the piezo controller
    def setXVoltage(self, voltage):
        assert self.ser.isOpen()

        self.ser.write('%s%f\r'%('XV', voltage))
        self.ser.readline()

    # set the voltage on the y-axis port of the piezo controller
    def setYVoltage(self, voltage):
        assert self.ser.isOpen()

        self.ser.write('%s%f\r'%('YV', voltage))
        self.ser.readline()

    # set the voltage on the z-axis port of the piezo controller
    def setZVoltage(self, voltage):
        assert self.ser.isOpen()

        self.ser.write('%s%f\r'%('ZV', voltage))
        self.ser.readline()

    # gets the manual offset on the x axis. This is an additional voltage added to the x axis via the physical front
    # panel knob
    def getXManualOffset(self):
        assert self.ser.isOpen()

        curr_voltage = self.getXVoltage()
        self.setXVoltage(0);
        manualOffset = self.getXVoltage()
        self.setXVoltage(curr_voltage - manualOffset)
        return manualOffset

    # gets the manual offset on the y axis. This is an additional voltage added to the y axis via the physical front
    # panel knob
    def getYManualOffset(self):
        assert self.ser.isOpen()

        curr_voltage = self.getYVoltage()
        self.setYVoltage(0);
        manualOffset = self.getYVoltage()
        self.setYVoltage(curr_voltage - manualOffset)
        return manualOffset

    # gets the manual offset on the z axis. This is an additional voltage added to the z axis via the physical front
    # panel knob
    def getZManualOffset(self):
        assert self.ser.isOpen()

        curr_voltage = self.getZVoltage()
        self.setZVoltage(0);
        manualOffset = self.getZVoltage()
        self.setZVoltage(curr_voltage - manualOffset)
        return manualOffset

    # closes the connection with the controller
    def closeConnection(self):
        self.ser.close()


if __name__ == '__main__':

    controller = MDT693A()
    voltages = [controller.getXVoltage(), controller.getYVoltage(), controller.getZVoltage()]
    print 'The X voltage is ' + str(voltages[0])
    print 'The Y voltage is ' + str(voltages[1])
    print 'The Z voltage is ' + str(voltages[2])

    testVoltages = [5, 10, 15]
    print 'Setting x, y, and z voltages to 5, 10, and 15, respectively...'
    controller.setXVoltage(testVoltages[0])
    controller.setYVoltage(testVoltages[1])
    controller.setZVoltage(testVoltages[2])

    print 'The X voltage is now ' + str(controller.getXVoltage())
    print 'The Y voltage is now ' + str(controller.getYVoltage())
    print 'The Z voltage is now ' + str(controller.getZVoltage())

    print 'Setting Voltages back...'
    controller.setXVoltage(voltages[0])
    controller.setYVoltage(voltages[1])
    controller.setZVoltage(voltages[2])
    currentVoltages = [controller.getXVoltage(), controller.getYVoltage(), controller.getZVoltage()]

    if abs(voltages[0] - currentVoltages[0]) < 1 and abs(voltages[1] - currentVoltages[1]) < 1 and abs(voltages[2] - currentVoltages[2]) < 1:
        print 'Successfully set voltages back to original values'
    else:
        print 'Was not able to set voltages back to original values'

    print 'The x manual offset is ' + str(controller.getXManualOffset())
    print 'The y manual offset is ' + str(controller.getYManualOffset())
    print 'The y manual offset is ' + str(controller.getZManualOffset())

    controller.closeConnection()