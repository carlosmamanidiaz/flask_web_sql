from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL


app = Flask(__name__)


mysql = MySQL(app, host="localhost", user="admin",password="password",db="flaskcontacts",autocommit=True) 


app.secret_key = 'mysecretkey'
@app.route('/')
def Index():
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    # print(data)
    return render_template("index.html", contacts = data)



@app.route('/add_contact', methods = ['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.get_db().cursor()
        cur.execute('INSERT INTO contacts(fullname,phone,email) VALUES (%s,%s,%s)', (fullname,phone,email))

        flash('Contact Added Successfuly')
        return redirect(url_for('Index'))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id = {id}')
    data = cur.fetchall()[0]
    return render_template("edit-contact.html", contact = data)

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method =="POST":
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.get_db().cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
    flash ('Actualizado Satisfatoriamente')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    print(id)
    cur = mysql.get_db().cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id}')
    flash('Contact Removed Successfuly')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
