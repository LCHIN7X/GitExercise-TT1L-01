from flask import redirect,render_template,url_for,request,flash
from app import db,create_app 
from .models import Faculty,Subject



@create_app.route('/addfaculty',methods=['GET','POST'])
def addfaculty():
    if request.method =="POST":
        getfaculty = request.form.get('faculty')
        faculty = Faculty(name=getfaculty)
        db.session.add(faculty)
        flash(f'Faculty {getfaculty} was added to your datebase')
        db.session.commit()
        return redirect(url_for('addfaculty'))
    
    return render_template('books/addfaculty.html',faculties='faculties')





@create_app.route('/addsub',methods=['GET','POST'])
def addsub():
    if request.method =="POST":
        getsubject = request.form.get('subject')
        sub = Subject(name=getsubject)
        db.session.add(sub)
        flash(f'Subject {getsubject} was added to your datebase')
        db.session.commit()
        return redirect(url_for('addsub'))
    
    return render_template('books/addfaculty.html',faculties='faculties')