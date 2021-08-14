from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/")
def blockchain():
    return jsonify(get_data_db())




def get_data_db():
     # create a Blockchain database if not exists
    conection = sqlite3.connect("blockchain.db")
    cursor = conection.cursor()
    

    # TODO: limit select result to start-end block number or limit by #of records

    data = cursor.execute("SELECT * from Blockchain").fetchall()
    conection.close()

    return data