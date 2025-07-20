import numpy as np
import pandas as pd
from src.sabr_model import SABRModel

class Calibration:
    @staticmethod
    def global_calibration_error(params, market_df, collection_date, S0, r):
        alpha, beta, rho, nu = params
        error = 0.0
        for maturity, group in market_df.groupby('ExpirationDate'):
            T = (pd.to_datetime(maturity) - collection_date).days / 365.0
            if group['IFwd'].notna().any():
                F = group['IFwd'].dropna().iloc[0]
            else:
                F = S0 * np.exp(r * T)
            for idx, row in group.iterrows():
                K = row['Strike']
                vol_market = row['ImpliedVolatility']
                vol_model = SABRModel.sabr_vol(F, K, alpha, beta, rho, nu)
                error += (vol_market - vol_model) ** 2
        return error

    @staticmethod
    def simulated_annealing(obj_func, init_params, market_df, collection_date, S0, r,
                            T0=1.0, alpha_temp=0.95, n_iter=1000):
        current_params = np.array(init_params)
        current_error = obj_func(current_params, market_df, collection_date, S0, r)
        best_params = current_params.copy()
        best_error = current_error
        T = T0
        for i in range(n_iter):
            new_params = current_params + np.random.normal(scale=0.01, size=current_params.shape)
            new_params[1] = np.clip(new_params[1], 0.0, 1.0)
            new_params[2] = np.clip(new_params[2], -0.999, 0.999)
            new_params[0] = max(new_params[0], 1e-5)
            new_params[3] = max(new_params[3], 1e-5)
            
            new_error = obj_func(new_params, market_df, collection_date, S0, r)
            delta = new_error - current_error
            
            if delta < 0 or np.exp(-delta / T) > np.random.rand():
                current_params = new_params
                current_error = new_error
                if new_error < best_error:
                    best_params = new_params
                    best_error = new_error
            T *= alpha_temp
        return best_params, best_error
