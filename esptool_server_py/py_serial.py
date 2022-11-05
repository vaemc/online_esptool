import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

serial_ports=[]
for port, desc, hwid in sorted(ports):
        try:
            s = serial.Serial(port)
            s.close()
            serial_ports.append(port)
        except (OSError, serial.SerialException):
            pass
for port in serial_ports:
    print(port)
