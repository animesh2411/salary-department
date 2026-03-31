# 🚀 Quick Start Guide

Welcome to **Salary Department**! Get up and running in minutes.

## Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)

## Installation & Setup

### 1. Clone or Navigate to the Repository

```bash
cd salary-department
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Home Page Features

- **Navigation Sidebar** – Choose between different tools
- **Home Dashboard** – Overview of all available tools
- **Tax Calculator** – Compare Old vs New tax regimes
- **Coming Soon** – Placeholder for future features

## Using the Tax Calculator

### Input Section (Left Column)

1. **Gross Annual Salary** – Enter your total annual salary (exact amount)
2. **Old Regime Deductions** (expandable, all in exact rupees):
   - **80C** – Insurance, PPF, ELSS (max ₹1.5L) - Enter exact amount
   - **80D** – Health Insurance (max ₹2L) - Enter exact amount
   - **HRA** – House Rent Allowance in rupees (calculated separately) - Enter exact amount
   - **Other Deductions** – Any other eligible deductions in rupees

   💡 **HRA Calculation Tip:** Calculate HRA as (Rent - 10% of salary), but max 50% of salary. Enter the final amount.

### Output Section (Right Column)

- **Quick Recommendation** – Which regime is better for you
- **Comparison Tab** – Side-by-side metrics and charts
- **New Regime Tab** – Detailed New Regime calculation
- **Old Regime Tab** – Detailed Old Regime calculation

### How to Get Results

Simply adjust the sliders and inputs, and the calculation updates in real-time!

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=modules --cov-report=html
```

### Run Specific Test Class

```bash
pytest tests/test_tax_calculator.py::TestNewRegime -v
```

## Code Quality

### Lint Code with Flake8

```bash
flake8 modules/ shared/ app.py
```

### Auto-Format Code (optional)

```bash
pip install black
black modules/ shared/ app.py
```

## Project Structure

```
salary-department/
├── app.py                          # Main entry point
├── modules/
│   └── tax_calculator/             # Tax Calculator module
│       ├── ui.py                   # Streamlit UI
│       ├── service.py              # Business logic
│       ├── models.py               # Data structures
│       ├── constants.py            # Tax rules
│       ├── utils.py                # Helper functions
│       └── __init__.py
├── shared/
│   ├── components.py               # Reusable UI components
│   ├── helpers.py                  # Shared utilities
│   └── __init__.py
├── tests/
│   ├── test_tax_calculator.py      # Test suite
│   └── __init__.py
├── requirements.txt                # Dependencies
├── README.md                        # Full documentation
└── QUICKSTART.md                   # This file
```

## Troubleshooting

### "Module not found" Error

Make sure you're in the correct directory and virtual environment is activated:

```bash
cd salary-department
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Streamlit Not Starting

Try clearing Streamlit cache:

```bash
streamlit cache clear
streamlit run app.py
```

### Tests Failing

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
pytest tests/ -v
```

## Next Steps

1. **Explore the Home Page** – See all available tools
2. **Try the Tax Calculator** – Compare tax regimes
3. **Adjust Values** – See real-time calculations
4. **Check Documentation** – Read README.md for detailed info
5. **Run Tests** – Verify everything works: `pytest tests/ -v`

## Tips & Tricks

### For Developers

- **Add a New Module:** Follow the structure in `modules/tax_calculator/`
- **Extend UI:** Reuse components from `shared/components.py`
- **Test Your Code:** Use `pytest` for unit tests
- **Check Quality:** Run `flake8` before committing

### For Users

- **New Regime** – Usually better if you have few deductions
- **Old Regime** – Better if you invest heavily (PPF, Insurance, etc.)
- **Sliders** – Use sliders to adjust deductions incrementally
- **Comparison** – Check the bar chart for visual comparison

## Support & Questions

- 📖 **Documentation** – See `README.md`
- 🧪 **Tests** – Run `pytest tests/ -v`
- 🔍 **Code** – Browse `modules/` for implementation
- 💬 **Issues** – Check GitHub issues or create a new one

## License

MIT License – Free to use and modify

---

**Happy Calculating!** 💰📊

For more details, see [README.md](README.md)

