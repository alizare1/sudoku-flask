# Sudoku-flask

This project was created for University of Tehran Summer of Code qualification. an API was provided for loading a sudoku table.
Aim of the project is to load the table using the API and show it using web page.
This app uses 'flask' and 'requests' to fetch the table, load template, speak to the client and verify the inputs.
'sqlite3' was used as database for saving user inputs for the future runs.

## How to run

Soduko API must be running on http://localhost:5000. (board.db is present, so app runs fine even without the API.)

this code uses 'flask' and 'requests' library. run the app by:
```bash
python3 app.py
```
open http://localhost:5001.


