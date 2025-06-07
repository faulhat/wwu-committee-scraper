import os
import pytest
from app import app
from flask import url_for
import sqlite3
from unittest.mock import MagicMock, patch
import pandas as pd


# Unit tests for Flaskapp
# Currently sets up a test client for addressing route behavior (no 404 page set up currently so no tests for that), 
#   sets up a mock database to simulate a database connection and returning rows from a SQL query, and simulates
#   the excel dump to test the file generation and exceptions with logic.

# These tests are for addressing route behavior with a test client.
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_serves_file(monkeypatch, client):
    monkeypatch.setattr(os.path, "isdir", lambda path: True)
    monkeypatch.setattr("app.send_file", lambda x: "mocked index.html")
    response = client.get("/")
    assert b"mocked index.html" in response.data or isinstance(response, str)

def test_data_route_serves(monkeypatch, client):
    monkeypatch.setattr(os.path, "isdir", lambda path: True)
    monkeypatch.setattr("app.send_from_directory", lambda directory, path: f"mocked {path}")
    response = client.get("/data/test.json")
    assert b"mocked test.json" in response.data or isinstance(response, str)

def test_pages_list_empty(tmp_path, monkeypatch, client):
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    response = client.get("/pages.json")
    assert response.status_code == 200
    assert response.json == []

def test_pages_excel(tmp_path, monkeypatch, client):
    monkeypatch.setattr("app.dump_to_excel", lambda db, excel: None)
    monkeypatch.setattr("app.send_file", lambda path: "mocked xlsx")
    response = client.get("/pages.xlsx")
    assert b"mocked xlsx" in response.data or isinstance(response, str)

def test_dist_serves_file(monkeypatch, client):
    monkeypatch.setattr(os.path, "isdir", lambda path: True)
    monkeypatch.setattr("app.send_file", lambda path: "mocked file content")
    response = client.get("/somefile.js")
    assert b"mocked file content" in response.data or isinstance(response, str)


# Testing with a mock SQLite database. verifies an SQL query as well.
def test_pages_list_with_mocked_db(client):
    # Define mock rows returned by cursor.fetchall
    mock_rows = [
        ("https://example.com", "Example Title", 10, "before", "keyword", "after"),
        ("https://another.com", None, 5, "before2", "keyword2", "after2"),
    ]

    # Expected JSON response based on full_pages_table logic
    expected_json = [
        {
            "url": "https://example.com",
            "title": "Example Title",
            "score": 10,
            "summary_before": "before",
            "summary_keyword": "keyword",
            "summary_after": "after"
        },
        {
            "url": "https://another.com",
            "title": "https://another.com",  # fallback to URL if title is None
            "score": 5,
            "summary_before": "before2",
            "summary_keyword": "keyword2",
            "summary_after": "after2"
        }
    ]

    # Mock the cursor and connection
    #mock_cursor = sqlite3.connect(":memory:")
    #mock_cursor.fetchall.return_value = mock_rows

    #mock_connection = sqlite3.connect(":memory:")
    #mock_connection.cursor.return_value = mock_cursor

    mock_connection = sqlite3.connect(":memory:")
    mock_cursor = mock_connection.cursor()

    mock_cursor.execute('''CREATE TABLE pages (url text, title text, score real, summary_before text, summary_keyword text, summary_after text)''')
    mock_cursor.executemany("INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?)", mock_rows)

    # Patch sqlite3.connect to return the mocked connection
    with patch("app.connect", return_value=mock_connection), \
         patch("app.os.path.isfile", return_value=True):
        response = client.get("/pages.json")
        assert response.status_code == 200
        assert response.json == expected_json


# Tests for the exporting to excel feature!
def test_dump_to_excel_success():
    mock_df = pd.DataFrame({
        "url": ["https://example.com"],
        "title": ["Example"],
        "score": [10],
        "terms": ["keyword"],
        "retrieved": ["2024-01-01"]
    })

    with patch("app.pd.read_sql_query", return_value=mock_df) as mock_read_sql, \
         patch("app.pd.DataFrame.to_excel") as mock_to_excel, \
         patch("app.connect") as mock_connect:
        
        # Set up mocked DB connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        from app import dump_to_excel
        dump_to_excel("mock.db", "mock.xlsx")

        mock_read_sql.assert_called_once()
        mock_to_excel.assert_called_once_with("mock.xlsx", index=False, engine='openpyxl')
        mock_conn.close.assert_called_once()


def test_dump_to_excel_read_sql_exception():
    with patch("app.pd.read_sql_query", side_effect=Exception("read error")) as mock_read_sql, \
         patch("app.connect") as mock_connect:
        
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        from app import dump_to_excel
        dump_to_excel("mock.db", "mock.xlsx")

        mock_read_sql.assert_called_once()
        mock_conn.close.assert_called_once()


def test_dump_to_excel_to_excel_exception():
    mock_df = pd.DataFrame({
        "url": ["https://example.com"],
        "title": ["Example"],
        "score": [10],
        "terms": ["keyword"],
        "retrieved": ["2024-01-01"]
    })

    with patch("app.pd.read_sql_query", return_value=mock_df), \
         patch("app.pd.DataFrame.to_excel", side_effect=Exception("write error")) as mock_to_excel, \
         patch("app.connect") as mock_connect:
        
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        from app import dump_to_excel
        dump_to_excel("mock.db", "mock.xlsx")

        mock_to_excel.assert_called_once()
        mock_conn.close.assert_called_once()
