import serial
import requests
import time

SERIAL_PORT = 'COM5'
BAUD_RATE = 9600

import requests

webhook_url = "https://discordapp.com/api/webhooks/1363216654384893982/MbCTx0PAE11kxja6dpg_8tN6y9q-DKhks9UD6eEkjsy3MHcfocaqICFlQTDj-GhzUbSS"

# Your message

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10)
time.sleep(2)   # Let Arduino reset

print("Monitoring Arduino...")


# DISTANCE_THRESHOLD = 100  # cm
TEMP_THRESHOLD = 70.0 # f
monitor = True
while monitor:
    try:

        line = ser.readline().decode('utf-8').strip()
        print(line)
        if not line:
            print("⏳ (empty line) - waiting for data...")
        if line.startswith("Temperature:"):
            print("caught")
            # Parse "Distance:123,Temp:25.4"    
            parts = line.split(',')
            print(parts)
            temp = float(parts[0].split(':')[1])
            print(temp)
            distance = float(parts[1].split(':')[1])
            print(distance)
            lights = bool(parts[2].split(':')[1])
            print(lights)

            print(f"Distance: {distance} cm | Temp: {temp} °F")
            

            # Trigger condition: empty room + hot
            if temp > TEMP_THRESHOLD or temp < 60 and distance == 0:
                message = {
                    "content": f"🚨 **Room Alert!**\nRoom is empty and temp is {temp:.1f}°F and lights are {lights}"
                }
                response = requests.post(webhook_url, json=message)
                if response.status_code == 204:
                    print("✅ Sent alert to Discord.")
                else:
                    print(f"❌ Discord Error: {response.status_code} - {response.text}")
                
                time.sleep(0.3)  # Cooldown to avoid spamming
                
            if lights == 0 and distance == 1:
                message = {
                    "content": f"🚨 **Room Alert!**\nRoom is not empty and lights are {lights} and temp is {temp:.1f}°F"
                }
                response = requests.post(webhook_url, json=message)
                if response.status_code == 204:
                    print("✅ Sent alert to Discord.")
                else:
                    print(f"❌ Discord Error: {response.status_code} - {response.text}")
            if lights == 1 and distance == 0: 
                message = {
                    "content": f"🚨 **Room Alert!**\nRoom light is still on, Please turn off"
                }
                response = requests.post(webhook_url, json=message)
                if response.status_code == 204:
                    print("✅ Sent alert to Discord.")
                else:
                    print(f"❌ Discord Error: {response.status_code} - {response.text}")
            if temp > TEMP_THRESHOLD or temp < 60:
                message = {
                    "content": f"🚨 **Room Alert!**\nRoom temperature is out of range, temp is {temp:.1f}°F"
                }
                response = requests.post(webhook_url, json=message)
                if response.status_code == 204:
                    print("✅ Sent alert to Discord.")
                else:
                    print(f"❌ Discord Error: {response.status_code} - {response.text}")
        print("sleeping")
        time.sleep(0.3)

    except Exception as e:
        print("stopped")
        