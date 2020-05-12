import pytest
from Optimizer import Optimizer

@pytest.fixture
def model_path():
    return 'models'


@pytest.fixture
def x():
    pass


@pytest.fixture
def y():
    pass


@pytest.fixture
def optimizer():
    return Optimizer()


def test_train_accepts_correct_data_format(optimizer, x, y):
    assert optimizer.train(x, y) is None


def test_portfolio_has_symbols_and_allocations():
    pass


def test_save_model(optimizer):
    pass


def test_load_model(optimizer):
    pass
