import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
connection = sqlite3.connect('manaject.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, project_name TEXT, description TEXT, worker_name TEXT, worker_email TEXT, start_date DATE, due_date DATE, FOREIGN KEY (worker_name) REFERENCES users(username))')
cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, from_worker_name TEXT, message TEXT, worker_to_send TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (worker_to_send) REFERENCES users(username))')
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')


def insert_user(username, password):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()  
        cursor.close()
        status = "OK"
        logging.info("Insertion to DB succeeded")
    except Exception as e:  
        logging.error("Error inserting to DB: %s", e)
        status = "ERROR"

    return status


def get_user_by_name(username):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        cursor.close()
        logging.info("Fetch from DB succeeded")
        return user
    except Exception as e:
        logging.error("Error fetching from DB: %s", e)
        return None
    

def get_all_projects():
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        cursor.close()
        logging.info("Fetch from DB succeeded")
    except:
        logging.error("Error fetching from DB")
        projects = []

    return projects


def get_projects_by_worker(worker_name):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM projects WHERE worker_name = ?', (worker_name,))
        projects = cursor.fetchall()
        cursor.close()
        logging.info("Fetch from DB succeeded")
    except Exception as e:
        logging.error("Error fetching from DB: %s", e)
        projects = []

    return projects


def get_project_details(worker_name, project_name):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM projects WHERE worker_name = ? AND project_name = ?', (worker_name, project_name))
        num_projects = cursor.rowcount 
        project = cursor.fetchone()
        cursor.close()

        if num_projects == 0:
            status = "NOT FOUND"  
        else:
            status = "OK" 
            logging.info("Fetch from DB succeeded")
    except Exception as e:
        logging.error("Error fetching from DB: %s", e)
        project = None

    return status, project


def create_project(project_name, project_description, worker_name, worker_email, start_date, due_date):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO projects (project_name, description, worker_name, worker_email, start_date, due_date) VALUES (?, ?, ?, ?, ?, ?)', (project_name, project_description, worker_name, worker_email, start_date, due_date))

        connection.commit()
        cursor.close()
        status = "OK"
        logging.info("Insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def delete_project(worker_name, project_name):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM projects WHERE worker_name = ? AND project_name = ?', (worker_name, project_name))
        num_deleted = cursor.rowcount  
        connection.commit()
        cursor.close()
        
        if num_deleted == 0:
            status = "NOT FOUND"  
        else:
            status = "OK" 
            logging.info("Deletion from DB succeeded")
    except Exception as e:
        logging.error("Error deleting from DB: %s", e)
        status = "ERROR"

    return status


def update_project(project_id, project_name, project_description, worker_name, worker_email, start_date, due_date):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE projects SET project_name = ?, description = ?, worker_name = ?, worker_email = ?, start_date = ?, due_date = ? WHERE id = ?', (project_name, project_description, worker_name, worker_email, start_date, due_date, project_id))
        connection.commit()
        cursor.close()
        status = "OK"
        logging.info("Update in DB succeeded")
    except Exception as e:
        logging.error("Error updating in DB: %s", e)
        status = "ERROR"

    return status


def insert_massage(from_worker_name, message, worker_to_send, current_timestamp):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO messages (from_worker_name, message, worker_to_send, timestamp) VALUES (?, ?, ?, ?)', (from_worker_name, message, worker_to_send, current_timestamp))
        connection.commit()
        cursor.close()
        status = "OK"
        logging.info("Insertion to DB succeeded")
    except:
        logging.error("Error inserting to DB")
        status = "ERROR"

    return status


def get_messages_by_worker(worker_name):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM messages WHERE worker_to_send = ?', (worker_name,))
        messages = cursor.fetchall()
        cursor.close()
        logging.info("Fetch from DB succeeded")
    except Exception as e:
        logging.error("Error fetching from DB: %s", e)
        messages = []

    return messages


def delete_message(worker_name, message_id):
    try:
        connection = sqlite3.connect('manaject.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM messages WHERE id = ? AND worker_to_send = ?', (message_id, worker_name))
        num_deleted = cursor.rowcount
        connection.commit()
        cursor.close()
        if num_deleted == 0:
            status = "NOT FOUND"  
        else:
            status = "OK" 
            logging.info("Deletion from DB succeeded")
    except Exception as e:
        logging.error("Error deleting from DB: %s", e)
        status = "ERROR"

    return status

    



