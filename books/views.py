from flask import redirect,render_template,url_for,request,flash,Blueprint,session
from auth.models import db,User
from .models import Faculty,Subject,Book
from .bforms import Addbooks 
from .invoice import Invoice
from flask_uploads import UploadSet, IMAGES
from flask_login import login_required,current_user


views = Blueprint("views",__name__,template_folder="templates",static_folder="static")


@views.route('/home')
@login_required
def home():
    books = Book.query.filter(Book.stock >0)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('home.html', books=books,facultiess=facultiess,subjects=subjects)

@views.route('/searchh')
def searchh():
    searchword = request.args.get('x')
    books = Book.query.msearch(searchword,fields=['name','desc'],limit=3)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('searchh.html',books=books,facultiess=facultiess,subjects=subjects)

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
    users = User.query.all()
    form=Addbooks(request.form)
    photos = UploadSet('photos', IMAGES)
    if request.method == 'POST':
        name = form.name.data
        username = request.form.get("username")
        price = form.price.data
        stock = form.stock.data
        desc = form.discription.data
        faculty = request.form.get('faculty')
        subject = request.form.get('subject')
        image = photos.save(request.files['image'])
        user = current_user
        addbo = Book(name=name,user_id=username,price=price,stock=stock,desc=desc,faculty_id=faculty,subject_id=subject,image=image,user=user)
        db.session.add(addbo)
        db.session.commit()
        flash(f"Book {name} has been added to your database",'success')
        return redirect(url_for('views.addbook'))
    return render_template('addbook.html',title ="Add Book page",form=form,faculties=faculties,subjects=subjects,photos=photos,users=users)


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@views.route('/addcart', methods=['POST'])
def addcart():
    try:
        book_id = request.form.get('book_id')
        quantity = request.form.get('quantity')
        book = Book.query.filter_by(id=book_id).first()
        if book_id and quantity and request.method == "POST":
            DictItems = {book_id:{'name': book.name, "price": book.price, "quantity": quantity, 'image': book.image}}

            if 'Shopcart' in session:
                print(session['Shopcart'])
                if book_id in session['Shopcart']:
                   print("Book is aalready in your cart")
                else:
                    session['Shopcart'] = MagerDicts(session['Shopcart'],DictItems)
                    return redirect(request.referrer)
            else:
                session['Shopcart'] = DictItems
                return redirect(request.referrer)

            return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@views.route('/carts')
def getCart():
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    if 'Shopcart' not in session:
        return redirect(request.referrer)
    total = 0
    for key, book in session['Shopcart'].items():
        total += float(book['price']) * int(book['quantity'])  
    return render_template('carts.html', total=total,facultiess=facultiess,subjects=subjects)


@views.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shopcart' not in session or len(session['Shopcart']) <= 0:
        return redirect(url_for('views.home'))

    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, book in session['Shopcart'].items():
                if int(key) == code:
                    book['quantity'] = quantity 
                    flash('Updated')
                    return redirect(url_for('views.getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('views.getCart'))


@views.route('/deletebook/<int:id>')
def deletebook(id):
    if 'Shopcart' not in session and len(session['Shopcart']):
        return redirect(url_for('views.home'))
    try:
        session.modified = True
        for key, book in session['Shopcart'].items():
                if int(key) == id:
                    session['Shopcart'].pop(key,None)
                    return redirect(url_for('views.getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('views.getCart'))
    
@views.route('/confirm')
def confirm():
    return render_template('confirm.html')
    
@views.route('/payment')
def payment():
    return render_template('payment.html')


@views.route('/order')
def order():
    if 'Shopcart' not in session or not session['Shopcart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('views.getCart'))

    order_details = session['Shopcart']
    total = 0 
    user = current_user  
    invoices = Invoice.query.all() 
    invoice_id = None  # Initialize invoice_id here

    try:
        # Create a new invoice
        new_invoice = Invoice()
        db.session.add(new_invoice)
        db.session.commit()

        # Add invoice ID to the order details
        invoice_id = new_invoice.id
        for book_id, item in order_details.items():
            item['invoice_id'] = invoice_id
            book = Book.query.get(book_id)
            if book:
                quantity_to_deduct = int(item['quantity'])
                if book.stock >= quantity_to_deduct:
                    book.stock -= quantity_to_deduct
                    total += float(item['price']) * quantity_to_deduct  
                else:
                    flash(f'Insufficient stock for {book.name}. Please remove it from your cart.', 'warning')
                    return redirect(url_for('views.getCart'))
        db.session.commit()
        flash('Checkout successful. Your order has been placed.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during checkout. Please try again later.', 'error')
        print(e)

    session.pop('Shopcart', None)  

    return render_template('order.html', order_details=order_details, total=total, user=user, invoice_id=invoice_id)












   




