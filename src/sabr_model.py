import numpy as np

class SABRModel:
    @staticmethod
    def sabr_vol(F, K, alpha, beta, rho, nu):
        if F == K:
            term1 = alpha / (F ** (1 - beta))
            term2 = 1 + (((1 - beta) ** 2) / 24) * (alpha ** 2 / (F ** (2 - 2 * beta))) +             (rho * beta * nu * alpha) / (4 * (F ** (1 - beta))) +             ((2 - 3 * rho ** 2) / 24) * nu ** 2
            return term1 * term2
        else:
            logFK = np.log(F / K)
            FK_avg = (F * K) ** ((1 - beta) / 2)
            z = (nu / alpha) * FK_avg * logFK
            if abs(z) < 1e-8:
                # Recalculate with a small perturbation to avoid division by zero
                epsilon = 1e-5
                return SABRModel.sabr_vol(F + epsilon, K, alpha, beta, rho, nu)
            x_z = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
            term1 = alpha / ((F * K) ** ((1 - beta) / 2))
            return term1 * (z / x_z)
