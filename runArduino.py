import serial
import webbrowser

ser = serial.Serial('COM7s', 9600, timeout=1)  

while True:
    command = ser.readline().decode().strip()
    if command == "OpenURL":
        # Replace with your local URL
        webbrowser.open('http://127.0.0.1:5000')
