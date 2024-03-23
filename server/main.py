from flask import Flask, request, render_template, flash, session, redirect
import db
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/',methods=['GET', 'POST'])
def home():  
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username = username)
    
    return render_template('index.html')
    

@app.route('/myprojects',methods=['GET'])
def display_my_project():
    worker_name = session['username']
    projects= db.get_projects_by_worker(worker_name)
    return render_template('myprojects.html',projects=projects, worker_name=worker_name) 


@app.route('/myprojects',methods=['POST'])
def delete_project():
    worker_name = session['username']
    project_name = request.form['project_name']
    status = db.delete_project(worker_name, project_name) 
    if status == "OK":
        flash('Project deleted successfully!', 'success')
        return redirect('myprojects')
    else:
        flash('Error! worker name or project name not exist!', 'error')
        return redirect('myprojects')

    

@app.route('/login',methods=['POST'])
def login():
    if 'loginUsername' in request.form and 'loginPassword' in request.form:
        login_username = request.form['loginUsername']
        login_password = request.form['loginPassword']
        user = db.get_user_by_name(login_username)
        print(check_password_hash(login_password, user[2]))
        if (user is not None) and (check_password_hash(user[2], login_password)):
            flash('User logged in successfully!', 'success')
            session['username'] = login_username
            return render_template('index.html', username=login_username)
        else:
            flash('Username or password is incorrect! Try again', 'error')
            return render_template('auth.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if 'signupUsername' in request.form and 'signupPassword' in request.form:
        signup_username = request.form['signupUsername']
        signup_password = request.form['signupPassword']
        user = db.get_user_by_name(signup_username)
        if user is None:
            hashed_password = generate_password_hash(signup_password)
            db.insert_user(signup_username, hashed_password)
            flash('User created successfully! Please login', 'success')
            return render_template('auth.html')
        else:
            flash('Username already exists! Try another Username', 'error')
            return render_template('auth.html')


@app.route('/auth',methods=['GET'])
def auth():
    return render_template('auth.html')


@app.route('/logout',methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/projects', methods=['GET', 'POST']) 
def projects():
    projects= db.get_all_projects()
    return render_template('projects.html',projects=projects) 


def check_due_date(due_date):
    current_date = datetime.now().date()
    if current_date > due_date:
        return True
    else:
        return False
    
@app.route('/createproject',methods=['GET'])
def desplay_create_project():
    return render_template('createproject.html')

@app.route('/createproject',methods=[ 'POST'])
def create_project():
    project_name = request.form['project_name']
    project_description = request.form["project_description"]
    worker_name = session['username']
    worker_email = request.form['worker_email']
    start_date = datetime.now().date()
    due_date_str = request.form['due_date']
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() 
    if check_due_date(due_date):
        flash('Error! due date is expired!', 'error')
        return render_template('createproject.html', project_name=project_name, project_description=project_description, worker_email=worker_email)

    db.create_project(project_name, project_description, worker_name, worker_email, start_date, due_date)
    flash('Project add successfully!', 'success')
    projects= db.get_all_projects()
    return render_template('projects.html',projects=projects)


@app.route('/update_project/<project_name>', methods=['GET'])
def desplay_update_project(project_name):
    worker_name = session['username']
    status, project_details = db.get_project_details(worker_name, project_name) 
    if project_details is not None and status == "OK":
        return render_template('project_details.html', project_details=project_details)


@app.route('/update_project/<project_name>', methods=['POST'])
def update_project(project_name):
    worker_name = session['username']
    project_name = request.form['project_name']
    project_description = request.form["project_description"]
    worker_name = session['username']
    worker_email = request.form['worker_email']
    start_date = request.form['start_date']
    due_date = request.form['due_date']
    db.create_project(project_name, project_description, worker_name, worker_email, start_date, due_date)
    flash('Project updated successfully!', 'success')
    projects= db.get_projects_by_worker(worker_name)

    return render_template('myprojects.html',projects=projects, worker_name=worker_name) 


@app.route('/messages', methods=['GET'])
def desplay_messages():
    worker_name = session['username']
    messages= db.get_messages_by_worker(worker_name)    
    return render_template('messages.html',messages=messages, worker_name=worker_name)

        
@app.route('/messages', methods=['POST'])
def send_messages():
    worker_name = session['username']
    messages= db.get_messages_by_worker(worker_name)
    worker_to_send = request.form['worker_to_send']
    if db.get_user_by_name(worker_to_send) is not None:
        message = request.form['message']
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.insert_massage(worker_name, message, worker_to_send, current_timestamp)
        flash('Massage sent successfully!', 'success')
        return render_template('messages.html', messages=messages, worker_name=worker_name)
    else:
        flash('Error! worker name not exist!', 'error')
        return render_template('messages.html', messages=messages, worker_name=worker_name)

    
@app.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    worker_name = session['username']
    status = db.delete_message(worker_name, message_id)
    if status == "OK":
        flash('Message deleted successfully!', 'success')
        messages= db.get_messages_by_worker(worker_name)
        return render_template('messages.html',messages=messages, worker_name=worker_name)
    else:
        flash('Error! could not delete message!', 'error')
        messages= db.get_messages_by_worker(worker_name)
        return render_template('messages.html',messages=messages, worker_name=worker_name)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

