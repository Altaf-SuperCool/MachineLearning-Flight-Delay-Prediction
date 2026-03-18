
# ⭐ What `artifacts/model.pt` Actually Contains

`model.pt` **does NOT contain the entire model**.

It contains only the **learned weights** of your neural network — the parameters that were updated during training.

Think of it as the **memory** your model built from millions of examples.

### ✔ It contains:
- Layer weights  
- Layer biases  
- BatchNorm running means & variances  
- Dropout masks (not active during inference)  
- All tensors that define the trained model  

### ✔ It does NOT contain:
- The model architecture code  
- The training data  
- The optimizer  
- The preprocessing logic  
- The training script  

This is why, during inference, you must **recreate the model architecture** and then load the weights.

---

# ⭐ How to Inspect What’s Inside `model.pt`

You can inspect it directly in Python:

```python
import torch

state = torch.load("artifacts/model.pt")
print(state.keys())
```

You will see something like:

```
dict_keys([
  'net.0.weight',
  'net.0.bias',
  'net.1.weight',
  'net.1.bias',
  'net.1.running_mean',
  'net.1.running_var',
  'net.4.weight',
  'net.4.bias',
  ...
])
```

Each entry corresponds to a layer in your MLP:

- `net.0` → first Linear layer  
- `net.1` → BatchNorm  
- `net.4` → second Linear layer  
- etc.

If you print one:

```python
print(state['net.0.weight'])
```

You’ll see a tensor like:

```
tensor([[ 0.0123, -0.0456, ... ],
        [ 0.0789,  0.0034, ... ],
        ...
])
```

These numbers are the **learned parameters**.

---

# ⭐ Why These Weights Matter

During training, your model:

- Makes predictions  
- Computes loss  
- Adjusts weights via backpropagation  

After millions of updates, the weights encode patterns like:

- Which carriers delay more  
- Which airports cause delays  
- Which times of day are risky  
- How distance affects delay probability  

All of this knowledge is stored in `model.pt`.

---

# ⭐ How `model.pt` Makes Predictions on New Data

When new data arrives:

### 1️⃣ Preprocessing happens  
Using:

- `encoder_mapping.pkl` → convert strings → integer IDs  
- `scaler.pkl` → scale numeric values  

### 2️⃣ You recreate the model architecture

```python
model = MLPModel(input_dim=6)
```

### 3️⃣ You load the learned weights

```python
model.load_state_dict(torch.load("artifacts/model.pt"))
model.eval()
```

### 4️⃣ You pass the new data through the model

```python
prob = model(input_tensor)
```

The model outputs something like:

```
0.82
```

Meaning:

> 82% chance this flight will be delayed.

---

# ⭐ How Old Training Data Helps Predict New Data

This is the heart of machine learning.

During training:

- The model sees millions of examples  
- It adjusts weights to reduce prediction error  
- These weights encode general patterns  

So when new data arrives:

- The model compares it to patterns it learned  
- It produces a probability based on similarity to past examples  

This is called **generalization**.

The model does **not** memorize old predictions.  
It learns **patterns** from old data and applies them to new data.

---

# ⭐ In One Sentence

`model.pt` is the **learned intelligence** of your system — a compact file containing all the weights your neural network learned, enabling it to make predictions on new, unseen data.

---
