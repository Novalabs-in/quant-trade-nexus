import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

class QuantTradingEngine:
    """
    ML-Driven Quantitative Trading Engine & Simulator
    Trains predictive XGBoost models on technical indicators and runs backtests.
    """
    def __init__(self, initial_capital=100000.0):
        self.capital = initial_capital
        self.positions = 0
        self.model = XGBClassifier(n_estimators=100, max_depth=3)

    def compute_indicators(self, df):
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()
        df['RSI'] = 50.0 # Placeholder for simplicity
        df.dropna(inplace=True)
        return df

    def train_model(self, df):
        df = self.compute_indicators(df)
        X = df[['SMA_10', 'SMA_30', 'RSI']]
        y = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        print("Model trained successfully!")

    def backtest(self, test_df):
        test_df = self.compute_indicators(test_df)
        X = test_df[['SMA_10', 'SMA_30', 'RSI']]
        predictions = self.model.predict(X)
        
        for price, signal in zip(test_df['Close'], predictions):
            if signal == 1 and self.capital >= price: # BUY
                self.positions += 1
                self.capital -= price
            elif signal == 0 and self.positions > 0: # SELL
                self.positions -= 1
                self.capital += price
        
        final_value = self.capital + (self.positions * test_df['Close'].iloc[-1])
        return final_value

if __name__ == "__main__":
    dates = pd.date_range(start="2026-01-01", periods=100)
    data = {"Close": np.random.normal(150, 5, 100).cumsum()}
    df = pd.DataFrame(data, index=dates)
    engine = QuantTradingEngine()
    engine.train_model(df.copy())
    print("Backtest Portfolio Final Value:", engine.backtest(df.copy()))
