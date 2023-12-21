import asyncio
import websockets
import json
import pandas as pd
import subprocess
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import threading

# Function to get the path to the CSV file from the user
async def get_csv_path():
    while True:
        csv_path = input("Enter the path to the CSV file: ")
        try:
            # Attempt to read the CSV file into a dictionary of records
            data = pd.read_csv(csv_path).to_dict('records')
            return data
        except FileNotFoundError:
            print("File not found. Please enter a valid CSV file path.")

# Function to get the user's choice for displaying lines (all or specific amount)
async def get_display_option():
    while True:
        option = input("Do you want to display all lines (A) or a specific amount (S)? ").lower()
        if option in ['a', 'all']:
            return 'all'
        elif option in ['s', 'specific']:
            return 'specific'
        else:
            print("Invalid option. Please enter 'A' for 'all' or 'S' for 'specific.")

# Function to get the number of lines to display based on the user's choice
async def get_display_lines(data, option):
    if option == 'all':
        return len(data)
    elif option == 'specific':
        while True:
            try:
                # Attempt to get a valid integer for the number of lines to display
                lines = int(input("Enter the number of lines to display on the server: "))
                return lines
            except ValueError:
                print("Please enter a valid integer.")

# Function to run 'test.py' subprocess
def run_test_py():
    subprocess.run(["python", "test.py"])

# Function to send data to the server via WebSocket
async def send_data(display_speed):
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connection successful!")

            # Get the CSV data from the user
            data = await get_csv_path()

            while True:
                # Get the user's choice for displaying lines
                display_option = await get_display_option()

                # Check if the user wants to run test.py
                if display_option in ['all', 'specific']:
                    # Run test.py using a separate thread
                    threading.Thread(target=run_test_py).start()

                # Get the number of lines to display based on the user's choice
                display_lines = await get_display_lines(data, display_option)

                # Send each record to the server
                for d in data[:display_lines]:
                    message = json.dumps(d)
                    await websocket.send(message)
                    await asyncio.sleep(display_speed)

                repeat_option = input("Do you want to send more data? (y/n): ").lower()
                if repeat_option != 'y':
                    break

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed. Exiting...")

# Main entry point of the script
if __name__ == "__main__":
    display_speed = 0.5 # Set the display speed in seconds (adjust as needed)
    asyncio.run(send_data(display_speed))
