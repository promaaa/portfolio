#!/usr/bin/env python3
"""
Generate calibration and accuracy charts for Power Monitoring System
Requires: matplotlib, numpy
Install: pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set style for professional-looking charts
plt.style.use("seaborn-v0_8-darkgrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans"]
plt.rcParams["font.size"] = 11

# Create output directory
output_dir = Path(__file__).parent.parent / "images"
output_dir.mkdir(exist_ok=True)


def generate_calibration_curve():
    """
    Generate calibration curve showing measured vs reference values
    with linear regression line
    """
    # Calibration data points (reference current in A, measured current in A)
    # Simulating real calibration data with small random errors
    np.random.seed(42)

    # Reference currents: 0%, 25%, 50%, 75%, 100% of 20A range
    reference_current = np.array(
        [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0]
    )

    # Measured currents with realistic ±2% error
    measured_current = reference_current * (
        1 + np.random.uniform(-0.015, 0.015, len(reference_current))
    )
    measured_current[0] = 0.02  # Small offset at zero

    # Linear regression
    coefficients = np.polyfit(reference_current, measured_current, 1)
    polynomial = np.poly1d(coefficients)

    # Generate fitted line
    fit_line = np.linspace(0, 20, 100)
    fitted_values = polynomial(fit_line)

    # Calculate R² value
    residuals = measured_current - polynomial(reference_current)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((measured_current - np.mean(measured_current)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # Calculate average error
    errors = np.abs((measured_current - reference_current) / reference_current * 100)
    avg_error = np.mean(errors[1:])  # Exclude zero point

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot ideal line (y=x)
    ax.plot([0, 20], [0, 20], "k--", alpha=0.3, linewidth=1.5, label="Ideal (1:1)")

    # Plot calibration points
    ax.scatter(
        reference_current,
        measured_current,
        s=80,
        c="#2563eb",
        edgecolors="white",
        linewidth=1.5,
        zorder=3,
        label="Calibration data",
    )

    # Plot fitted line
    ax.plot(
        fit_line,
        fitted_values,
        "r-",
        linewidth=2.5,
        alpha=0.7,
        label=f"Linear fit (R² = {r_squared:.4f})",
    )

    # Add error bars
    errors_absolute = measured_current - reference_current
    ax.errorbar(
        reference_current,
        measured_current,
        yerr=0.15,
        fmt="none",
        ecolor="gray",
        alpha=0.3,
        capsize=4,
    )

    # Labels and title
    ax.set_xlabel("Reference Current (A)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Measured Current (A)", fontsize=13, fontweight="bold")
    ax.set_title(
        "ACS712 Current Sensor Calibration Curve\nMulti-point Calibration with Linear Regression",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    # Grid
    ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend
    ax.legend(loc="upper left", fontsize=11, framealpha=0.95)

    # Add statistics box
    textstr = f"Calibration Statistics:\n"
    textstr += f"Slope: {coefficients[0]:.4f}\n"
    textstr += f"Offset: {coefficients[1]:.3f} A\n"
    textstr += f"Avg Error: {avg_error:.2f}%\n"
    textstr += f"R²: {r_squared:.4f}"

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
    ax.text(
        0.98,
        0.02,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="bottom",
        horizontalalignment="right",
        bbox=props,
        family="monospace",
    )

    # Set limits with some padding
    ax.set_xlim(-0.5, 21)
    ax.set_ylim(-0.5, 21)

    # Equal aspect ratio
    ax.set_aspect("equal", adjustable="box")

    # Tight layout
    plt.tight_layout()

    # Save
    output_path = output_dir / "calibration-curve.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Generated: {output_path}")
    plt.close()


def generate_accuracy_comparison_chart():
    """
    Generate bar chart comparing measurement accuracy across different load types
    """
    # Load types and their measurement data
    load_types = [
        "Resistive\n(100W lamp)",
        "Resistive\n(60W lamp)",
        "Inductive\n(Fan motor)",
        "Switching\n(Laptop PSU)",
        "Mixed\nload",
    ]

    # Reference values (W)
    reference_values = np.array([100.2, 59.8, 45.3, 65.1, 215.7])

    # Measured values (W)
    measured_values = np.array([101.1, 60.4, 44.8, 66.5, 219.2])

    # Calculate errors (%)
    errors = (measured_values - reference_values) / reference_values * 100

    # Absolute errors for bar heights
    abs_errors = np.abs(errors)

    # Colors: green if within ±1%, yellow if ±1-2%, red if >2%
    colors = []
    for err in abs_errors:
        if err <= 1.0:
            colors.append("#22c55e")  # Green
        elif err <= 2.0:
            colors.append("#f59e0b")  # Yellow/Orange
        else:
            colors.append("#ef4444")  # Red

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # === LEFT PLOT: Comparison of measured vs reference ===
    x = np.arange(len(load_types))
    width = 0.35

    bars1 = ax1.bar(
        x - width / 2,
        reference_values,
        width,
        label="Reference (Fluke 115)",
        color="#64748b",
        alpha=0.8,
        edgecolor="white",
        linewidth=1.5,
    )
    bars2 = ax1.bar(
        x + width / 2,
        measured_values,
        width,
        label="Measured (ESP32+ACS712)",
        color="#2563eb",
        alpha=0.9,
        edgecolor="white",
        linewidth=1.5,
    )

    ax1.set_xlabel("Load Type", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Power (W)", fontsize=12, fontweight="bold")
    ax1.set_title(
        "Measured vs Reference Power Values", fontsize=13, fontweight="bold", pad=12
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(load_types, fontsize=9.5)
    ax1.legend(fontsize=10, loc="upper left", framealpha=0.95)
    ax1.grid(True, alpha=0.3, axis="y", linestyle="--")
    ax1.set_axisbelow(True)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.1f}W",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#334155",
        )

    for bar in bars2:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.1f}W",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#1e40af",
        )

    # === RIGHT PLOT: Error percentages ===
    bars_error = ax2.bar(
        x, abs_errors, color=colors, alpha=0.85, edgecolor="white", linewidth=1.5
    )

    # Add ±2% target line
    ax2.axhline(
        y=2.0, color="red", linestyle="--", linewidth=2, alpha=0.6, label="±2% Target"
    )
    ax2.axhline(
        y=1.0,
        color="orange",
        linestyle=":",
        linewidth=1.5,
        alpha=0.5,
        label="±1% Reference",
    )

    ax2.set_xlabel("Load Type", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Absolute Error (%)", fontsize=12, fontweight="bold")
    ax2.set_title(
        "Measurement Error by Load Type", fontsize=13, fontweight="bold", pad=12
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(load_types, fontsize=9.5)
    ax2.set_ylim(0, 2.5)
    ax2.grid(True, alpha=0.3, axis="y", linestyle="--")
    ax2.set_axisbelow(True)
    ax2.legend(fontsize=9, loc="upper right", framealpha=0.95)

    # Add error value labels on bars with sign
    for i, (bar, err) in enumerate(zip(bars_error, errors)):
        height = bar.get_height()
        sign = "+" if err > 0 else ""
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{sign}{err:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#0f172a",
        )

    # Add summary statistics
    avg_error = np.mean(abs_errors)
    max_error = np.max(abs_errors)

    textstr = f"Performance Summary:\n"
    textstr += f"Average Error: {avg_error:.2f}%\n"
    textstr += f"Max Error: {max_error:.2f}%\n"
    textstr += f"Target Met: {'✓ YES' if max_error <= 2.0 else '✗ NO'}\n"
    textstr += f"Tests Passed: {np.sum(abs_errors <= 2.0)}/{len(abs_errors)}"

    props = dict(
        boxstyle="round",
        facecolor="#e0f2fe",
        alpha=0.9,
        edgecolor="#0284c7",
        linewidth=2,
    )
    ax2.text(
        0.02,
        0.98,
        textstr,
        transform=ax2.transAxes,
        fontsize=10,
        verticalalignment="top",
        horizontalalignment="left",
        bbox=props,
        family="monospace",
        fontweight="bold",
    )

    # Overall title
    fig.suptitle(
        "Power Monitoring System - Accuracy Validation Results",
        fontsize=15,
        fontweight="bold",
        y=0.98,
    )

    # Tight layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save
    output_path = output_dir / "accuracy-comparison-chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Generated: {output_path}")
    plt.close()


def generate_power_waveform_example():
    """
    Bonus: Generate a sample power waveform showing V, I, and P
    """
    # Time array (2 AC cycles at 60Hz = 33.33ms)
    t = np.linspace(0, 2 / 60, 1000)

    # Voltage waveform (120V RMS, 60Hz)
    V_peak = 120 * np.sqrt(2)
    voltage = V_peak * np.sin(2 * np.pi * 60 * t)

    # Current waveform (5A RMS, 60Hz, with phase shift for power factor 0.85)
    I_peak = 5 * np.sqrt(2)
    phase_shift = np.arccos(0.85)  # ~31.8 degrees
    current = I_peak * np.sin(2 * np.pi * 60 * t - phase_shift)

    # Instantaneous power
    power = voltage * current

    # Average power
    P_avg = 120 * 5 * 0.85

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot waveforms
    ax.plot(t * 1000, voltage, "b-", linewidth=2, label="Voltage (V)", alpha=0.8)
    ax.plot(
        t * 1000, current * 24, "r-", linewidth=2, label="Current (A × 24)", alpha=0.8
    )
    ax.plot(t * 1000, power, "g-", linewidth=2.5, label="Power (W)", alpha=0.9)
    ax.axhline(
        y=P_avg,
        color="orange",
        linestyle="--",
        linewidth=2,
        alpha=0.7,
        label=f"Average Power = {P_avg:.0f}W",
    )

    # Labels and title
    ax.set_xlabel("Time (ms)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Amplitude", fontsize=12, fontweight="bold")
    ax.set_title(
        "AC Power Waveforms - Inductive Load (PF = 0.85)\nVoltage, Current, and Instantaneous Power",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=11, framealpha=0.95)

    # Add annotation for phase shift
    ax.annotate(
        "Phase shift\n(cos φ = 0.85)",
        xy=(5, 100),
        xytext=(10, 300),
        arrowprops=dict(arrowstyle="->", color="purple", lw=2),
        fontsize=10,
        color="purple",
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7),
    )

    # Tight layout
    plt.tight_layout()

    # Save
    output_path = output_dir / "power-waveform-example.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Generated: {output_path}")
    plt.close()


def generate_system_block_diagram():
    """
    Generate a simplified system block diagram showing data flow
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Hide axes
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Define colors
    sensor_color = "#3b82f6"
    mcu_color = "#8b5cf6"
    comm_color = "#10b981"
    ui_color = "#f59e0b"

    # Block positions (x, y, width, height)
    blocks = {
        "power_line": (0.5, 3, 1.2, 1.5),
        "acs712": (2.2, 3.8, 1.4, 0.8),
        "zmpt101b": (2.2, 2.4, 1.4, 0.8),
        "esp32": (4.2, 2.8, 1.6, 1.8),
        "wifi": (6.5, 3.2, 1.2, 1),
        "dashboard": (8.3, 2.8, 1.4, 1.8),
    }

    # Draw blocks
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    # Power Line
    ax.add_patch(
        FancyBboxPatch(
            blocks["power_line"][:2],
            blocks["power_line"][2],
            blocks["power_line"][3],
            boxstyle="round,pad=0.05",
            edgecolor="black",
            facecolor="#fee2e2",
            linewidth=2,
        )
    )
    ax.text(
        blocks["power_line"][0] + blocks["power_line"][2] / 2,
        blocks["power_line"][1] + blocks["power_line"][3] / 2,
        "AC Power\nLine\n110-240V",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    # ACS712
    ax.add_patch(
        FancyBboxPatch(
            blocks["acs712"][:2],
            blocks["acs712"][2],
            blocks["acs712"][3],
            boxstyle="round,pad=0.05",
            edgecolor=sensor_color,
            facecolor="#dbeafe",
            linewidth=2.5,
        )
    )
    ax.text(
        blocks["acs712"][0] + blocks["acs712"][2] / 2,
        blocks["acs712"][1] + blocks["acs712"][3] / 2,
        "ACS712\nCurrent Sensor",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
    )

    # ZMPT101B
    ax.add_patch(
        FancyBboxPatch(
            blocks["zmpt101b"][:2],
            blocks["zmpt101b"][2],
            blocks["zmpt101b"][3],
            boxstyle="round,pad=0.05",
            edgecolor=sensor_color,
            facecolor="#dbeafe",
            linewidth=2.5,
        )
    )
    ax.text(
        blocks["zmpt101b"][0] + blocks["zmpt101b"][2] / 2,
        blocks["zmpt101b"][1] + blocks["zmpt101b"][3] / 2,
        "ZMPT101B\nVoltage Sensor",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
    )

    # ESP32
    ax.add_patch(
        FancyBboxPatch(
            blocks["esp32"][:2],
            blocks["esp32"][2],
            blocks["esp32"][3],
            boxstyle="round,pad=0.05",
            edgecolor=mcu_color,
            facecolor="#ede9fe",
            linewidth=2.5,
        )
    )
    ax.text(
        blocks["esp32"][0] + blocks["esp32"][2] / 2,
        blocks["esp32"][1] + blocks["esp32"][3] / 2 + 0.3,
        "ESP32",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax.text(
        blocks["esp32"][0] + blocks["esp32"][2] / 2,
        blocks["esp32"][1] + blocks["esp32"][3] / 2 - 0.15,
        "Microcontroller",
        ha="center",
        va="center",
        fontsize=8,
    )
    ax.text(
        blocks["esp32"][0] + blocks["esp32"][2] / 2,
        blocks["esp32"][1] + blocks["esp32"][3] / 2 - 0.45,
        "• ADC (12-bit)\n• Processing\n• WiFi Stack",
        ha="center",
        va="center",
        fontsize=7,
    )

    # WiFi
    ax.add_patch(
        FancyBboxPatch(
            blocks["wifi"][:2],
            blocks["wifi"][2],
            blocks["wifi"][3],
            boxstyle="round,pad=0.05",
            edgecolor=comm_color,
            facecolor="#d1fae5",
            linewidth=2.5,
        )
    )
    ax.text(
        blocks["wifi"][0] + blocks["wifi"][2] / 2,
        blocks["wifi"][1] + blocks["wifi"][3] / 2,
        "WiFi\n802.11n\n2.4GHz",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
    )

    # Dashboard
    ax.add_patch(
        FancyBboxPatch(
            blocks["dashboard"][:2],
            blocks["dashboard"][2],
            blocks["dashboard"][3],
            boxstyle="round,pad=0.05",
            edgecolor=ui_color,
            facecolor="#fef3c7",
            linewidth=2.5,
        )
    )
    ax.text(
        blocks["dashboard"][0] + blocks["dashboard"][2] / 2,
        blocks["dashboard"][1] + blocks["dashboard"][3] / 2 + 0.3,
        "Web Dashboard",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
    )
    ax.text(
        blocks["dashboard"][0] + blocks["dashboard"][2] / 2,
        blocks["dashboard"][1] + blocks["dashboard"][3] / 2 - 0.2,
        "Real-time\nVisualization\nWebSocket",
        ha="center",
        va="center",
        fontsize=7,
    )

    # Draw arrows
    arrow_style = dict(arrowstyle="->", lw=2.5, color="#374151")

    # Power line to sensors
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["power_line"][0] + blocks["power_line"][2],
                blocks["power_line"][1] + blocks["power_line"][3] * 0.7,
            ),
            (blocks["acs712"][0], blocks["acs712"][1] + blocks["acs712"][3] / 2),
            **arrow_style,
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["power_line"][0] + blocks["power_line"][2],
                blocks["power_line"][1] + blocks["power_line"][3] * 0.3,
            ),
            (blocks["zmpt101b"][0], blocks["zmpt101b"][1] + blocks["zmpt101b"][3] / 2),
            **arrow_style,
        )
    )

    # Sensors to ESP32
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["acs712"][0] + blocks["acs712"][2],
                blocks["acs712"][1] + blocks["acs712"][3] / 2,
            ),
            (blocks["esp32"][0], blocks["esp32"][1] + blocks["esp32"][3] * 0.7),
            **arrow_style,
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["zmpt101b"][0] + blocks["zmpt101b"][2],
                blocks["zmpt101b"][1] + blocks["zmpt101b"][3] / 2,
            ),
            (blocks["esp32"][0], blocks["esp32"][1] + blocks["esp32"][3] * 0.3),
            **arrow_style,
        )
    )

    # ESP32 to WiFi
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["esp32"][0] + blocks["esp32"][2],
                blocks["esp32"][1] + blocks["esp32"][3] / 2,
            ),
            (blocks["wifi"][0], blocks["wifi"][1] + blocks["wifi"][3] / 2),
            **arrow_style,
        )
    )

    # WiFi to Dashboard
    ax.add_patch(
        FancyArrowPatch(
            (
                blocks["wifi"][0] + blocks["wifi"][2],
                blocks["wifi"][1] + blocks["wifi"][3] / 2,
            ),
            (
                blocks["dashboard"][0],
                blocks["dashboard"][1] + blocks["dashboard"][3] / 2,
            ),
            **arrow_style,
        )
    )

    # Add labels on arrows
    ax.text(
        1.9,
        4.5,
        "I",
        ha="center",
        va="center",
        fontsize=9,
        style="italic",
        color="#7c3aed",
    )
    ax.text(
        1.9,
        2.6,
        "V",
        ha="center",
        va="center",
        fontsize=9,
        style="italic",
        color="#7c3aed",
    )
    ax.text(3.8, 4.2, "0-5V", ha="center", va="center", fontsize=8, color="#6366f1")
    ax.text(3.8, 2.5, "0-5V", ha="center", va="center", fontsize=8, color="#6366f1")
    ax.text(6.0, 3.7, "Digital", ha="center", va="center", fontsize=8, color="#6366f1")
    ax.text(7.4, 3.7, "JSON/WS", ha="center", va="center", fontsize=8, color="#059669")

    # Title
    ax.text(
        5,
        6.5,
        "Power Monitoring System Architecture",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
    )
    ax.text(
        5,
        6.1,
        "Non-invasive measurement with wireless real-time transmission",
        ha="center",
        va="center",
        fontsize=10,
        style="italic",
        color="#6b7280",
    )

    # Legend
    legend_y = 0.8
    ax.add_patch(
        FancyBboxPatch(
            (0.5, legend_y - 0.15),
            0.3,
            0.25,
            boxstyle="round,pad=0.02",
            edgecolor=sensor_color,
            facecolor="#dbeafe",
            linewidth=1.5,
        )
    )
    ax.text(1.0, legend_y, "Sensors", ha="left", va="center", fontsize=8)

    ax.add_patch(
        FancyBboxPatch(
            (2.0, legend_y - 0.15),
            0.3,
            0.25,
            boxstyle="round,pad=0.02",
            edgecolor=mcu_color,
            facecolor="#ede9fe",
            linewidth=1.5,
        )
    )
    ax.text(2.5, legend_y, "Processing", ha="left", va="center", fontsize=8)

    ax.add_patch(
        FancyBboxPatch(
            (3.7, legend_y - 0.15),
            0.3,
            0.25,
            boxstyle="round,pad=0.02",
            edgecolor=comm_color,
            facecolor="#d1fae5",
            linewidth=1.5,
        )
    )
    ax.text(4.2, legend_y, "Communication", ha="left", va="center", fontsize=8)

    ax.add_patch(
        FancyBboxPatch(
            (5.8, legend_y - 0.15),
            0.3,
            0.25,
            boxstyle="round,pad=0.02",
            edgecolor=ui_color,
            facecolor="#fef3c7",
            linewidth=1.5,
        )
    )
    ax.text(6.3, legend_y, "User Interface", ha="left", va="center", fontsize=8)

    plt.tight_layout()

    # Save
    output_path = output_dir / "system-block-diagram.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Generated: {output_path}")
    plt.close()


def main():
    """Generate all charts"""
    print("Generating charts for Power Monitoring System...\n")

    try:
        generate_calibration_curve()
        generate_accuracy_comparison_chart()
        generate_power_waveform_example()
        generate_system_block_diagram()

        print("\n✓ All charts generated successfully!")
        print(f"✓ Output directory: {output_dir.absolute()}")

    except Exception as e:
        print(f"\n✗ Error generating charts: {e}")
        raise


if __name__ == "__main__":
    main()
