import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# File paths
file1_path = 'test.txt'  # Format: "M/D/YYYY HH:MM<TAB>Voltage"
file2_path = 'AudioMothR_3-11_12-43.txt'  # Format: "hours since 3/11 12:43, Voltage"

# Define the starting time for the second file
start_time_file2 = datetime.strptime('3/11/2025 12:43', '%m/%d/%Y %H:%M')

# Function to read first file (absolute timestamps)
def read_file1(file_path):
    x_values, y_values = [], []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    time_str, voltage = line.split("\t")  # Split by tab
                    actual_time = datetime.strptime(time_str.strip(), "%m/%d/%Y %H:%M")
                    x_values.append(actual_time)
                    y_values.append(float(voltage.strip()))
                except ValueError:
                    print(f"Skipping invalid line in {file_path}: {line}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return x_values, y_values

# Function to read second file (relative timestamps)
def read_file2(file_path, start_time):
    x_values, y_values = [], []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    hours_since_start, voltage = line.split(",")
                    hours_since_start = float(hours_since_start.strip())  # Convert to float for hours
                    actual_time = start_time + timedelta(hours=hours_since_start)
                    x_values.append(actual_time)
                    y_values.append(float(voltage.strip()))
                except ValueError:
                    print(f"Skipping invalid line in {file_path}: {line}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return x_values, y_values

# Read both datasets
x1, y1 = read_file1(file1_path)
x2, y2 = read_file2(file2_path, start_time_file2)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(x1, y1, marker="o", linestyle="-", label="Battery Voltage (Manual, 2 weeks)", color="blue")
plt.plot(x2, y2, marker="s", linestyle="--", label="Battery Voltage (Automated, 3 days)", color="green")

# Formatting
plt.title("Audiomoth R Battery Voltage Over Time")
plt.xlabel("Date and Time")
plt.ylabel("Voltage (V)")
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

plt.axvline(x=datetime.strptime("3/13/2025 00:30", "%m/%d/%Y %H:%M"), color="red", linestyle="--", label="Stopped recording wav files with data here (3/13/2025 00:30)")
plt.axvline(x=datetime.strptime("3/05/2025 19:42", "%m/%d/%Y %H:%M"), color="orange", linestyle="--", label="SD card switched out (3/05/2025 19:42)")

plt.legend()
plt.tight_layout()
plt.show()
