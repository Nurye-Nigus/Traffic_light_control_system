from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nurye@68793'
app.config['MYSQL_DB'] = 'traffic_light'
mysql = MySQL(app)

# Route to handle form submission
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    try:
        # Get form data
        name = request.form['name']
        phone = request.form['phone']
        description = request.form['description']
        
        # Connect to MySQL and insert data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comment (Name, Phone, Description) VALUES (%s, %s, %s)", (name, phone, description))
        mysql.connection.commit()
        cur.close()

        # Fetch and return updated comments
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM comment")
        comments = cur.fetchall()
        cur.close()

        return jsonify({'message': 'Comment submitted successfully', 'comments': comments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to fetch and display squires
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM squires")
    squires_data = cur.fetchall()
    cur.close()
    return render_template('home.html', squires=squires_data)

# Other routes...

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')

if __name__ == '__main__':
    app.run(debug=True)
