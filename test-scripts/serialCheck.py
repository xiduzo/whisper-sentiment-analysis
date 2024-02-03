import os, pty, serial

main, sub = pty.openpty()
s_name = os.ttyname(sub)

ser = serial.Serial(s_name, 9600, timeout=1)

# To Write to the device
ser.write('Your text'.encode('utf-8'))

# To read from the device
os.read(main,1000)