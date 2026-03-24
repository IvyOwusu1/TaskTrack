from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Home page - view tasks
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")

    if task:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task,))
        conn.commit()
        conn.close()
 
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    
    conn.commit()
    conn.close()
    
    return redirect("/")


@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    updated_task = request.form.get("task")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET title = ? WHERE id = ?",
        (updated_task, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")



if __name__ == "__main__":
    init_db()
    app.run(debug=True)