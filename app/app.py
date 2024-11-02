from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'user'),
    'password': os.getenv('MYSQL_PASSWORD', 'secret'),
    'database': os.getenv('MYSQL_DB', 'form_db')
}

# Connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route to display the form and the data
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        # Insert data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

    # Retrieve all entries
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("form.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

