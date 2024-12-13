# Flask-Banking-Application

This is a simple banking application built with **Flask** and **SQLite**. The application allows users to input their financial data, predict the likelihood of defaulting on a loan, and store this information in a SQLite database. It also includes a web interface to view and manage stored data, along with data analysis capabilities using **SparkSQL**.

## Features

- Predict whether a user will default on a loan based on their financial information.
- Store user input data and prediction results in a SQLite database.
- View and analyze stored data through a web interface.
- Error handling for invalid input data.
- Data analysis with SparkSQL for deeper insights into the stored data.

## Requirements

- Python
- Flask
- scikit-learn (for machine learning model)
- SQLite
- PySpark (for SparkSQL analysis)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NguyenPhuongDng/Flask-Banking-Application.git
2. Run `bank_app.py`
3. Access the link : http://127.0.0.1:5000 to enter application web interface
