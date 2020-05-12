import pandas as pd


class Optimizer:
    def __init__(self, model=None):
        """
        Initialize optimizer class.
        :param model: Pass in predefined model
        """
        self.model = model

    def train(self, x, y):
        """
        Train model with new data
        :param x: Features
        :param y: Labels
        :return: None
        """
        pass

    def save(self, path):
        """Save model to path"""
        pass

    def compute_portfolio(self, x) -> pd.DataFrame:
        """

        :return: DataFrame of optimal portfolio allocation
        Compute portfolio based on currently trained model
        """
        return pd.DataFrame()
