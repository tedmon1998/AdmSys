import pytest
import app
import os.path


def test_create_database():  # Тест на создание БД
    app.init_db()
    assert os.path.exists(app.db_name) == True


def test_clients():  # Тест на наличие столбцов в Clients
    assert app.Clients.name == False
    assert app.Clients.city == False
    assert app.Clients.address == False


def test_orders():  # Тест на наличие столбцов в Orders
    assert app.Orders.clients == False
    assert app.Orders.amount == False
    assert app.Orders.date == False
    assert app.Orders.description == False


def test_sum_clients():  # Тест на наличие 10 строк в Clients
    app.fill_db()
    assert len(app.Clients.select()) > 100


def test_sum_orders():  # Тест на наличие 10 строк в Orders
    app.fill_db()
    assert len(app.Orders.select()) > 10
