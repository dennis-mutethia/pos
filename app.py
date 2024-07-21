from flask import Flask, render_template, request, redirect, url_for, current_app, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
import sqlite3, secrets, hashlib

app = Flask(__name__)
secret_key = secrets.token_hex()
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
app.app_context().push()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Website:
    def __init__(self, id, user_id, name, url):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.url = url

def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = {}'.format(int(user_id)))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

def get_user_by_username(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None
    
def save_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO users(username, password) VALUES(?, ?)', (username, password))
    conn.commit()
    conn.close()  
    
def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()
    
def authenticate_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

def save_website(name, url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO websites(user_id, name, url) VALUES(?, ?, ?)', (current_user.id, url, name))
    conn.commit()
    conn.close()  

def get_user_website_by_name_url(name, url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM websites WHERE user_id = ? AND (name = ? OR url = ?)", (current_user.id, name, url))
    website_data = cursor.fetchone()
    conn.close()
    if website_data:
        return Website(website_data[0], website_data[1], website_data[2], website_data[3])
    else:
        return None

def get_user_websites():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM websites WHERE user_id = ?", (current_user.id,))
    websites_data = cursor.fetchall()
    conn.close()
    user_websites = []
    for website_data in websites_data:
        user_websites.append(Website(website_data[0], website_data[1], website_data[2], website_data[3]))
        
    return user_websites 

def delete_website(website_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM websites WHERE id = ?', (website_id,))
    conn.commit()
    conn.close()  
                    
# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    # TODO 1: Implement the user registration.

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            hashed_password = hash_password(password)
            
            if get_user_by_username(username) is None: 
                save_user(username, hashed_password)               
                flash('Registration Successful! Proceed to Login', 'success')
                return redirect(url_for('login'))
            else: 
                flash('Registration failed! Username already exists.', 'danger') 
                
        else: 
            flash('Registration failed! Passwords do not match.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # TODO 2: Implement the user login.

    error = None
    if request.method == 'POST':       
        username = request.form['username']
        password = request.form['password']        
        hashed_password = hash_password(password)
        user = authenticate_user(username, hashed_password)
        
        if user: 
            login_user(user)
            return redirect(url_for('dashboard'))
        else: 
            error = 'Login failed! Username & Password do not match or Username does not exist.'

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    # TODO 3: Implement the function for adding websites to user profiles.    
    
    if request.method == 'POST':       
        website_name = request.form['website_name']
        website_url = request.form['website_url']  
        
        if get_user_website_by_name_url(website_name, website_url) is None: 
            save_website(website_name, website_url)             
            flash('Website Added Successful!', 'success')
        else: 
            flash('Adding Website failed! Website already exists.', 'danger') 

    user_websites = get_user_websites() 
    
    return render_template('dashboard.html', websites=user_websites)

@app.route('/dashboard/<int:website_id>/delete', methods=['POST'])
@login_required
def delete(website_id):

    # TODO 4: Implement the function for deleting websites from user profiles.
    
    delete_website(website_id)
    return redirect(url_for("dashboard"))

def create_tables():
    # Creates new tables in the database.db database if they do not already exist.
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    with current_app.open_resource("schema.sql") as f:
        c.executescript(f.read().decode("utf8"))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
