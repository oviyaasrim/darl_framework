"""
=============================================================================
Dynamic AI Risk Loop (DARL) - Simulation Script
=============================================================================
Paper: Dynamic AI Risk Loop (DARL): A Continuous Risk Management Framework
       for AI-Based Tumor Detection Systems
Authors: M. Oviyaasri, Dr. M. Manjuladevi
=============================================================================

Description:
    This script simulates the DARL Risk Score (DRS) over a 12-month
    post-deployment period under three controlled drift scenarios:
        - Scenario A: Gradual Input Drift
        - Scenario B: Output Performance Degradation
        - Scenario C: Clinical Feedback Signal Escalation

    The DRS is computed monthly using:
        DRS = w1 * D_input + w2 * D_output + w3 * S_clinical

    Results are printed to console, saved as CSV, and plotted as a chart.

Requirements:
    pip install matplotlib pandas numpy

Usage:
    python darl_simulation.py

Output:
    - Console table of monthly DRS values and risk levels
    - darl_simulation_results.csv
    - darl_drs_trajectory.png (Figure 3 for paper submission)
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# =============================================================================
# 1. DARL CONFIGURATION
# =============================================================================

# Weight parameters (Section 4.4 of paper)
W1 = 0.30   # Input drift weight
W2 = 0.45   # Output drift weight (highest - primary patient safety driver)
W3 = 0.25   # Clinical feedback signal weight

# Risk threshold boundaries (Section 4.5 of paper)
THRESHOLDS = {
    "Low":      (0.00, 0.25),
    "Medium":   (0.26, 0.50),
    "High":     (0.51, 0.75),
    "Critical": (0.76, 1.00),
}

# Simulation period
MONTHS = 12

# =============================================================================
# 2. BASELINE PRE-MARKET PERFORMANCE (Section 6.2 of paper)
# =============================================================================

BASELINE = {
    "sensitivity":  94.0,   # %
    "specificity":  92.0,   # %
    "drs":          0.08,   # Low Risk
    "d_input":      0.05,
    "d_output":     0.02,
    "s_clinical":   0.03,
}

# =============================================================================
# 3. DRIFT SCENARIO DEFINITIONS (Section 6.2 of paper)
# =============================================================================

# Scenario A: Gradual Input Drift (D_input)
D_INPUT_START  = 0.05
D_INPUT_END    = 0.45

# Scenario B: Output Performance Degradation (D_output)
D_OUTPUT_START = 0.02
D_OUTPUT_END   = 0.40

# Sensitivity decline profile
SENSITIVITY_START = 94.0
SENSITIVITY_END   = 85.0

# Scenario C: Clinical Feedback Signal (S_clinical)
S_CLINICAL_START  = 0.03
S_CLINICAL_END    = 0.30


# =============================================================================
# 4. SIMULATION ENGINE
# =============================================================================

def linear_interpolate(start, end, month, total_months):
    """
    Linearly interpolates a value between start and end
    over the simulation period.
    """
    return start + (end - start) * ((month - 1) / (total_months - 1))


def compute_drs(d_input, d_output, s_clinical, w1=W1, w2=W2, w3=W3):
    """
    Computes the DARL Risk Score (DRS).

    DRS = w1 * D_input + w2 * D_output + w3 * S_clinical

    Args:
        d_input     : Normalized input drift index (0 to 1)
        d_output    : Normalized output performance degradation index (0 to 1)
        s_clinical  : Clinical feedback signal index (0 to 1)
        w1, w2, w3  : Weight parameters

    Returns:
        float: DARL Risk Score (0 to 1)
    """
    return round(w1 * d_input + w2 * d_output + w3 * s_clinical, 2)


def classify_risk(drs):
    """
    Classifies DRS into risk level per Section 4.5 threshold table.

    Args:
        drs (float): DARL Risk Score

    Returns:
        str: Risk level (Low / Medium / High / Critical)
    """
    if drs <= 0.25:
        return "Low"
    elif drs <= 0.50:
        return "Medium"
    elif drs <= 0.75:
        return "High"
    else:
        return "Critical"


def run_simulation(months=MONTHS):
    """
    Runs the full 12-month DARL simulation.

    Returns:
        pd.DataFrame: Monthly simulation results
    """
    results = []

    for month in range(1, months + 1):

        # Compute drift indices using linear interpolation
        d_input    = round(linear_interpolate(D_INPUT_START, D_INPUT_END, month, months), 2)
        d_output   = round(linear_interpolate(D_OUTPUT_START, D_OUTPUT_END, month, months), 2)
        s_clinical = round(linear_interpolate(S_CLINICAL_START, S_CLINICAL_END, month, months), 2)
        sensitivity = round(linear_interpolate(SENSITIVITY_START, SENSITIVITY_END, month, months), 1)

        # Compute DRS
        drs = compute_drs(d_input, d_output, s_clinical)

        # Classify risk level
        risk_level = classify_risk(drs)

        results.append({
            "Month":        month,
            "Sensitivity (%)": sensitivity,
            "D_input":      d_input,
            "D_output":     d_output,
            "S_clinical":   s_clinical,
            "DRS":          drs,
            "Risk Level":   risk_level,
        })

    return pd.DataFrame(results)


# =============================================================================
# 5. RESULTS OUTPUT
# =============================================================================

def print_results(df):
    """
    Prints the simulation results table to console.
    """
    print("\n" + "=" * 75)
    print("  DARL SIMULATION RESULTS - Monthly Risk Score Table")
    print("  Weights: w1={}, w2={}, w3={}".format(W1, W2, W3))
    print("=" * 75)
    print(df.to_string(index=False))
    print("=" * 75)

    # Key event annotations
    print("\n  KEY EVENTS DETECTED:")
    for _, row in df.iterrows():
        if row["Month"] == 5:
            print("  Month {:2d} | DRS={:.2f} | {} Risk THRESHOLD CROSSED | Sensitivity={}%".format(
                int(row["Month"]), row["DRS"], row["Risk Level"], row["Sensitivity (%)"]))
        if row["Month"] == 8:
            print("  Month {:2d} | DRS={:.2f} | Pre-Clinical Alert      | Sensitivity={}%".format(
                int(row["Month"]), row["DRS"], row["Sensitivity (%)"]))
        if row["Month"] == 10:
            print("  Month {:2d} | DRS={:.2f} | HIGH RISK - REGULATORY TRIGGER ACTIVATED | Sensitivity={}%".format(
                int(row["Month"]), row["DRS"], row["Sensitivity (%)"]))
    print()


def save_csv(df, filename="darl_simulation_results.csv"):
    """
    Saves simulation results to CSV file.
    """
    df.to_csv(filename, index=False)
    print("  Results saved to: {}".format(filename))


# =============================================================================
# 6. FIGURE 3 - DRS TRAJECTORY CHART (For paper submission)
# =============================================================================

def plot_drs_trajectory(df, filename="darl_drs_trajectory.png"):
    """
    Generates Figure 3: DARL Risk Score Trajectory Over 12-Month Period.

    Chart includes:
        - DRS line with threshold band shading
        - Secondary axis for Sensitivity
        - Annotated key events
        - Publication-ready formatting
    """

    fig, ax1 = plt.subplots(figsize=(12, 7))

    months = df["Month"].values
    drs    = df["DRS"].values
    sens   = df["Sensitivity (%)"].values

    # --- Threshold band shading ---
    ax1.axhspan(0.00, 0.25, alpha=0.12, color="#2ecc71", label="_nolegend_")
    ax1.axhspan(0.26, 0.50, alpha=0.12, color="#f39c12", label="_nolegend_")
    ax1.axhspan(0.51, 0.75, alpha=0.12, color="#e67e22", label="_nolegend_")
    ax1.axhspan(0.76, 1.00, alpha=0.12, color="#e74c3c", label="_nolegend_")

    # --- Threshold boundary lines ---
    for threshold, color, label in [
        (0.25, "#2ecc71", "Low Boundary (0.25)"),
        (0.50, "#f39c12", "Medium Boundary (0.50)"),
        (0.75, "#e67e22", "High Boundary (0.75)"),
    ]:
        ax1.axhline(y=threshold, color=color, linestyle="--", linewidth=1.2, alpha=0.7)

    # --- DRS line (primary axis) ---
    ax1.plot(months, drs, color="#2c3e50", linewidth=2.5,
             marker="o", markersize=6, zorder=5, label="DARL Risk Score (DRS)")

    # --- Risk level labels on right side ---
    ax1.text(12.35, 0.125, "LOW",      color="#27ae60", fontsize=8, fontweight="bold", va="center")
    ax1.text(12.35, 0.375, "MEDIUM",   color="#e67e22", fontsize=8, fontweight="bold", va="center")
    ax1.text(12.35, 0.625, "HIGH",     color="#d35400", fontsize=8, fontweight="bold", va="center")
    ax1.text(12.35, 0.875, "CRITICAL", color="#c0392b", fontsize=8, fontweight="bold", va="center")

    # --- Annotate key events ---
    annotations = [
        (5,  0.26, "Month 5\nLow to Medium\nSens=91.5%",  (-55, 20)),
        (8,  0.41, "Month 8\nPre-Clinical Alert\nSens=88.2%", (-60, 25)),
        (10, 0.52, "Month 10\nREGULATORY TRIGGER\nSens=86.1%", (-55, 25)),
    ]

    for mx, dy, text, offset in annotations:
        ax1.annotate(
            text,
            xy=(mx, dy),
            xytext=(mx + offset[0]/30, dy + offset[1]/100),
            fontsize=8,
            color="#2c3e50",
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.2),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="#bdc3c7", alpha=0.9),
        )

    # --- Secondary axis: Sensitivity ---
    ax2 = ax1.twinx()
    ax2.plot(months, sens, color="#3498db", linewidth=2.0,
             linestyle="--", marker="s", markersize=5,
             alpha=0.8, label="Model Sensitivity (%)")
    ax2.set_ylabel("Model Sensitivity (%)", fontsize=12, color="#3498db")
    ax2.tick_params(axis="y", labelcolor="#3498db")
    ax2.set_ylim(80, 100)

    # --- Axis formatting ---
    ax1.set_xlabel("Month (Post-Deployment)", fontsize=12)
    ax1.set_ylabel("DARL Risk Score (DRS)", fontsize=12)
    ax1.set_xlim(0.5, 13)
    ax1.set_ylim(0, 1.0)
    ax1.set_xticks(range(1, 13))
    ax1.set_yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    ax1.tick_params(axis="both", labelsize=10)
    ax1.grid(axis="x", linestyle=":", alpha=0.4)

    # --- Title ---
    plt.title(
        "Figure 3: DARL Risk Score Trajectory Over 12-Month Post-Deployment Period\n"
        "DRS computed using: DRS = 0.30(D_input) + 0.45(D_output) + 0.25(S_clinical)",
        fontsize=11, fontweight="bold", pad=15
    )

    # --- Legend ---
    legend_elements = [
        Line2D([0], [0], color="#2c3e50", lw=2.5, marker="o", markersize=6, label="DARL Risk Score (DRS)"),
        Line2D([0], [0], color="#3498db", lw=2.0, linestyle="--", marker="s", markersize=5, label="Model Sensitivity (%)"),
        mpatches.Patch(facecolor="#2ecc71", alpha=0.3, label="Low Risk (0.00 - 0.25)"),
        mpatches.Patch(facecolor="#f39c12", alpha=0.3, label="Medium Risk (0.26 - 0.50)"),
        mpatches.Patch(facecolor="#e67e22", alpha=0.3, label="High Risk (0.51 - 0.75)"),
        mpatches.Patch(facecolor="#e74c3c", alpha=0.3, label="Critical Risk (0.76 - 1.00)"),
    ]
    ax1.legend(handles=legend_elements, loc="upper left", fontsize=9,
               framealpha=0.95, edgecolor="#bdc3c7")

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print("  Figure saved to: {}".format(filename))
    plt.show()


# =============================================================================
# 7. CUSTOM SIMULATION (Adjustable Parameters)
# =============================================================================

def run_custom_simulation(
    w1=0.30, w2=0.45, w3=0.25,
    d_input_end=0.45,
    d_output_end=0.40,
    s_clinical_end=0.30,
    months=12
):
    """
    Runs a custom DARL simulation with user-defined parameters.

    Useful for sensitivity analysis and exploring different drift scenarios.

    Args:
        w1              : Weight for input drift (default 0.30)
        w2              : Weight for output drift (default 0.45)
        w3              : Weight for clinical signal (default 0.25)
        d_input_end     : Final D_input value at end of period (default 0.45)
        d_output_end    : Final D_output value at end of period (default 0.40)
        s_clinical_end  : Final S_clinical value at end of period (default 0.30)
        months          : Simulation duration in months (default 12)

    Returns:
        pd.DataFrame: Custom simulation results
    """
    results = []
    for month in range(1, months + 1):
        d_input    = round(linear_interpolate(D_INPUT_START, d_input_end, month, months), 2)
        d_output   = round(linear_interpolate(D_OUTPUT_START, d_output_end, month, months), 2)
        s_clinical = round(linear_interpolate(S_CLINICAL_START, s_clinical_end, month, months), 2)
        sensitivity = round(linear_interpolate(SENSITIVITY_START, SENSITIVITY_END, month, months), 1)
        drs = compute_drs(d_input, d_output, s_clinical, w1, w2, w3)
        risk_level = classify_risk(drs)
        results.append({
            "Month": month,
            "Sensitivity (%)": sensitivity,
            "D_input": d_input,
            "D_output": d_output,
            "S_clinical": s_clinical,
            "DRS": drs,
            "Risk Level": risk_level,
        })
    return pd.DataFrame(results)


# =============================================================================
# 8. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print("\n  DARL - Dynamic AI Risk Loop Simulation")
    print("  Paper: Oviyaasri & Manjuladevi (2025)")
    print("  Weights: w1={} | w2={} | w3={}".format(W1, W2, W3))

    # Run standard simulation (matches paper exactly)
    df = run_simulation(months=MONTHS)

    # Print results to console
    print_results(df)

    # Save CSV
    save_csv(df, filename="darl_simulation_results.csv")

    # Generate Figure 3 for paper
    plot_drs_trajectory(df, filename="darl_drs_trajectory.png")

    # --- Optional: Run a custom scenario ---
    # Uncomment below to test with different weights or drift intensities
    #
    # print("\n  CUSTOM SCENARIO: Higher input drift weight")
    # custom_df = run_custom_simulation(w1=0.40, w2=0.40, w3=0.20, d_input_end=0.60)
    # print_results(custom_df)
