import serial
import csv
import os

# Replace 'COM3' with your port (e.g., '/dev/ttyUSB0' on Linux or '/dev/tty.SLAB_USBtoUART' on macOS)
ser = serial.Serial('COM8', 115200, timeout=1)


file_path = r"C:\Users\ladmin\Solar\PVSoilingTest.csv"  # Replace with the actual path to your file

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' deleted successfully.")
else:
    print(f"File '{file_path}' does not exist.")

with open(r"C:\Users\ladmin\Solar\PVSoilingTest.csv", 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Read and write header (assumes the first line is a header)
    csv_writer.writerow(["TimeStamp","BusVoltage 1 (V)", "Current 1 (mA)", "Power 1 (mW)", "Resistance 1 (Ohm)","BusVoltage 2 (V)", "Current 2 (mA)", "Power 2 (mW)", "Resistance 2 (Ohm)"])

    print("Recording data. Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Assume CSV formatting on the device
                data = line.split(',')
                csv_writer.writerow(data)
                print(data)  # Optionally print to console
    except KeyboardInterrupt:
        print("Data logging stopped.")
