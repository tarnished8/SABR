import numpy as np
import pandas as pd
import os
from src.data_loader import DataLoader
from src.calibration import Calibration
from src.simulation import Simulation
from src.visualization import Visualization

def main():  
    # Load and clean data
    data_loader = DataLoader(file_path='data/DOWJONESdata.xlsx')
    df = data_loader.load_and_clean_data()

    # Visualize implied volatility
    Visualization.plot_implied_volatility(df)

    # Calibrate SABR model
    r = 0.0435
    S0 = 448.5 
    collection_date = pd.to_datetime("2025-01-28")
    init_params = [0.2, 0.2, -0.5, 0.2]
    
    best_params, error = Calibration.simulated_annealing(
        Calibration.global_calibration_error, 
        init_params, 
        df, 
        collection_date, 
        S0, 
        r,
        T0=1.0, 
        alpha_temp=0.95, 
        n_iter=2000
    )
    
    print("Global Calibrated Parameters [alpha, beta, rho, nu]:", best_params)
    print("Global Calibration Error:", error)

    # Price Asian option
    T_maturity = 1
    F = S0 * np.exp(r * T_maturity)
    print(f"Forward Price F at T = {T_maturity} using r = {r} is: {F:.2f}")

    sigma0, beta_cal, rho_cal, nu_cal = best_params
    S0_sim = F
    n_steps = 252
    n_paths = 10000
    strike = S0_sim

    S_paths, _ = Simulation.simulate_sabr(
        S0_sim, 
        sigma0, 
        beta_cal, 
        rho_cal, 
        nu_cal, 
        T=T_maturity, 
        n_steps=n_steps, 
        n_paths=n_paths
    )
    
    asian_price = Simulation.price_asian_option(S_paths, strike)
    print("Asian Option Price:", asian_price)

if __name__ == "__main__":
    main()
