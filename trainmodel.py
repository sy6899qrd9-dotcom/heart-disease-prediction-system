import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("heart_10000_encoded.csv")

# Features and target
X = df.drop("target", axis=1)
y = df["target"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model saved successfully!")