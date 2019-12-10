import requests as req
import sqlite3 as db
import json
from flask import Flask, request, redirect, jsonify
from flask import render_template

url = 'http://localhost:5000/sudoku'

colored_board = []

def check_db_exists():
    database = db.connect('board.db')
    with database:
        cur = database.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='board';")
        if len(cur.fetchall()):
            return True
        return False

def load_data():
    if check_db_exists():
        database = db.connect('board.db')
        with database:
            cur = database.cursor()
            cur.execute("SELECT * FROM board")
            new_board = cur.fetchall()
            return [list(elem) for elem in new_board]
    else:
        r = req.get(url)
        print('Content-Type: ', r.headers['content-type'])
        print(r.json())
        board = [a for b in r.json() for a in b]
        board = [a if a != 0 else '' for a in board]
        return [[i, 'black'] for i in board]

def get_index(cell):
    return(cell//9, cell % 9)

def check_cells():
    for i, cell in enumerate(colored_board):
        if cell[1] != 'black':
            if check_new_cell(i, cell[0]):
                colored_board[i][1] = 'green'
            else:
                colored_board[i][1] = 'red'

def check_new_cell(cell, value):
    for i in range(cell, 81, 9):
        if i == cell:
            continue
        if colored_board[i][0] == value:
            return False
    for i in range(cell - cell % 9, cell + (9 - cell % 9)):
        if i == cell:
            continue
        if colored_board[i][0] == value:
            return False
    for i in range(81):
        if i == cell:
            continue
        cell_index = get_index(cell)
        index = get_index(i)
        if cell_index[0] // 3 == index[0] // 3 and cell_index[1] // 3 == index[1] // 3:
            if colored_board[i][0] == value:
                return False
    return True



app = Flask(__name__)

@app.route('/')
def home_dir():
    load_status = ''
    if check_db_exists():
        load_status = 'Loaded from Database'
    else:
        load_status = 'Fetched from Server'
    return render_template('sudoku.html', load_status=load_status)

@app.route('/submit', methods=['POST'])
def submit():
    cell = int(request.form['cell'])
    value = int(request.form['value'])
    if check_new_cell(cell, value):
        color = 'green'
    else:
        color = 'red'
    colored_board[cell][0] = value
    colored_board[cell][1] = color
    check_cells()
    return 'OK'

@app.route('/getBoard', methods=['GET'])
def give_board():
    return jsonify(board=colored_board)

@app.route('/remove', methods=['POST'])
def remove_cell():
    cell = int(request.form['cell'])
    colored_board[cell][0] = ''
    colored_board[cell][1] = 'black'
    check_cells()
    return 'OK'

@app.route('/save', methods=['POST'])
def save_to_database():
    database = db.connect('board.db')
    with database:
        cur = database.cursor()
        cur.execute("DROP TABLE IF EXISTS board")
        cur.execute("CREATE TABLE board(value INT, color TEXT)")
        cur.executemany("INSERT INTO board VALUES(?,?)", colored_board)
    return 'OK'


if __name__ == '__main__':
    colored_board = load_data()
    app.run(port=5001)
