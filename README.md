# algo-trading

## Overview
This trading system consists of a portfolio optimizer and trading strategy.

The portfolio optimizer is responsible for training new models as well as returning a target portfolio with optimal 
allocations. We use ML models to return the target portfolio.

The trading strategy is responsible for executing trades to reach the target portfolio returned by the optimizer.

## Architecture (Proposed / Current)
- **Backtrader** for local backtesting
- **Pytorch** for ML models 

## Setup
To install the dependencies, pipenv is used. You can do:

``pipenv install``

## Running
From the top directory, run **main.py**:
``python main.py``

## References
To learn about Backtrader, take a look here: https://www.backtrader.com/docu/quickstart/quickstart/