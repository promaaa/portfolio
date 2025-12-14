# Chart Generation Scripts

This directory contains Python scripts to generate publication-quality charts and graphs for the Power Monitoring System research article.

## Requirements

```bash
pip install matplotlib numpy
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

### Generate All Charts

Run the main script to generate all charts at once:

```bash
python generate_charts.py
```

This will create the following images in the `images/` directory:

1. **calibration-curve.png** - Linear regression calibration curve showing measured vs reference current values
2. **accuracy-comparison-chart.png** - Bar chart comparing measurement accuracy across different load types
3. **power-waveform-example.png** - AC waveform visualization showing voltage, current, and power (bonus)

## Generated Charts

### 1. Calibration Curve (`calibration-curve.png`)

- **Purpose**: Demonstrates the linear calibration of the ACS712 current sensor
- **Features**:
  - Multi-point calibration data (0-20A range)
  - Linear regression fit line with R² value
  - Comparison against ideal 1:1 line
  - Error bars showing measurement uncertainty
  - Statistics box with slope, offset, average error, and R²

### 2. Accuracy Comparison Chart (`accuracy-comparison-chart.png`)

- **Purpose**: Validates measurement accuracy across different load types
- **Features**:
  - Side-by-side comparison of reference vs measured values
  - Error percentage analysis with color-coded bars
  - ±2% target accuracy line
  - Performance summary with pass/fail indication
  - Includes resistive, inductive, and switching loads

### 3. Power Waveform Example (`power-waveform-example.png`)

- **Purpose**: Illustrates AC power measurement with phase shift
- **Features**:
  - Voltage and current waveforms (60Hz)
  - Instantaneous power calculation
  - Average power line
  - Phase shift annotation (power factor 0.85)

## Customization

You can modify the data in each function to match your actual calibration and test results:

### Calibration Data

Edit the `reference_current` and `measured_current` arrays in `generate_calibration_curve()`:

```python
reference_current = np.array([0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0])
measured_current = np.array([...])  # Your actual measurements
```

### Accuracy Test Data

Edit the load types and measurements in `generate_accuracy_comparison_chart()`:

```python
reference_values = np.array([100.2, 59.8, 45.3, 65.1, 215.7])
measured_values = np.array([101.1, 60.4, 44.8, 66.5, 219.2])
```

## Output

All charts are saved as high-resolution PNG files (300 DPI) suitable for publication:

- **Location**: `../images/`
- **Resolution**: 300 DPI
- **Format**: PNG with white background
- **Size**: Varies (10-14 inches wide, 6-7 inches tall)

## Styling

Charts use professional scientific publication styling:

- Seaborn dark grid style
- Sans-serif fonts (Arial/DejaVu Sans)
- Color scheme matching the website theme
- Accessible color choices (colorblind-friendly where possible)

## Adding New Charts

To add a new chart:

1. Create a new function in `generate_charts.py`:

```python
def generate_my_new_chart():
    """Description of the chart"""
    # Your plotting code here
    output_path = output_dir / "my-new-chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: {output_path}")
    plt.close()
```

2. Call it from `main()`:

```python
def main():
    generate_calibration_curve()
    generate_accuracy_comparison_chart()
    generate_my_new_chart()  # Add here
```

## License

MIT License - Free to use and modify for your research projects.

## Notes

- The script uses reproducible random seeds (`np.random.seed(42)`) for consistent output
- All measurements are simulated but based on realistic tolerances
- Charts are optimized for both digital display and print publication
- Data can be easily replaced with actual experimental results