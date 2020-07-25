import json
from flask import json, Flask, render_template
import sqlite3

app = Flask(__name__)

def write_json(data, filename='data.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

@app.route('/')
def main():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)