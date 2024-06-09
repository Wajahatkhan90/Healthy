from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# MySQL database connection settings
host = "localhost"
user = "root"
password = "qwerty"
database = "forms"

@app.route('/endpoint', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(f"Received data: {data}")  # Enhanced logging

    try:
        # Create a MySQL connection
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()

        # Check if the data already exists
        check_query = """
            SELECT COUNT(*) FROM Appointments 
            WHERE name=%s AND email=%s AND userdate=%s AND department=%s AND phone=%s AND message=%s
        """
        cursor.execute(check_query, (
            data['username'], 
            data['usermail'], 
            data['userdate'], 
            data['department'], 
            data['userphone'], 
            data['msg']
        ))
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert the data into the Appointments table
            insert_query = """
                INSERT INTO Appointments (name, email, userdate, department, phone, message) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['username'], 
                data['usermail'], 
                data['userdate'], 
                data['department'], 
                data['userphone'], 
                data['msg']
            ))
            cnx.commit()

            # Return a success response
            return jsonify({'message': 'Data stored successfully'}), 201
        else:
            # Return a message indicating data already exists
            return jsonify({'message': 'Duplicate data, not stored'}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error storing data'}), 500

    finally:
        if cnx:
            cnx.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
