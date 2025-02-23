from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.app_context().push()

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created= db.Column(db.DateTime, default=datetime.now)

    """ def test_connection(self):
        with app.app_context():
            pass """

    def __repr__(self) -> str:
        return '<Task %r>' % self.id

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST" :
        task_content = request.form['content'] #Contient le id de l'entrée qu'on souhaite récupérer
        new_task = ToDo(content=task_content)
        print(new_task)

        try :
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue to your task"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    
    except:
        return "The was a problem deleting the Task"
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = ToDo.query.get_or_404(id)

    if request.method=="POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Something went wrong"

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)