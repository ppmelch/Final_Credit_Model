# Final Credit Model
### Credit Models project

**Authors:**
- José Armando Melchor Soto — 745697
- Rolando Fortanell Canedo — 744872
- David Campos Ambriz — 7444435
 
**Course:** Credit Models

**Institution:** ITESO Universidad Jesuita de Guadalajara

**Date:** May 13, 2026
 
---
 
## Table of Contents

---
 
## Overview
 

---
 
## Architecture
 
### Project Structure
 
```mermaid
flowchart LR

    ROOT["Final_Credit_Model/"]

    ROOT --> DATA["data/"]
    ROOT --> BACKEND["backend/"]
    ROOT --> FRONTEND["frontend/"]
    ROOT --> NOTEBOOKS["notebooks/"]
    ROOT --> DOCS["docs/"]

    %% ======================
    %% BACKEND
    %% ======================

    BACKEND --> SRC["src/"]
    BACKEND --> SCRIPTS["Scripts/"]

    SRC --> SRC_DATA["data/"]
    SRC --> MODELING["modeling/"]
    SRC --> VIZMOD["visualization/"]
    SRC --> UTILS["utils/"]
    SRC --> MODELS["models/"]

    %% DATA
    SRC_DATA --> PREP["data_preparation.py"]
    SRC_DATA --> SPLIT["data_splitter.py"]

    %% MODELING
    MODELING --> BASE["base_model.py"]
    MODELING --> BUSINESS["business_logic.py"]
    MODELING --> CLASSIF["classification_model.py"]
    MODELING --> CONFIG["config.py"]
    MODELING --> EVAL["model_evaluation.py"]
    MODELING --> MODEL["model.py"]
    MODELING --> RISK["risk_calculator.py"]
    MODELING --> GEO["geospatial_risk.py"]
    MODELING --> THRESH["threshold_optimization.py"]
    MODELING --> RUNNER["experiment_runner.py"]
    MODELING --> OPTUNA["optuna_optimizer.py"]
    MODELING --> LOADER["model_loader.py"]

    %% VISUALIZATION
    VIZMOD --> VIZ["viz.py"]

    %% UTILS
    UTILS --> PRINTS["prints.py"]
    UTILS --> UTILSFILE["utils.py"]

    %% MODELS
    MODELS --> RF["random_forest.pkl"]

    %% SCRIPTS
    SCRIPTS --> EXTERNAL["External Data Source Scripts (00-13).py"]

    %% ======================
    %% FRONTEND
    %% ======================

    FRONTEND --> INDEX["index.html"]
    FRONTEND --> SVG["jalisco.svg"]

    FRONTEND --> FRONTDATA["data/"]
    FRONTEND --> JS["js/"]
    FRONTEND --> CSS["css/"]

    FRONTDATA --> RISKJSON["risk_data.json"]
    FRONTDATA --> JALISCOJSON["Jalisco.json"]
    FRONTDATA --> DASHJSON["dashboard_data.json"]

    JS --> APP["app.js"]
    CSS --> STYLE["style.css"]

    %% ======================
    %% NOTEBOOKS
    %% ======================

    NOTEBOOKS --> ANALYSIS["data_analysis.ipynb"]
    NOTEBOOKS --> FEATURE["feature_analysis.ipynb"]
    NOTEBOOKS --> DEV["Credit Model Development.ipynb"]

    %% ======================
    %% DOCS
    %% ======================

    DOCS --> PDF["Final_Credit_Model.pdf"]

    %% ======================
    %% ROOT FILES
    %% ======================

    ROOT --> MAIN["main.py"]
    ROOT --> REQ["requirements.txt"]
    ROOT --> README["README.md"]

    %% ======================
    %% STYLES
    %% ======================

    classDef root fill:#111111,color:#ffffff,stroke:#ffffff,stroke-width:2px;
    classDef folder fill:#4b4b4b,color:#ffffff,stroke:#cfcfcf;
    classDef file fill:#6b6b6b,color:#ffffff,stroke:#d9d9d9;
    classDef datafill fill:#2f6b2f,color:#ffffff,stroke:#9ad29a;
    classDef frontendfill fill:#8c6d1f,color:#ffffff,stroke:#e3c36d;
    classDef jsfill fill:#3b57b7,color:#ffffff,stroke:#9fb3ff;
    classDef cssfill fill:#7a57c7,color:#ffffff,stroke:#c5b0ff;
    classDef scriptsfill fill:#a54e4e,color:#ffffff,stroke:#ffb3b3;
    classDef modelFill fill:#d8b0b0,color:#000000,stroke:#ffffff;

    class ROOT root;

    class DATA,BACKEND,FRONTEND,NOTEBOOKS,DOCS,SRC,SCRIPTS,SRC_DATA,MODELING,VIZMOD,UTILS,MODELS,FRONTDATA,JS,CSS folder;

    class PREP,SPLIT,BASE,BUSINESS,CLASSIF,CONFIG,EVAL,MODEL,RISK,GEO,THRESH,RUNNER,OPTUNA,LOADER,VIZ,PRINTS,UTILSFILE,INDEX,SVG,APP,STYLE,ANALYSIS,FEATURE,DEV,PDF,MAIN,REQ,README,EXTERNAL file;

    class RISKJSON,JALISCOJSON,DASHJSON frontendfill;
    class APP jsfill;
    class STYLE cssfill;
    class RF modelFill;
```
 
### Functional Architecture
 
```mermaid

```
 
### OOP Architecture
 
```mermaid


```
 

 

---
 
## Methodology

 

### Model
 
 
---
 
## Results
 
### Model Performance

### Key Findings
 


---
 
## Limitations & Assumptions
 
### Future Improvements
 

---
 
## Conclusions
 

---
 
## Installation
 
```bash
# 1. Clone the repository
git clone https://github.com/ppmelch/Final_Credit_Model.git
cd Credit_Model
 
# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
 
# 3. Install dependencies
pip install -r requirements.txt
```
 
---
 
## Usage
 
```bash
python main.py
```
 
---
 
## Output
 

---
 
## Documentation
 
The full project report is available at:
 
- [Credit Model Report](docs/Final_Credit_Model.pdf)
 
---
 
## License
 
This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
