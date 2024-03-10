from flask import Flask, render_template

app = Flask(__name__)

squires = [{
    "name": "Stadium",
    "junctions": "From-Megenagn, From-Agona, From-Mexico, From-Piasa",
    "map_location": "https://maps.app.goo.gl/6UC9EtcyaH6MjEQZA",
    "morning_manager": "Mr. X +251929404324",
    "afternoon_manager": "Mr. Y +251929404325",
    "evening_manager": "Mr. Z +251929404326"
}, {
    "name": "Mexico",
    "junctions": "Junction A, Junction B, Junction C",
    "map_location": "https://maps.app.goo.gl/MpXZLGxuiYP3toyH6",
    "morning_manager": "Mr. A +251929404324",
    "afternoon_manager": "Mr. B +251929404324",
    "evening_manager": "Mr. C +251929404324"
}, {
    "name": "Megenagna",
    "junctions": "Junction X, Junction Y, Junction Z",
    "map_location": "https://maps.app.goo.gl/vKvPeNNkVM8K1CgN7",
    "morning_manager": "Mr. P +251929404324",
    "afternoon_manager": "Mr. Q +251929404324",
    "evening_manager": "Mr. R +251929404324"
}]


@app.route('/')
def home():
    return render_template('home.html', squires=squires)


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
