from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

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
