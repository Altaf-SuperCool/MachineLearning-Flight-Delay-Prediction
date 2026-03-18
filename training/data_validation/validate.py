def validate_schema(df, schema):
    required_cols = schema["required_columns"]

    # Check required columns
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Check types
    for col, dtype in schema["columns"].items():
        if col not in df.columns:
            continue

        if dtype == "string" and df[col].dtype != "object":
            print(f"Warning: {col} expected string but got {df[col].dtype}")

        if dtype == "integer" and not str(df[col].dtype).startswith("Int"):
            print(f"Warning: {col} expected integer but got {df[col].dtype}")

        if dtype == "float" and "float" not in str(df[col].dtype):
            print(f"Warning: {col} expected float but got {df[col].dtype}")

    print("Schema validation passed.")
