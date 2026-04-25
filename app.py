from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"  # you can change this later

FILE = "customers.txt"
PASSWORD = "timmy1234"  # change this to your own password

def load_data():
    try:
        with open(FILE, "r") as f:
            return [line.strip().split("|") for line in f.readlines()]
    except:
        return []

def save_data(data):
    with open(FILE, "w") as f:
        for row in data:
            f.write("|".join(row) + "\n")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        
    return '''
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #f4f6f8;
            font-family: Arial;
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            width: 300px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
            }
    </style>
    <div class="box">
        <h2>Enter Password </h2>
        <form method="post">
            <input type="password" name="password" placeholder="Enter password" required>
            <button>Login</button>
        </form>
    </div>
    '''    

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    
    data = load_data()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        amount = request.form["amount"]

        data.append([name, phone, amount, "Unpaid"])
        save_data(data)

        return redirect("/dashboard")
        
    query = request.args.get("search", "").lower()
    if query:
        data = [d for d in data if query in " ".join(d).lower()]

    return render_template_string("""
    <style>
        body { font-family: Arial; background:#f4f6f8; padding:20px; }
        .box { max-width:500px; margin:auto; background:white; padding:20px; border-radius:10px; }
        input, button { width:100%; padding:10px; margin:5px 0; }
        .item { background:#eee; padding:8px; margin-top:5px; display:flex; justify-content:space-between; }
        a { margin-left:5px; }
    </style> 

    <div class="box">
        <h2>Debt Tracker </h2>
                                  
        <form method="post">
            <input name="name" placeholder="Name" required>
            <input name="phone" placeholder="Phone" required>
            <input name="amount" placeholder=Amount owed" required>
            <button>Add</button>
        </form>      
            
        <form method="get">
            <input name="search" placeholder="Search...">
            <button>Search</button>
        </form>

        <h3>Customers</h3>
                                  
        {% for d in data %}
        <div class="item">
            <span>{{d[0]}} - {{d[2]}} ({{d[3]}})</span>
            <span>
                <a href="/paid/{{loop.index0}}">paid</a>
                <a href="/delete/{{loop.index0}}">delete</a>
            </span>
        </div>
        {% endfor %}
    </div>
    """, data=data)               

@app.route("/paid/<int:i>")
def paid(i):
    data = load_data()
    if 0 <= i <len(data):
        data[i][3] = "paid"
        save_data(data)
    return redirect("/dashboard")

@app.route("/delete/<int:i>")
def delete(i):
    data = load_data()
    if 0 <= i < len(data):
        data.pop(i)
        save_data(data)
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)