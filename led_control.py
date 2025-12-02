import serial as ser
import numpy as np
import drawnow as dn
import matplotlib.pyplot as plt
from time import sleep

# serial argument
port  = "COM9"
baudrate = 115200
timeout = 1.0

# graphing variables
pot_values = []
brightness = []
MAX_ADC = 1023.0
MAX_PWM = 225.0
counter = 0

# This function graphs the data received
def graph():
    plt.title("Brightness Vs. Potentiometer values")
    plt.grid(True)

    plt.xlim(0.0,MAX_ADC)
    plt.xlabel("Potentiometer values")

    plt.ylim(0.0,MAX_PWM)
    plt.ylabel("Led Brightness")

    plt.plot(np.array(pot_values),np.array(brightness),'ro--',label="y=0.2493x")
    plt.legend(loc="upper left")

while True:
    try:
        # initialize the serial communication
        arduino_serial_data = ser.Serial(port, baudrate, timeout=timeout)
        plt.ion()
        break

    except ser.SerialException:
        print("Unable to connect to serial. Trying again..")
        sleep(2)

arduino_serial_data.reset_input_buffer()
sleep(2)
print("Serial connected.\nSerial ok")

try:
    while True:
        if arduino_serial_data.in_waiting >= 0:
            arduino_data = float(arduino_serial_data.readline().decode("utf-8").strip())
            print(f"Data recieved: {arduino_data}")
            pot_values.append(arduino_data)
            led_intensity = (MAX_PWM/MAX_ADC) * arduino_data
            brightness.append(led_intensity)
            dn.drawnow(graph)
            plt.pause(0.0001)
            counter += 1

        # pops the first value added to the list if current items in list exceeds 50
        if counter > 50:
            pot_values.pop(0)
            brightness.pop(0)

except KeyboardInterrupt:
    print("Communication closed")
    arduino_serial_data.close()