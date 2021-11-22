from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('takenote.html')

@app.route("/",methods=['POST'])
def takenote():
    global name
    name = request.form['Name']
    global desc 
    desc = request.form['Description']
    return redirect(url_for('listnotes'))
@app.route('/list-notes')
def listnotes():
    # print the result
    print('\nNotes:')
    #
    # Querying the database
    #

    # query the database for ALL data in the notes table
    with sqlite3.connect("database.db") as con:
        cur.execute('SELECT * FROM notes;')

    html = ''
    notes = {}
    for row in cur.fetchall():
        display_name = row[1]
        display_desc = row[2]
        notes[display_name] = display_desc
        
    #
    # Cleaning up
    #
    
    return render_template('notes.html',name=name,desc=desc,notes=notes)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=False)