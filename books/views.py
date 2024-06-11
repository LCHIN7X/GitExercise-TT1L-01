from flask import redirect, render_template, url_for, request, flash, Blueprint, session
from auth.models import db, User
from .models import Faculty, Subject,Book,  Stock, BannedBook
from .invoice import Invoice,InvoiceItem,Rating
from .bforms import Addbooks
from .forms import RatingForm 
from flask_uploads import UploadSet, IMAGES
from flask_login import login_required,current_user

import secrets,traceback


views = Blueprint("views",__name__,template_folder="templates",static_folder="static")


@views.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 12  

    books_query = Book.query.filter(Book.stock > 0, Book.is_original == True)
    pagination = books_query.paginate(page=page, per_page=per_page, error_out=False)
    
    books = pagination.items
    bookss = Book.query.filter(Book.stock > 0, Book.is_original == False).all()

    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()

    average_rating = {}
    for book in books:
        ratings = [rating.rating for rating in book.book_ratings]
        average_rating[book.id] = sum(ratings) / len(ratings) if ratings else 0
        
    
    average_ratingsh = {}
    for sbook in bookss:
        ratings = [rating.rating for rating in sbook.book_ratings]
        average_ratingsh[sbook.id] = sum(ratings) / len(ratings) if ratings else 0
        
    return render_template('home.html', books=books, bookss=bookss, facultiess=facultiess,subjects=subjects, pagination=pagination, average_rating=average_rating,average_ratingsh=average_ratingsh)


@views.route('/searchh')
def searchh():
    searchword = request.args.get('x')
    books = Book.query.msearch(searchword, fields=['name', 'desc']).filter(Book.stock > 0, Book.is_original == True).limit(3).all()

    if books:
        bookss = Book.query.filter_by(name=books[0].name).filter(Book.stock > 0, Book.is_original == False).all()
    else:
        bookss = []

   
    facultiess = Faculty.query.join(Book, (Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book, (Subject.id == Book.subject_id)).all()

    average_rating = {}
    for book in books:
        ratings = [rating.rating for rating in book.book_ratings]
        average_rating[book.id] = sum(ratings) / len(ratings) if ratings else 0

    average_ratingsh = {}
    for sbook in bookss:
        ratings = [rating.rating for rating in sbook.book_ratings]
        average_ratingsh[sbook.id] = sum(ratings) / len(ratings) if ratings else 0
    
    return render_template('searchh.html', books=books, bookss=bookss, facultiess=facultiess, subjects=subjects,average_rating=average_rating,average_ratingsh=average_ratingsh)




@views.route('/book/<int:id>')
@login_required
def single_page(id):
    book = Book.query.get_or_404(id)   
    bookss = Book.query.filter_by(name=book.name).filter(Book.stock > 0, Book.is_original == False).all()
    facultiess = Faculty.query.all()
    subjects = Subject.query.all()
    
    
    ratings = [rating.rating for rating in book.ratings]
    average_rating = sum(ratings) / len(ratings) if ratings else 0

    average_ratingsh = {}
    for sbook in bookss:
        ratings = [rating.rating for rating in sbook.book_ratings]
        average_ratingsh[sbook.id] = sum(ratings) / len(ratings) if ratings else 0
    
    return render_template('single_page.html', book=book, bookss=bookss, facultiess=facultiess, subjects=subjects,average_rating=average_rating,average_ratingsh=average_ratingsh)



@views.route('/faculty/<int:id>')
@login_required
def get_faculty(id):
    page = request.args.get('page', 1, type=int)
    per_page = 12 

    books_query = Book.query.filter_by(faculty_id=id).filter(Book.stock > 0, Book.is_original == True)
    pagination = books_query.paginate(page=page, per_page=per_page, error_out=False)
    get_faculty = pagination.items
    
    additional_books = Book.query.filter_by(faculty_id=id).filter(Book.stock > 0, Book.is_original == False).all()
    facultiess = Faculty.query.join(Book, (Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book, (Subject.id == Book.subject_id)).all()

    average_rating = {}
    for book in get_faculty:
        ratings = [rating.rating for rating in book.book_ratings]
        average_rating[book.id] = sum(ratings) / len(ratings) if ratings else 0

    average_ratingsh = {}
    for sbook in additional_books:
        ratings = [rating.rating for rating in sbook.book_ratings]
        average_ratingsh[sbook.id] = sum(ratings) / len(ratings) if ratings else 0

    return render_template('home.html', books=get_faculty, bookss=additional_books, facultiess=facultiess, subjects=subjects, pagination=pagination,average_rating=average_rating,average_ratingsh=average_ratingsh)


@views.route('/subjects/<int:id>')
def get_subject(id):
    page = request.args.get('page', 1, type=int)
    per_page = 12 

    books_query = Book.query.filter_by(subject_id=id).filter(Book.stock > 0, Book.is_original == True)
    pagination = books_query.paginate(page=page, per_page=per_page, error_out=False)
    get_sub = pagination.items
    
    additional_books = Book.query.filter_by(subject_id=id).filter(Book.stock > 0, Book.is_original == False).all()
    facultiess = Faculty.query.join(Book, (Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book, (Subject.id == Book.subject_id)).all()

    average_rating = {}
    for book in get_sub:
        ratings = [rating.rating for rating in book.book_ratings]
        average_rating[book.id] = sum(ratings) / len(ratings) if ratings else 0

    average_ratingsh = {}
    for sbook in additional_books:
        ratings = [rating.rating for rating in sbook.book_ratings]
        average_ratingsh[sbook.id] = sum(ratings) / len(ratings) if ratings else 0

    return render_template('home.html', books=get_sub, bookss=additional_books, facultiess=facultiess, subjects=subjects, pagination=pagination,average_rating=average_rating,average_ratingsh=average_ratingsh)




@views.route('/addfaculty', methods=['GET','POST'])
@login_required
def addfaculty():
    if request.method == "POST":
        getfaculty = request.form.get('faculty')
        
  
        existing_faculty = Faculty.query.filter_by(name=getfaculty).first()
        if existing_faculty:
            flash(f'Faculty "{getfaculty}" already exists.',  category='error')
            return redirect(url_for('views.addfaculty'))
        
        faculty = Faculty(name=getfaculty)
        db.session.add(faculty)
        db.session.commit()
        flash(f'Faculty "{getfaculty}" was added to your database.', 'success')
        return redirect(url_for('views.addbook'))
    
    return render_template('addfaculty.html')


@views.route('/addsub', methods=['GET','POST'])
@login_required
def addsub():  
    if request.method =="POST":
        getsubject = request.form.get('subject') 
        
    
        existing_subject = Subject.query.filter_by(name=getsubject).first()
        if existing_subject:
            flash(f'Subject "{getsubject}" already exists.',  category='error')
            return redirect(url_for('views.addsub'))
        
        sub = Subject(name=getsubject)  
        db.session.add(sub)
        db.session.commit()
        flash(f'Subject "{getsubject}" was added to your database.', 'success') 
        return redirect(url_for('views.addbook'))
    
    return render_template('addsub.html')




@views.route('/addbook', methods=['POST', 'GET'])
@login_required
def addbook():
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    users = User.query.all()
    form = Addbooks(request.form)
    photos = UploadSet('photos', IMAGES)
    if request.method == 'POST':
        name = form.name.data
        username = request.form.get("username")
        
       
        price_str = request.form.get('price')
 
        if not price_str:
            flash("Price cannot be empty", category='error')
            return redirect(url_for('views.addbook'))
        try:
            price = float(price_str)
        except ValueError:
            flash("Price must be a valid number",  category='error')
            return redirect(url_for('views.addbook'))
            
        stock = form.stock.data
        desc = form.discription.data
        con = form.condition.data
        faculty = request.form.get('faculty')
        subject = request.form.get('subject')
        
        image = photos.save(request.files['image'])
        user = current_user
        
       
        existing_book = Book.query.filter_by(name=name).first()
        book_is_banned = BannedBook.query.filter_by(book_name=name).first()
        if existing_book:
            flash("This book has been added. If you need to sell the same book, please add it at a different price in the book details.",  category='error')
            return redirect(url_for('views.addbook'))
        
        if book_is_banned:
            flash(f"You cannot add the book with title {name} as this book has been banned by the system.",category='error')
            return redirect(url_for('views.addbook'))


        addbo = Book(name=name, user_id=username, price=price, stock=stock, desc=desc, con=con, faculty_id=faculty,
                     subject_id=subject, image=image, user=user, is_original=True)
        db.session.add(addbo)
        db.session.commit()

        addstock = Stock(book_id=addbo.id, user_id=user.id, name=name, stock=stock, con=con, faculty_id=faculty,
                         subject_id=subject)
        db.session.add(addstock)
        db.session.commit()
        
        flash(f"Book {name} has been added!",  'success')
        return redirect(url_for('views.addbook'))
    
    return render_template('addbook.html', title="Add Book page", form=form, faculties=faculties, subjects=subjects, photos=photos, users=users)



@views.route('/addsbook/<int:book_id>', methods=['POST', 'GET'])
@login_required
def addsbook(book_id):
    form = Addbooks(request.form)
    original_book = Book.query.get_or_404(book_id)
    user = current_user

    if request.method == 'POST':
        price = form.price.data
        stock = form.stock.data
        con = form.condition.data
        addbo = Book(name=original_book.name, price=price, stock=stock, desc=original_book.desc,con=con, image=original_book.image, 
                     faculty_id=original_book.faculty_id, subject_id=original_book.subject_id, user_id=user.id,is_original=False)

        db.session.add(addbo)
        db.session.commit()

        addstock = Stock(book_id=addbo.id,user_id=user.id,name=original_book.name,stock=stock,con=con,faculty_id=original_book.faculty_id,subject_id=original_book.subject_id)
        db.session.add(addstock)
        db.session.commit()

        flash(f"Your book has been listed for sale", 'success' )
        return redirect(url_for('views.single_page', id=book_id))  

    return render_template('addsbook.html', form=form, user=user, book=original_book)






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
    
@views.route('/payment')
def payment():
    return render_template('payment.html')




@views.route('/order')
@login_required
def order():
    if 'Shopcart' not in session or not session['Shopcart']:
        flash('Your cart is empty',  category='error')
        return redirect(url_for('views.getCart'))

    order_details = session['Shopcart']
    total = 0
    user = current_user
    invoice = None

    try:
        session.modified = True
        for book_id, item in order_details.items():
            book = Book.query.get(book_id)
            if book:
                quantity_to_deduct = int(item['quantity'])
                if book.stock >= quantity_to_deduct:
                    book.stock -= quantity_to_deduct
                    total += float(item['price']) * quantity_to_deduct
                else:
                    flash(f'Insufficient stock for {book.name}. Please remove it from your cart.',  category='error')
                    return redirect(url_for('views.getCart'))

        invoice_number = secrets.token_hex(5)
        new_invoice = Invoice(invoice=invoice_number, user_id=user.id)
        db.session.add(new_invoice)
        db.session.flush()  

        for book_id, item in order_details.items():
            book = Book.query.get(book_id)
            if book:
                invoice_item = InvoiceItem(invoice_id=new_invoice.id,book_id=book.id,quantity=item['quantity'],price=float(item['price']))
                db.session.add(invoice_item)

        db.session.commit()
        invoice = new_invoice
        flash('Checkout successful. Your order has been placed.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during checkout. Please try again later.',  category='error')
        print(f"Error: {str(e)}")
        traceback.print_exc()

    session.pop('Shopcart', None)
    return render_template('order.html', order_details=order_details, total=total, user=user, invoices=[invoice])


   




@views.route('/history')
@login_required
def history():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()

    for invoice in invoices:
        invoice.total_price = sum(item.price * item.quantity for item in invoice.items)

    return render_template('history.html', invoices=invoices)


@views.route('/rate/<int:book_id>/<int:invoice_id>', methods=['GET', 'POST'])
@login_required
def rate(book_id, invoice_id):
    form = RatingForm()
    book = Book.query.get_or_404(book_id)
    invoice = Invoice.query.get_or_404(invoice_id)

    if invoice.user_id != current_user.id:
        flash('Invalid invoice.', 'warning')
        return redirect(url_for('views.home'))

    if invoice.status.lower() != 'complete':
        flash('You can only rate after payment is complete.', 'error')
        return redirect(url_for('views.home'))

    if form.validate_on_submit():
        rated = Rating.query.filter_by(user_id=current_user.id, book_id=book_id, invoice_id=invoice_id).first()

        if rated:
            flash('You have already rated this book for this order.', 'error')
        else:
            rating = Rating(rating=form.rating.data, user_id=current_user.id, book_id=book_id, invoice_id=invoice_id)
            db.session.add(rating)
            db.session.commit()
            flash('Rating submitted successfully', 'success')

        return redirect(url_for('views.home'))
    
    return render_template('rate.html', form=form, book=book)






