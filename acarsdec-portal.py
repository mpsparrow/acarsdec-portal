from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main():
    conn = sqlite3.connect('acars.db')
    c = conn.cursor()
    c.execute("SELECT * FROM acarsTest ORDER BY date DESC;")
    data = c.fetchall()

    dates = []

    for item in data:
        x = datetime.fromtimestamp(float(item[0]))
        dates.append(x.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

    return render_template("main.html", data=data, dates=dates)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)