from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

@app.route("/")
def home():
    # shows a list of all the to-do items
    todo_list = Todo.query.all()

    # THIS IS HOW WE pass the list of the to-do items to the HTML with the todos=todo_list argument
    return render_template(template_name_or_list="index.html", todos=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # create the item(s) that you are adding
    title = request.form.get("title")
    todo_to_add = Todo(title=title, complete=False)

    # add the item to the database
    db.session.add(todo_to_add)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/update/<int:id>")
def update(id):
    # access the item you want to update
    todo_to_update = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()

    # update the 'complete' status of the item to be the opposite of what is currently is
    todo_to_update.complete = not todo_to_update.complete # can't use the bracket method to access the complete attribute for some reason

    db.session.commit()

    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete(id):
    # access the item you want to delete
    todo_to_delete = db.session.execute(db.select(Todo).where(Todo.id == id)).scalar()

    # delete the item from your database
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # DO THIS ONCE AT FIRST TO CREATE THE DB THEN COMMENT OUT
    # with app.app_context():
        # db.create_all()
        # db.session.commit()
    app.run(debug=True)