from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

customers = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        customers.append(f"{name} - {phone}")
    return render_template_string("""
        <h1>Customer Form</h1>
                                  
        <form method="post">
            <input name="name" placeholder="Enter name" required>
            <br><br>                      
            <button type="submit">Save</button>
        </form>

        <h2>Saved Customers</h2>
        {% for c in customers %}
             <p>{{c}}</p>
        {% endfor %}
    """, customers=customers)

if __name__ == "__main__":
    app.run(debug=True)