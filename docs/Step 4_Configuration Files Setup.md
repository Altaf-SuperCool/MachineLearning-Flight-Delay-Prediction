
# #️⃣ **Step 4 — Configuration Files Setup (Commands Only)**

These commands create and populate:

- `config.yaml`
- `params.yaml`
- `schema.json`

### ## 4.1 Create configuration folder structure

```powershell
New-Item -ItemType Directory -Path "training\config" -ErrorAction SilentlyContinue
```

---

### ## 4.2 Create config.yaml

```powershell
New-Item -ItemType File -Path "training\config\config.yaml"
```

(You then pasted the YAML content manually.)

---

### ## 4.3 Create params.yaml

```powershell
New-Item -ItemType File -Path "training\config\params.yaml"
```

(You then pasted the YAML content manually.)

---

### ## 4.4 Create schema.json

```powershell
New-Item -ItemType File -Path "training\config\schema.json"
```

(You then pasted the JSON schema manually.)

---

### ## 4.5 Validate folder structure

```powershell
Get-ChildItem -Recurse training\config
```

