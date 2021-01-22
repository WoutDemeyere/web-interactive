import os
import json
from azure.iot.device import IoTHubDeviceClient
import rtmidi
import time


conn_str = "" #Get conenction string from azure
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("PYTHON MIDI")

def message_received_handler(message):
    data = json.loads(message.data)

    print(f"--- Trigering chanel {data['chan']}")

    midiout.send_message([0x90, data['chan'], 112]) 
    time.sleep(0.4)
    midiout.send_message([0x90, data['chan'], 0])

def run():
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            device_client.disconnect()
            break

if __name__ == "__main__":
    device_client.connect()
    print("Connected")
    device_client.on_message_received = message_received_handler
    run()

