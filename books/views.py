from flask import redirect,render_template,url_for,request,flash,Blueprint
from . import database as db
from .models import Faculty,Subject
from .bforms import Addbooks 



views = Blueprint("views",__name__)

@views.route("/home")
def home():
    return render_template("base.html")

@views.route('/addfaculty',methods=['GET','POST'])
def addfaculty():
    if request.method =="POST":
        getfaculty = request.form.get('faculty')
        faculty = Faculty(name=getfaculty)
        db.session.add(faculty)
        flash(f'Faculty {getfaculty} was added to your datebase','success')
        db.session.commit()
        return redirect(url_for('views.addfaculty'))
    
    return render_template('books/addfaculty.html',faculties='faculties')

@views.route('/addsub',methods=['GET','POST'])
def addsub():
    if request.method =="POST":
        getfaculty = request.form.get('subject')
        sub = Subject(name=getfaculty)
        db.session.add(sub)
        flash(f'Subject {getfaculty} was added to your datebase','success')
        db.session.commit()
        return redirect(url_for('views.addfaculty'))
    
    return render_template('books/addfaculty.html')

@views.route('/addbook',methods=['POST','GET'])
def addbook():
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    form=Addbooks(request.form)

    if request.method == 'POST' and 'photo' in request.files:
        photos.save(request.files['photo'])
        flash("Photo saved successfully.")
        return render_template('views.addbook.html')
    return render_template('books/addbook.html',title ="Add Book page",form=form,faculties=faculties,subjects=subjects)