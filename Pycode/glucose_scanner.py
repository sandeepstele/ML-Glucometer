import machine
import utime
import uos

# Define IR sensor pin and glucose level range
ir_pin = machine.ADC(26)  # Pin A0
glucose_min = 0
glucose_max = 65535  # 16-bit ADC value in Raspberry Pi Pico
glucose_min_val = 70.0
glucose_max_val = 400.0

# Initialize file for storing data
filename = 'glucose_data.csv'

def initialize_csv():
    with open(filename, 'w') as f:
        f.write('SensorValue,GlucoseLevel\n')

def save_to_csv(sensor_value, glucose_level):
    with open(filename, 'a') as f:
        f.write(f'{sensor_value},{glucose_level}\n')

def calculate_glucose(sensor_value):
    # Use quadratic equation to calculate glucose level
    glucose_level = (0.000009) * (sensor_value ** 2) + (0.1788) * sensor_value + 75.454
    # Add random noise to glucose level
    noise = machine.rng() % 11 - 5  # random noise between -5 and +5
    glucose_level += noise
    return glucose_level

# Initialize CSV file
initialize_csv()

while True:
    # Read sensor value from ADC
    sensor_value = ir_pin.read_u16()

    # Check if finger is in contact with sensor
    if glucose_min < sensor_value < glucose_max:
        # Map the sensor value and calculate glucose level
        glucose_level = calculate_glucose(sensor_value)
        
        # Save the reading to the CSV file
        save_to_csv(sensor_value, glucose_level)
        
        # Print glucose level to serial monitor
        print(f"Glucose level: {glucose_level} mg/dL")
    else:
        print("Please place finger on the sensor")
    
    # Delay before taking next reading
    utime.sleep(5)  # 5 seconds delay
