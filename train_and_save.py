import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("data/final_dataset.csv")
print("Dataset shape:", df.shape)

# Defensive checks
assert "student_id" in df.columns
assert "at_risk" in df.columns
assert len(df) > 100

# Split features/target
X = df.drop(columns=["student_id", "at_risk"])
y = df["at_risk"]

categorical_cols = X.select_dtypes(include="object").columns.tolist()
numerical_cols = X.select_dtypes(exclude="object").columns.tolist()

print("Categorical columns:", categorical_cols)
print("Numerical columns:", numerical_cols)

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numerical_cols),
    ]
)

model = LogisticRegression(
    max_iter=2000,
    solver="liblinear",
    class_weight="balanced"
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", model),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline.fit(X_train, y_train)

os.makedirs("artifacts", exist_ok=True)
joblib.dump(pipeline, "artifacts/student_risk_model.joblib")

print("✅ Model trained and saved successfully")