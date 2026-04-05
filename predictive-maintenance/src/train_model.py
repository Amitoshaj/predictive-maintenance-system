import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('../data/sensor_data.csv')

X = df[['temperature', 'pressure', 'vibration']]
y = df['failure']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

import os

os.makedirs('../model', exist_ok=True)
joblib.dump(model, '../model/model.pkl')

print("Model trained and saved successfully!")
from sklearn.metrics import accuracy_score, confusion_matrix

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

import matplotlib.pyplot as plt

features = ['temperature', 'pressure', 'vibration']
importance = model.feature_importances_

plt.bar(features, importance)
plt.title("Feature Importance")
plt.xlabel("Sensors")
plt.ylabel("Importance")

# Save graph
plt.savefig('../model/feature_importance.png')

print("Feature importance saved!")
