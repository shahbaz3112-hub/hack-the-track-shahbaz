import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def prepare_model_data(df):
    features = ["S1", "S2", "S3"]
    target = "Lap Time"

    # Drop rows with missing values in features or target
    df_model = df.dropna(subset=features + [target])

    # Optional: Filter out extreme lap times (e.g., > 300 seconds)
    df_model = df_model[df_model[target] < 300]

    X = df_model[features]
    y = df_model[target]

    print(f"✅ Modeling data shape: {X.shape}")
    return X, y

def train_model(X, y, model_type="linear"):
    """
    Train a regression model to predict lap time.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "linear":
        model = LinearRegression()
    elif model_type == "random_forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Unsupported model type")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred)
    }

    return model, metrics

def predict_lap_time(model, input_df):
    candidate_features = ["S1", "S2", "S3", "Sector Ratio", "Subsector StdDev"]
    features = [col for col in candidate_features if col in input_df.columns]

    input_df = input_df.dropna(subset=features)
    X = input_df[features]
    predictions = model.predict(X)
    return predictions