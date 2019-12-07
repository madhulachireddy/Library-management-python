import smtplib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# MYSQL connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/studentlibrary'
db = SQLAlchemy(app)


# students class
class Users(db.Model):
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    roll_no = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80))
    pincode = db.Column(db.String(80))
    email = db.Column(db.String(100))

# Default method
    def __init__(self, name, password, roll_no, city, pincode, email):
        self.name = name
        self.password = password
        self.roll_no = roll_no
        self.city = city
        self.pincode = pincode
        self.email = email

# Like to-string method
    def __repr__(self):
        return '%s %s %d %s %s %s' % (self.name, self.password, self.roll_no, self.city, self.pincode, self.email)


# default api
@app.route('/')
def hello_world():
    return 'Hello World!'


# Users API calling
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    query = Users(name=data['name'], password=data['password'], roll_no=data['roll_no'], city=data['city'],
                       pincode=data['pincode'], email=data['email'])
    db.session.add(query)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


# Select query by passing name
@app.route('/retreving')
def retreive_data():
    #print("@@@@@@@@@@@")
    result = Users.query.filter_by(name='kavitha').all()
    print(result)
    #for x in range(0,):
     #   return jsonify(x)
    return "OK"


# Books class
class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    publisher_name = db.Column(db.String(80))
    copies_available = db.Column(db.Integer)

    def __init__(self, book_id, book_title, author, publisher_name, copies_available):
        self.book_id = book_id
        self.book_title = book_title
        self.author = author
        self.publisher_name = publisher_name
        self.copies_available = copies_available

    def __repr__(self):
        return '%d %s %s %s %d' % (self.book_id, self.book_title, self.author, self.publisher_name, self.copies_available)


# Books API
@app.route('/books', methods=['POST'])
def create_book():

    data2 = request.get_json()
    query2 = Books(book_id=data2['book_id'], book_title=data2['book_title'], author=data2['author'],
                   publisher_name=data2['publisher_name'], copies_available=data2['copies_available'])
    db.session.add(query2)
    db.session.commit()
    #return data2['book_id']
    return jsonify({'message': 'Books table created!'})


# Search query by passing book title
@app.route('/bookretreving')
def retreive_bookdata():
    bname = request.get_json()
    res = bname['book_title']
    print(bname)
    result = Books.query.filter_by(book_title=res).all()
    for x in result:
        print(x.author)
    return "OK"


# Books issuing class
class books_issue(db.Model):
    book_id = db.Column(db.Integer)
    roll_no = db.Column(db.Integer)
    issue_date = db.Column(db.DATE)
    submitted_date = db.Column(db.DATE)
    issue_id = db.Column(db.Integer, primary_key=True)
    expiry_date = db.Column(db.DATE)

    def __init__(self, book_id, roll_no, issue_date, submitted_date, issue_id, expiry_date):
        self.book_id = book_id
        self.roll_no = roll_no
        self.issue_date = issue_date
        self.submitted_date = submitted_date
        self.issue_id = issue_id
        self.expiry_date = expiry_date

    def __repr__(self):
        return '%d %d %s %s %d %s' % (self.book_id, self.roll_no, self.issue_date, self.submitted_date, self.issue_id,
                                      self.expiry_date)


@app.route('/books_issue', methods=['POST'])
def issuing():
    data3 = request.get_json()
    print(data3)
    query3 = books_issue(book_id=data3['book_id'], roll_no=data3['roll_no'], issue_date=data3['issue_date'],
                         submitted_date=data3['submitted_date'], issue_id=data3['issue_id'], expiry_date=data3['expiry_date'])
    db.session.add(query3)
    db.session.commit()
    storing = data3['book_id']
    print(storing)
    day1 = data3['issue_date']
    day2 = data3['expiry_date']
    issue_update(storing)
    return jsonify({'message': 'Books_issue_details created!'})


# Updating copies of books after issuing books to users
def issue_update(storing):
    result = Books.query.filter_by(book_id=storing).all()
    #print(result)
    for x in result:
    #fres = result['copies_available']
        fres = x.copies_available
        bid = x.book_id
    print(bid)
    #print(fres)
    count = fres-1
    #print(count)
    quering = Books.query.filter_by(book_id=storing).update(dict(copies_available=count))
    db.session.commit()


@app.route('/days')
def days_calculation():
    res1 = books_issue.query.all()
    for x in res1:
        x1 = x.roll_no
        x2 = x.issue_date
        x3 = x.expiry_date
        date_format = "%Y-%m-%d"
        n1 = datetime.strptime(str(x3), date_format)
        n2 = datetime.strptime(str(x2), date_format)
        diff = n1 - n2
        no_days = diff.days
        print(x1)
        print(x2)
        print(x3)
        print(no_days)
        stmail = Users.query.filter_by(roll_no=x1).all()
        for y in stmail:
            studentm = y.email
        print(studentm)
        if no_days <= 5:
            From = "madhulachireddy@gmail.com"
            To = studentm
            text = "Hi all, Please return the book as soon as possible. Your expiry date is about to come !!! This is" \
                   " an automatic email reminder."
            username = str("madhulachireddy@gmail.com")
            password = str("Madhu@22")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(From, To, text)
            server.quit()
            print("The reminder e-mail for expiry date less than 5 days was sent !")
        else:
            print("U still have time to return book")
    return "OKKK"


# Books returning  class
class Books_return(db.Model):
    book_id = db.Column(db.Integer)
    issue_id = db.Column(db.Integer)
    submitted_date = db.Column(db.DATE, primary_key=True)
    expiry_date = db.Column(db.DATE)
    fine = db.Column(db.Integer)


@app.route('/booksreturning', methods=['POST'])
def returning():

    data4 = request.get_json()
    query4 = Books_return(book_id=data4['book_id'], issue_id=data4['issue_id'], submitted_date=data4['submitted_date'],
                          expiry_date=data4['expiry_date'], fine=data4['fine'])
    db.session.add(query4)
    db.session.commit()
    storing = data4['issue_id']
    #fineupdate = data4['issue_id']
    return_update(storing)
    day1 = data4['submitted_date']
    day2 = data4['expiry_date']
    duecalculate(day1, day2, storing)
    #fine_calculation(day1, day2, storing)
    return jsonify({'message': 'Books returning table created!'})


# Calculating fine amount
def duecalculate(day1, day2, storing):
    if day1 > day2:
        addfine = Books_return.query.filter_by(issue_id=storing).all()
        # print(addfine)
        for x in addfine:
            final = x.fine+200
            # print(final)
        amount = Books_return.query.filter_by(issue_id=storing).update(dict(fine=final))
        db.session.commit()
        # print(amount)
    else:
        addfine = Books_return.query.filter_by(issue_id=storing).update(dict(fine=0))
        db.session.commit()


# Updating returning of books
def return_update(storing):
    result = books_issue.query.filter_by(issue_id=storing).all()
    #print(result)
    for x in result:
    #fres = result['copies_available']
        fres = x.book_id
    #print(fres)
    return_updating(fres)


def return_updating(fres):
    finalupdate = Books.query.filter_by(book_id=fres).all()
   #print(finalupdate)
    for x in finalupdate:
        fres2 = x.copies_available
    #print(fres2)
    count = fres2+1
    #print(count)
    quering = Books.query.filter_by(book_id=fres).update(dict(copies_available=count))
    db.session.commit()


if __name__ == '__main__':
    app.run()
