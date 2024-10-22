import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load data from CSV file
data = []
glucose_levels = []

with open('glucose_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(float(row['SensorValue']))
        glucose_levels.append(float(row['GlucoseLevel']))

# Convert to numpy arrays
data = np.array(data).reshape(-1, 1)
glucose_levels = np.array(glucose_levels)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, glucose_levels, test_size=0.2, random_state=42)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict glucose levels on test data
predictions = model.predict(X_test)

# Print predictions and actual values
for i in range(len(predictions)):
    print(f"Predicted: {predictions[i]:.2f}, Actual: {y_test[i]:.2f}")

# Save the model if necessary
import joblib
joblib.dump(model, 'glucose_model.pkl')
