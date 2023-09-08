from flask import Flask,render_template,redirect,request,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask('__name__');

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app);
app.app_context().push()
class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    des=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __reper__(self)->str:

        return f"{self.sno} {self.title}" 

@app.route('/',  methods=['GET', 'POST'])
def hello():
    if request.method== 'POST':
        title=(request.form.get('title'))
        des=(request.form.get('des'))
        
        to=Todo(title=title,des=des)
        db.session.add(to)
        db.session.commit()
    alldata=Todo.query.all()
    
    return render_template('index.html',data=alldata)
   
@app.route('/show/')
def product():
    alldata=Todo.query.all()
    return "products"

@app.route('/update/<int:sno>/',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=(request.form.get('title'))
        des=(request.form.get('des'))
        mytodo=Todo.query.filter_by(sno=sno).first()
        mytodo.title=title
        mytodo.des=des
        db.session.add(mytodo)
        db.session.commit()
        return redirect('/')
    mytodo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',data=mytodo)

@app.route('/delete/<int:sno>/',methods=['GET','POST'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'GET':
        if todo:
            db.session.delete(todo)
            db.session.commit()
    return redirect('/')
    
        


if __name__=="__main__":
    app.run(debug=True,)
