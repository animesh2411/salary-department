# Salary Department 💼

A comprehensive, modular Streamlit application for salary-related financial tools.
Access the application here: https://yoursalary.streamlit.app/

## Features 🌟

- **Tax Calculator** – Calculate and compare income tax under Old vs New Regime (India FY 2026-27)
- **Modular Architecture** – Easy to add new tools and features
- **Production-Grade Code** – Clean, testable, scalable design
- **Comprehensive Testing** – Full pytest coverage
- **CI/CD Pipeline** – GitHub Actions for automated testing

## Project Structure

```
salary-department/
├── app.py                          # Main Streamlit entry point (home page)
├── requirements.txt                # Python dependencies
├── modules/
│   ├── __init__.py
│   └── tax_calculator/             # Tax Calculator Module
│       ├── __init__.py
│       ├── constants.py            # Tax slabs, deduction limits
│       ├── models.py               # Data structures (SalaryInput, TaxResult)
│       ├── service.py              # Core business logic
│       ├── ui.py                   # Streamlit UI components
│       └── utils.py                # Helper functions
├── shared/
│   ├── __init__.py
│   ├── components.py               # Reusable UI components
│   └── helpers.py                  # Shared utility functions
├── tests/
│   ├── __init__.py
│   └── test_tax_calculator.py      # Tax calculator tests
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD pipeline
└── .gitignore
```

## Installation

### Prerequisites
- Python 3.9+
- pip or conda

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd salary-department
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Accessing Features

1. **Home Page** – Dashboard with all available tools
2. **Tax Calculator** – Calculate and compare tax between Old vs New Regime
3. **More Tools** – Preview of upcoming features

## Using the Tax Calculator

### Inputs
- **Gross Annual Salary** – Your total annual salary
- **Deductions (Old Regime Only):**
  - 80C (Insurance, PPF, etc.) – Max ₹1.5L
  - 80D (Health Insurance) – Max ₹2L
  - HRA (House Rent Allowance) – Percentage-based
  - Other Deductions – Custom deductions

### Outputs
- **Tax Comparison** – Side-by-side comparison of both regimes
- **Savings Analysis** – How much you can save with recommended regime
- **Detailed Breakdown** – Taxable income, effective tax rate, take-home salary
- **Visual Charts** – Bar charts comparing tax and take-home salary

### Tax Rules (FY 2026-27)

#### New Regime
| Income Range | Tax Rate |
|---|---|
| ₹0 – ₹4L | 0% |
| ₹4L – ₹8L | 5% |
| ₹8L – ₹12L | 10% |
| ₹12L – ₹16L | 15% |
| ₹16L – ₹20L | 20% |
| ₹20L – ₹24L | 25% |
| > ₹24L | 30% |

**Rules:**
- Standard Deduction: ₹75,000
- Rebate: Tax = 0 if taxable income ≤ ₹12L
- No other deductions allowed

#### Old Regime
| Income Range | Tax Rate |
|---|---|
| ₹0 – ₹2.5L | 0% |
| ₹2.5L – ₹5L | 5% |
| ₹5L – ₹10L | 20% |
| > ₹10L | 30% |

**Rules:**
- Standard Deduction: ₹50,000
- Allows: 80C, 80D, HRA, and other deductions
- No rebate

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage report:
```bash
pytest tests/ --cov=modules --cov-report=html
```

### Test Coverage

The test suite covers:
- New Regime tax calculations
- Old Regime tax calculations
- Tax comparisons and recommendations
- Edge cases and boundary conditions
- Deduction validations

## Code Quality

The project uses:
- **Flake8** – Code linting (PEP 8 compliance)
- **Pytest** – Unit testing
- **Pytest-cov** – Code coverage reporting

## Architecture Highlights

### Modular Design
- **Modules are self-contained** – Each module has its own logic, UI, and tests
- **Shared components** – Common UI elements and utilities in `shared/`
- **Easy to extend** – Add new modules without affecting existing code

### Separation of Concerns
- **models.py** – Data structures only
- **constants.py** – Configuration and constants
- **service.py** – Pure business logic (testable, no side effects)
- **ui.py** – Streamlit UI (handles presentation)
- **utils.py** – Helper functions

### Best Practices
- Type hints throughout
- Comprehensive docstrings
- No hardcoded values (all in constants)
- Pure functions (service layer)
- Full test coverage

## Adding New Modules

To add a new salary tool, follow this pattern:

```python
# modules/new_tool/
# ├── __init__.py
# ├── constants.py
# ├── models.py
# ├── service.py
# ├── ui.py
# └── utils.py
```

1. Create the module structure
2. Implement business logic in `service.py`
3. Create UI in `ui.py`
4. Update `shared/helpers.py` to register the module
5. Add module to `app.py` navigation
6. Write tests in `tests/`

## Configuration

### Requirements
See `requirements.txt` for all dependencies:
- **streamlit** – Web framework
- **pandas** – Data manipulation
- **pytest** – Testing framework
- **flake8** – Code linting

### Environment Variables

Currently, no environment variables are required. Future versions may support:
- Database connections
- API keys
- Custom configuration

## Deployment

The app can be deployed on:
- **Streamlit Cloud** – Free hosting (recommended)
- **Heroku** – Traditional deployment
- **AWS/Azure** – Custom deployments
- **Docker** – Containerized deployment

### Streamlit Cloud Deployment

```bash
git push origin main
# Visit https://streamlit.io/cloud and connect your GitHub repo
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

### Development Guidelines

- Write clean, documented code
- Add tests for new features
- Follow PEP 8 style guide
- Update README for new features
- Ensure CI/CD pipeline passes

## Roadmap 🗺️

### Phase 1 (Current)
- ✅ Tax Calculator (Old vs New Regime)
- ✅ Modular architecture
- ✅ Testing framework
- ✅ CI/CD pipeline

### Phase 2 (Planned)
- 📅 Salary Analyzer
- 📅 Retirement Planner
- 📅 Investment Recommendations

### Phase 3 (Future)
- 📅 Budget Planner
- 📅 Expense Tracker
- 📅 Wealth Management Tools

## License

This project is licensed under the MIT License – see LICENSE file for details.

## Disclaimer

⚠️ **Important:** This tool is for **educational and informational purposes only**. 
It should not be considered as professional financial or tax advice. 
Always consult with a qualified Chartered Accountant (CA) for:
- Final tax planning decisions
- Specific deduction claims
- Complex financial situations
- Professional tax compliance

The developers are not liable for any financial decisions made based on this tool.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check documentation

## Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)

---

**Version:** 1.0.0  
**Last Updated:** April 2026  
**Maintained by:** Salary Department Team

