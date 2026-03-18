# ✅ **How to Know Step 7 Is Completed**

Step 7 is considered **fully complete** when all of the following have happened:

### **1. Training loop finished all epochs**
You saw logs like:

```
Epoch 1/5 - Train Loss: ...
Epoch 2/5 - Train Loss: ...
...
Epoch 5/5 - Train Loss: ...
```

### **2. Evaluation ran successfully**
You saw:

- Classification report  
- Precision/recall  
- F1 score  
- ROC‑AUC  

Example:

```
Classification report:
              precision    recall  f1-score   support
...
ROC-AUC: 0.78
```

### **3. The model was saved**
You saw:

```
Saving model to artifacts/model.pt...
Model saved successfully.
```

And the file exists:

```
artifacts/model.pt
```

If all three happened → **Step 7 is 100% complete**.

---

# 🧠 **What “completed” means in the pipeline**

Step 7 is the **learning phase**.

By completing Step 7, you now have:

### ✔ A trained neural network  
Stored in:

```
artifacts/model.pt
```

### ✔ A model that can make predictions on new data  
Because it has learned patterns from historical flights.

### ✔ A model that is ready for deployment  
This is the artifact Step 8 will load.

### ✔ A reproducible training run  
Because Step 6 + Step 7 together define the full training pipeline.

---

# 🧩 **How Step 7 fits into the whole MLOps pipeline**

Here’s the big picture:

```
Step 6 → Preprocessing
    |
    | produces:
    |   X_train.pt
    |   X_test.pt
    |   y_train.pt
    |   y_test.pt
    |   encoder_mapping.pkl
    |   scaler.pkl
    |
Step 7 → Model Training
    |
    | produces:
    |   model.pt
    |
Step 8 → Inference API
    |
    | loads:
    |   model.pt
    |   encoder_mapping.pkl
    |   scaler.pkl
    |
Step 9 → CI/CD Deployment
Step 10 → Monitoring & Retraining
```

So Step 7 is the **bridge** between:

- Data preparation  
- Model deployment  

---

```
python -m training.model_training.train
```
Using device: cpu
Input dimension: 6
Epoch 1/5 - Train Loss: 0.6473
Epoch 2/5 - Train Loss: 0.6420
Epoch 3/5 - Train Loss: 0.6413
Epoch 4/5 - Train Loss: 0.6409
Epoch 5/5 - Train Loss: 0.6408
Evaluating on test set...
Classification report:
              precision    recall  f1-score   support

         0.0       0.65      0.98      0.78    746293
         1.0       0.52      0.04      0.08    417523

    accuracy                           0.64   1163816
   macro avg       0.58      0.51      0.43   1163816
weighted avg       0.60      0.64      0.53   1163816

ROC-AUC: 0.5940
Saving model to artifacts\model.pt...
Model saved successfully.