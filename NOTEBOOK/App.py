from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('notes.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)''')

@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    note = request.form['note']
    if note:
        with sqlite3.connect('notes.db') as conn:
            conn.execute('INSERT INTO notes (content) VALUES (?)', (note,))
    return redirect('/')

@app.route('/delete/<int:note_id>')
def delete(note_id):
    with sqlite3.connect('notes.db') as conn:
        conn.execute('DELETE FROM notes WHERE id=?', (note_id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
