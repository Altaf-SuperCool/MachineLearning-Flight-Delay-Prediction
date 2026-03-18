# #️⃣ **Step 6 — Feature Engineering (PyTorch Version)**

This step prepares the dataset for PyTorch training by:

- Integer‑encoding categorical features  
- Scaling numeric features  
- Converting all features into dense PyTorch tensors  
- Saving preprocessing artifacts for inference  
- Producing `.pt` files for Step 7  

---

## ## 6.1 Run Train/Test Split

Splits the raw dataset into:

- `train.csv`  
- `test.csv`  

```powershell
python -m training.data_split.split
```

---

## ## 6.2 Run Feature Engineering (Encoding + Scaling + Tensor Conversion)

This step:

- Fits `OrdinalEncoder` on categorical columns  
- Fits `StandardScaler` on numeric columns  
- Transforms train/test datasets  
- Converts them into PyTorch tensors  
- Saves:

  ```
  X_train.pt
  X_test.pt
  y_train.pt
  y_test.pt
  encoder_mapping.pkl
  scaler.pkl
  ```

Run:

```powershell
python -m training.feature_engineering.feature_engineer
```

---

## ## 6.3 Output Files

After Step 6 completes, you will have:

### **Processed tensors**
```
data/processed/X_train.pt
data/processed/X_test.pt
data/processed/y_train.pt
data/processed/y_test.pt
```

### **Preprocessing artifacts**
```
artifacts/encoder_mapping.pkl   ← integer encoding mapping
artifacts/scaler.pkl            ← numeric scaling parameters
```

These artifacts are required for:

- Step 7 PyTorch training  
- Step 8 inference API  
- Any future retraining or CI/CD automation  

---

## ## 6.4 Summary

Step 6 transforms raw airline data into **model‑ready PyTorch tensors** and saves the preprocessing logic needed for consistent inference.

This ensures:

- Training and inference use identical transformations  
- Categorical features become integer IDs  
- Numeric features are standardized  
- The model receives a clean, dense feature matrix  

---
