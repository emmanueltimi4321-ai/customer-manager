from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"  # you can change this later

FILE = "customers.txt"
PASSWORD = "timmy4812"  # change this to your own password

def load_customers():
    try:
        with open(FILE, "r") as f:
            return f.readlines()
    except:
        return []

def save_all(customers):
    with open(FILE, "w") as f:
        f.writelines(customers)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")

    return render_template_string("""
    <h2>Enter Password </h2>
    <form method="post">
        <input type="password" name="password" placeholder="Enter password" required>
        <button type="submit">Login</button>
    </form>
    """)

@app.route("/dashboard", methods=["GET", "POST"])
def home():
    if not session.get("logged_in"):
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        with open(FILE, "a") as f:
            f.write(f"{name} - {phone}\n")

        return redirect("/dashboard")

    query = request.args.get("search", "").lower()
    customers = load_customers()

    if query:
        customers = [c for c in customers if query in c.lower()]

    return render_template_string("""
    <style>
        body { font-family: Arial; background: #f4f6f8; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        input { width: 100%; padding: 10px; margin: 5px 0; }
        button { padding: 10px; width: 100%; background: #007bff; color: white; border: none; }
        .customer { display: flex; justify-content: space-between; background: #eee; padding: 8px; margin-top: 5px; border-radius: 5px; }
        a { color: red; text-decoration: none; }
    </style>

    <div class="container">
        <h2>Customer Manager </h2>

        <form method="post">
            <input name="name" placeholder="Enter name" required>
            <input name="phone" placeholder="Enter phone" required>
            <button type="submit">Add Customer</button>
        </form>

        <br>

        <form method="get">
            <input name="search" placeholder="Search customer...">
            <button type="submit">Search</button>
        </form>

        <h3>Customers</h3>

        {% for c in customers %}
            <div class="customer">
                <span>{{c}}</span>
                <a href="/delete/{{loop.index0}}">Delete</a>
            </div>
        {% endfor %}
    </div>
    """, customers=customers)

@app.route("/delete/<int:index>")
def delete(index):
    if not session.get("logged_in"):
        return redirect("/")

    customers = load_customers()

    if 0 <= index < len(customers):
        customers.pop(index)
        save_all(customers)

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)