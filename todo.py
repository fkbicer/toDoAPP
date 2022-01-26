from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/fkbic/OneDrive/Desktop/ToDoAPP/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all() # Todo' column'larimizin özellikleri, sözlük seklinde liste halinde return oluyor.
                             #For döngüsü kullanarak sözlük üzerinde hareket etmeye calisacagiz.
    return render_template("index.html", todos =todos)
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo= Todo.query.filter_by(id = id).first() #complete butonuna bastigimizda True ise False, False ise True yapacagız.
                                                #filter_by method'u ile biz istedigimiz id'li objeyi seciyoruz.
    if todo.complete == True:
        todo.complete=False
    else:
        todo.complete=True
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id =id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/add", methods =["POST"])
def addTodo():
    title= request.form.get("title") # name'i title olan degeri alıyoruz.
    newTodo = Todo(title = title ,complete = False) #todo class'indan bir tane obje olusturduk.
    db.session.add(newTodo) # degeri ekledik
    db.session.commit() # ekledigimizi commit ettik.

    return redirect(url_for("index"))
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)