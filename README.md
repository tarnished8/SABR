# SABR Model Calibration and Option Pricing

This project calibrates the SABR model to market data for options on the Dow Jones Index (DJX) and then uses the calibrated model to price an Asian option via Monte Carlo simulation.

## Structure

- `data/`: Contains the market data in an Excel file.
- `notebooks/`: Contains the original Jupyter notebook.
- `src/`: Contains the Python source code, organized into modules:
    - `data_loader.py`: Loads and cleans the market data.
    - `sabr_model.py`: Defines the SABR model.
    - `calibration.py`: Calibrates the SABR model to the market data.
    - `simulation.py`: Simulates the SABR model and prices the Asian option.
    - `visualization.py`: Visualizes the implied volatility smile.
- `main.py`: The main script to run the entire workflow.
- `requirements.txt`: The required Python packages.

## Usage

1. Install the required packages:

```
pip install -r requirements.txt
```

2. Run the main script:

```
python main.py
```
