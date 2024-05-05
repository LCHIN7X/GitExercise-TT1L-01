from flask import redirect,render_template,url_for,request,flash,Blueprint
from auth.models import db
from .models import Faculty,Subject,Book
from .bforms import Addbooks 
from flask_uploads import UploadSet, IMAGES
from flask_login import login_required


views = Blueprint("views",__name__,template_folder="templates",static_folder="static")


@views.route('/home')
@login_required
def home():
    books = Book.query.filter(Book.stock >0)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('home.html', books=books,facultiess=facultiess,subjects=subjects)

@views.route('/book/<int:id>')
def single_page(id):
    book = Book.query.get_or_404(id)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('single_page.html',book=book,facultiess=facultiess,subjects=subjects)

@views.route('/faculty/<int:id>')
def get_faculty(id):
    faculty = Book.query.filter_by(faculty_id=id)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('home.html',faculty=faculty,facultiess=facultiess,subjects=subjects)

@views.route('/subjects/<int:id>')
def get_subject(id):
    get_sub = Book.query.filter_by(subject_id=id)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('home.html',subjects=subjects,get_sub=get_sub,facultiess=facultiess)


@views.route('/addfaculty', methods=['GET','POST'])
@login_required
def addfaculty():
    if request.method == "POST":
        getfaculty = request.form.get('faculty')
        faculty = Faculty(name=getfaculty)
        db.session.add(faculty)
        flash(f'Faculty {getfaculty} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('views.addfaculty'))
    
    return render_template('addfaculty.html', faculties='faculties')




@views.route('/addsub', methods=['GET','POST'])
@login_required
def addsub():
    if request.method =="POST":
        getfaculty = request.form.get('subject')
        sub = Subject(name=getfaculty)
        db.session.add(sub)
        flash(f'Subject {getfaculty} was added to your datebase','success')
        db.session.commit()
        return redirect(url_for('views.addfaculty'))
    
    return render_template('addfaculty.html')

@views.route('/addbook', methods=['POST', 'GET'])
@login_required
def addbook():
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    form=Addbooks(request.form)
    photos = UploadSet('photos', IMAGES)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        desc = form.discription.data
        faculty = request.form.get('faculty')
        subject = request.form.get('subject')
        image = photos.save(request.files['image'])
        addbo = Book(name=name,price=price,stock=stock,desc=desc,faculty_id=faculty,subject_id=subject,image=image)
        db.session.add(addbo)
        db.session.commit()
        flash(f"Book {name} has been added to your database",'success')
        return redirect(url_for('views.addbook'))
    return render_template('addbook.html',title ="Add Book page",form=form,faculties=faculties,subjects=subjects,photos=photos)
