import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from typing import Optional

class Visualization:
    @staticmethod
    def plot_implied_volatility(df: pd.DataFrame, output_dir: str = 'output') -> None:
        """
        Plot implied volatility smile for each maturity in the dataset.

        Args:
            df: DataFrame containing options data with columns 'ExpirationDate', 'Strike', 'ImpliedVolatility'
            output_dir: Directory to save the plots (default: 'output')

        Raises:
            ValueError: If required columns are missing from the DataFrame
            TypeError: If ExpirationDate column is not datetime type
        """
        # Validate input data
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")

        required_columns = ['ExpirationDate', 'Strike', 'ImpliedVolatility']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Ensure ExpirationDate is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['ExpirationDate']):
            try:
                df = df.copy()
                df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'])
            except Exception as e:
                raise TypeError(f"Could not convert ExpirationDate to datetime: {e}")

        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            raise OSError(f"Could not create output directory '{output_dir}': {e}")

        # Set seaborn style
        sns.set(style="whitegrid")

        # Get unique maturities and sort them
        unique_maturities = sorted(df['ExpirationDate'].dropna().unique())

        if not unique_maturities:
            raise ValueError("No valid expiration dates found in the data")

        # Plot for each maturity
        for maturity in unique_maturities:
            try:
                subset = df[df['ExpirationDate'] == maturity].copy()

                # Skip if no data for this maturity
                if subset.empty:
                    print(f"Warning: No data found for maturity {maturity.date()}")
                    continue

                # Remove rows with NaN values in required columns
                subset = subset.dropna(subset=['Strike', 'ImpliedVolatility'])

                if subset.empty:
                    print(f"Warning: No valid data points for maturity {maturity.date()}")
                    continue

                # Sort by strike for better visualization
                subset = subset.sort_values('Strike')

                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 6))

                try:
                    sns.lineplot(data=subset, x='Strike', y='ImpliedVolatility', marker='o', ax=ax)

                    ax.set_title(f'Implied Volatility vs Strike for Maturity {maturity.date()}')
                    ax.set_xlabel('Strike Price')
                    ax.set_ylabel('Implied Volatility')
                    ax.grid(True)

                    # Save the plot
                    filename = f'implied_volatility_smile_{maturity.date()}.png'
                    filepath = os.path.join(output_dir, filename)
                    plt.savefig(filepath, dpi=300, bbox_inches='tight')
                    print(f"Saved plot: {filepath}")

                    # Show the plot
                    plt.show()

                except Exception as e:
                    print(f"Error creating plot for maturity {maturity.date()}: {e}")

                finally:
                    # Always close the figure to free memory
                    plt.close(fig)

            except Exception as e:
                print(f"Error processing maturity {maturity}: {e}")
                continue
