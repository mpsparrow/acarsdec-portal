import socket
import sqlite3
import json


def createTable():
    # connect to sqlite table
    conn = sqlite3.connect('acars.db')
    c = conn.cursor()

    # create db table
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS acarsTest (
                    date text, station_id text, ip_address text, port integer, channel integer, freq text, level integer,
                    error integer, mode integer, label text, block_id integer, ack text, tail text, 
                    flight text, msgno text, msg text)''')
        print("table created")
    except:
        pass
    finally:
        conn.close()

def saveData(data, address):
    # connect to sqlite table
    conn = sqlite3.connect('acars.db')
    c = conn.cursor()

    x = json.loads(data.decode("utf-8"))

    # some data cleaning
    try:
        if not(bool(x["ack"])):
            x["ack"] = ""
    except:
        pass

    try:
        text = x["text"]
    except:
        text = ""

    table = """INSERT INTO acarsTest (date, station_id, ip_address, port, channel, freq, level,
                error, mode, label, block_id, ack, tail, flight, msgno, msg) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    dataTuple = (x['timestamp'], x['station_id'], address[0], address[1], x['channel'], 
                x['freq'], x['level'], x['error'], x['mode'], x['label'], x['block_id'], 
                x['ack'], x['tail'], x['flight'], x['msgno'], text)

    # insert data into the db
    c.execute(table, dataTuple)

    conn.commit()
    conn.close()


# set up our receiving socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("192.168.1.95", 12345))

createTable()

# main receiving loop
while True:
    # receive the data and decode it
    data, address = udp_socket.recvfrom(512)
    print("Received %s from %s:%d" %(data, address[0], address[1]))
    saveData(data, address)