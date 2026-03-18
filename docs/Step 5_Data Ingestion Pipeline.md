
# #️⃣ **Step 5 — Data Ingestion Pipeline (Commands Only)**

These commands cover:

- Folder creation  
- CSV placement  
- Optional S3 upload  
- Running ingestion  
- Verifying processed output  

---

## ## 5.1 Create required data folders

```powershell
New-Item -ItemType Directory -Path "data" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "data\raw" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "data\processed" -ErrorAction SilentlyContinue
```

---

## ## 5.2 Place CSV file into raw folder

(Manual step)
Download from Kaggle → extract → rename to:
https://www.kaggle.com/datasets/usdot/flight-delays/flights.csv

Place your file here:

```
data/raw/airline_delays.csv
```

---

## ## 5.3 (Optional) Upload CSV to S3

```powershell
aws s3 cp data/raw/airline_delays.csv s3://airline-delay-raw-data/airline_delays.csv
```

---

## ## 5.4 Verify CSV exists locally

```powershell
Get-ChildItem -Recurse data/raw
```

---

## ## 5.5 Run ingestion using Python module mode

This is the correct way to run package‑based scripts:

```powershell
python -m training.data_ingestion.ingest
```

---

## ## 5.6 Verify processed output

```powershell
Get-ChildItem data/processed
```

Expected output:

```
processed_data.csv
```
