from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:root@127.0.0.1:8889/FlaskDB'

db=SQLAlchemy(app)
# a
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        taskContent=request.form['content']
        newTask=Todo(content=taskContent)

        try :
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is issue'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    deleteTask=Todo.query.get_or_404(id)

    try:
        db.session.delete(deleteTask)
        db.session. commit()
        return redirect('/')
    except:
        return deleteTask.content

@app.route('/update/<int:id>',methods=['GET','POST'])
def  update(id):
    task = Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There is the issue'
    else:
        return render_template('update.html',task=task)



if __name__=="__main__":
    app.run(debug=True)
