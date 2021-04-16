from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'damascusXIII'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<user_id>')
def user(user_id):
    data = {
        'user_id': user_id
    }
    newuser_db = connectToMySQL('dojo_survey').query_db('SELECT * FROM dojos WHERE id=%(user_id)s;',data)
    return render_template('user.html', newuser_tp=newuser_db)

@app.route('/user/create', methods=['POST'])
def create_user():
    print(request.form)
    is_valid = True
    if len(request.form['firstname']) < 1:
        is_valid = False
        flash('Please enter a first name')
    if len(request.form['lastname']) < 1:
        is_valid = False
        flash('Please enter a last name')
    if request.form['location'] == 'Choose...':
        is_valid = False
        flash('Please choose a location')
    if request.form['favorite'] == 'Choose...':
        is_valid = False
        flash('Please choose a favorite language')
    if 'gender' not in request.form:
        is_valid = False
        flash('Please select a gender')
    if 'race' not in request.form:
        is_valid = False
        flash('Please select a race')
    
    if not is_valid:
        return redirect('/', )
    else:
        query = 'INSERT INTO dojos(first_name,last_name,race_ethnicity,gender,location,language,comment) VALUES(%(f_name)s,%(l_name)s,%(race)s,%(gender)s,%(location)s,%(language)s,%(comment)s);'
        data = {
            'f_name': request.form['firstname'],
            'l_name': request.form['lastname'],
            'race': request.form['race'],
            'gender': request.form['gender'],
            'location': request.form['location'],
            'language': request.form['favorite'],
            'comment': request.form['comment']
        }
        connectToMySQL('dojo_survey').query_db(query,data)
        user_id = connectToMySQL('dojo_survey').query_db('SELECT id FROM dojos;')
        return redirect('/user/'+str(user_id))

if __name__ == '__main__':
    app.run(debug=True)