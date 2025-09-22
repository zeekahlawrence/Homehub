from flask import Flask, render_template, request, url_for , redirect , session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.secret_key = "246"


db = SQLAlchemy(app)
 
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name= db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    

    def __repr__(self):
        return f"<User {self.name} - {self.email}>"
    
class Property(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(90), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    images = db.Column(db.String(90))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Rentproperty(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(90), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    address=db.Column(db.String(200), nullable=False)
    images = db.Column(db.String(90))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Details(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    name = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    location =db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f"<User {self.name} - {self.email}"


@app.route('/home')
def home(): 
    return render_template('index.html')

@app.route('/search')
def search():

    query = request.args.get('query') # this gets the word that are typed into the search box

    if not query:
        results = Property.query.all()
        return render_template("buy.html", property=results) # if search box is empty
    
    results = Property.query.filter(
        (Property.title.ilike(f"%{query}%"))|
         (Property.address.ilike(f"%{query}%"))
    ).all()
    return render_template('buy.html', property=results, search_term=query)

@app.route('/buy')
def buy():

    property = Property.query.all()
    return render_template('buy.html', property=property)

    
@app.route('/sell')
def sell():
    return render_template('sell.html')

@app.route('/sellUsers', methods=['GET', 'POST'])
def sellUsers():
    if request.method =='POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        address = request.form['address']
        images = request.files['images']

        filename = secure_filename(images.filename)
        images.save(os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        ))

    new_property= Property(
        title=title,
        description=description,
        price=price,
        address=address,
        images=filename,
        user_id=1
    )
    db.session.add(new_property)
    db.session.commit()

    return redirect(url_for('buy'))             # After creating, send user to the Buy page to see it.
        
  
@app.route('/sellcon')
def sellcon():
    if request.method=='POST':
        name = request.form['name']
        email=request.form['email']
        number=request.form['number']  
        location=request.form['location']

        contact = Details(
        name=name,
        email=email,
        number=number,
        location=location

        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('details'))
                    
        

@app.route('/rent')
def rent():

    newProperty = Rentproperty.query.all()
    return render_template('rent.html',newProperty=newProperty)



@app.route('/rentUsers', methods=['GET', 'POST'])
def rentUsers(): 
    if request.method=='POST':
        title =request.form['title']
        description = request.form['description']
        price= request.form['price']
        address=request.form['address']
        images = request.files['images']

        filename= secure_filename(images.filename)
        images.save(os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
        ) )

        newProperty= Rentproperty(
            title=title,
            description=description,
            price=price,
            address= address,
            images=filename,
            user_id=1
            )
        db.session.add(newProperty)
        db.session.commit()

        flash("Rent property listed successfully!", "success")
        return redirect(url_for('rent'))

@app.route('/details')
def details():
    details = Details.query.all()
    return render_template('details.html', details=details)

    return render_template('details.html')
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/regUsers', methods=['POST'])
def regUsers():
    name = request.form['name']
    email = request.form['email']
    password= request.form['password']
    confirmpassword= request.form['confirmpassword']

    if password != confirmpassword:
        flash("passwords do not match", "danger")
        return redirect(url_for('register'))  
    
    else:
        saveUser = Users(name=name, email=email, password=password, confirmpassword=confirmpassword)
        db.session.add(saveUser)
        db.session.commit()

    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dologin', methods=['POST'])
def doLogin():
    email = request.form['email']
    password=request.form['password']

    getUsers = Users.query.all()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

