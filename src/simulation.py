import numpy as np

class Simulation:
    @staticmethod
    def simulate_sabr(S0, sigma0, beta, rho, nu, T=1.0, n_steps=252, n_paths=10000):
        dt = T / n_steps
        S_paths = np.zeros((n_paths, n_steps + 1))
        sigma_paths = np.zeros((n_paths, n_steps + 1))
        S_paths[:, 0] = S0
        sigma_paths[:, 0] = sigma0
        
        for t in range(1, n_steps + 1):
            Z1 = np.random.normal(0, 1, n_paths)
            Z2 = np.random.normal(0, 1, n_paths)
            dW = np.sqrt(dt) * Z1
            dZ = np.sqrt(dt) * (rho * Z1 + np.sqrt(1 - rho**2) * Z2)
            
            base = np.maximum(S_paths[:, t-1], 1e-5)
            S_paths[:, t] = S_paths[:, t-1] + sigma_paths[:, t-1] * (base ** beta) * dW
            sigma_paths[:, t] = sigma_paths[:, t-1] + nu * sigma_paths[:, t-1] * dZ
        return S_paths, sigma_paths

    @staticmethod
    def price_asian_option(S_paths, strike):
        S_avg = S_paths.mean(axis=1)
        payoffs = np.maximum(S_avg - strike, 0)
        return np.mean(payoffs)
