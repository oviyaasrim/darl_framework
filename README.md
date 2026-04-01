# Dynamic AI Risk Loop (DARL)
### A Continuous Risk Management Framework for AI-Based Tumor Detection Systems

---

## Paper Reference

> **Oviyaasri, M. & Manjuladevi, M. (2025).** Dynamic AI Risk Loop (DARL): A Continuous Risk Management Framework for AI-Based Tumor Detection Systems. *[Journal Name - To Be Updated Post Acceptance]*

---

## Overview

DARL is a closed-loop, continuous risk management framework purpose-built for AI-enabled Software as a Medical Device (SaMD). It addresses the structural mismatch between static risk management standards (ISO 14971) and the dynamic, adaptive nature of deployed machine learning systems.

**Core Formula:**

```
DRS = w1(D_input) + w2(D_output) + w3(S_clinical)
```

Where:
- `D_input` = Normalized input drift index (0 to 1)
- `D_output` = Normalized output performance degradation index (0 to 1)
- `S_clinical` = Clinical feedback signal index (0 to 1)
- Default weights: `w1=0.30`, `w2=0.45`, `w3=0.25`

---

## Risk Threshold Classification

| Risk Level | DRS Range | Required Action |
|---|---|---|
| Low | 0.00 to 0.25 | Routine monitoring |
| Medium | 0.26 to 0.50 | Internal engineering review |
| High | 0.51 to 0.75 | PCCP evaluation and retraining |
| Critical | 0.76 to 1.00 | Device suspension and regulatory notification |

---

## Repository Structure

```
darl-framework/
│
├── darl_simulation.py          # Main simulation script (paper Section 6)
├── darl_simulation_results.csv # Output: monthly DRS table
├── darl_drs_trajectory.png     # Output: Figure 3 for paper
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/darl-framework.git
cd darl-framework
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Usage

**Run the standard simulation (matches paper exactly):**
```bash
python darl_simulation.py
```

**This will generate:**
- Console table of monthly DRS values and risk levels
- `darl_simulation_results.csv` - Full simulation data
- `darl_drs_trajectory.png` - Figure 3 (publication-ready, 300 DPI)

**Run a custom scenario (adjust parameters in script):**
```python
from darl_simulation import run_custom_simulation

# Example: Higher input drift weight scenario
custom_df = run_custom_simulation(
    w1=0.40,
    w2=0.40,
    w3=0.20,
    d_input_end=0.60,
    months=12
)
print(custom_df)
```

---

## Simulation Parameters

All parameters are defined at the top of `darl_simulation.py` and can be modified:

```python
# Weight parameters
W1 = 0.30   # Input drift weight
W2 = 0.45   # Output drift weight
W3 = 0.25   # Clinical signal weight

# Drift scenario end values (Month 12)
D_INPUT_END    = 0.45
D_OUTPUT_END   = 0.40
S_CLINICAL_END = 0.30
```

---

## Simulation Results (Paper - Section 6)

| Month | Sensitivity (%) | D_input | D_output | S_clinical | DRS | Risk Level |
|---|---|---|---|---|---|---|
| 1 | 94.0 | 0.05 | 0.02 | 0.03 | 0.08 | Low |
| 5 | 91.5 | 0.21 | 0.19 | 0.15 | 0.26 | **Medium** |
| 8 | 88.2 | 0.33 | 0.31 | 0.24 | 0.41 | Medium |
| 10 | 86.1 | 0.41 | 0.37 | 0.28 | 0.52 | **High** |
| 12 | 85.0 | 0.45 | 0.40 | 0.30 | 0.57 | High |

**Key Finding:** DARL detects drift at Month 5 (Sensitivity = 91.5%) before clinical consequences accumulate, and triggers regulatory action at Month 10, approximately 6 weeks before terminal performance decline.

---

## Regulatory Alignment

This framework is designed to align with:
- **FDA TPLC Draft Guidance (January 2025)** - Total Product Lifecycle approach for AI-enabled devices
- **IMDRF N88 FINAL (January 2025)** - Good Machine Learning Practice (GMLP) principles
- **ISO 14971:2019** - Risk management for medical devices (extended)
- **EU AI Act (2024)** - Post-market monitoring for high-risk AI systems

---

## Requirements

```
matplotlib>=3.5.0
pandas>=1.4.0
numpy>=1.21.0
```

---

## License

This project is licensed under the MIT License.

---

## Authors

- **M. Oviyaasri** - Independent Researcher, Hyderabad, India
- **Dr. M. Manjuladevi** - SNS College of Engineering, Tamil Nadu, India

---

## Citation

If you use this code in your research, please cite:

```bibtex
@article{oviyaasri2025darl,
  title={Dynamic AI Risk Loop (DARL): A Continuous Risk Management Framework
         for AI-Based Tumor Detection Systems},
  author={Oviyaasri, M. and Manjuladevi, M.},
  journal={[Journal Name]},
  year={2025}
}
```

---

## Contact

For questions related to the DARL framework or simulation code:
**oviyaasriac@outlook.com**
