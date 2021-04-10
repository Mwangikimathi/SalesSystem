from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nelsonkimathi123@localhost:5432/sales_database'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class Item(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    stock = db.Column(db.Integer, unique=True, nullable=False)
    buying_price = db.Column(db.Integer, unique=False, nullable=False)
    selling_price = db.Column(db.Integer, unique=False, nullable=False)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    quantity = db.Column(db.Integer, primary_key=True)
    created_at =  db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'),nullable=False)
    inventories = db.relationship('Item',backref=db.backref('sales', lazy=True))


@app.route('/', methods = ['GET','POST'])
def add_details():
    if request.method == 'POST':
       name = request.form['name']
       stock = request.form['stock']
       buying_price = request.form['buying_price']
       selling_price = request.form['selling_price']
     
       print(name ,stock, buying_price ,selling_price)
       inventories = Item(name = name, stock = stock, buying_price = buying_price, selling_price = selling_price)
       print('Record successfully added')
       db.session.add(inventories)
       db.session.commit()
       return redirect(url_for('add_details'))
    else:
        goods = Item.query.all()
        return render_template('items.html', goods = goods)

@app.route('/sale/<int:inv_id>', methods = ['GET','POST'])
def make_sales(inv_id):
    if request.method == 'POST':
       quantity = request.form['quantity']
       inv_id = request.form['inv_id']
       
       n = Item.query.filter_by(id = inv_id).first()
       n.stock = int(n.stock) - int(quantity)
       if int(n.stock) - int(quantity) <= 0:
           flash(u"Quantity entered is more than stock", 'error')
           return redirect(url_for('add_details'))
           
       db.session.add(n)
       db.session.commit()

       print(quantity ,inv_id)
       sale = Sale(quantity = quantity, inv_id = inv_id)
       db.session.add(sale)
       db.session.commit()
       return redirect(url_for('add_details'))
    else:
        return render_template('items.html')

@app.route('/edit/<int:y>', methods = ['GET','POST'])
def edititem(y):
    if request.method == 'GET':
        editem = Item.query.filter_by(id = y).first()
        print(editem)

        return render_template('edititem.html', form = editem)
    else:
       editem = Item.query.filter_by(id = y).first()
       editem.name = request.form['name']
       editem.stock = request.form['stock']
       editem.buying_price = request.form['buying_price']
       editem.selling_price = request.form['selling_price']

       db.session.add(editem)
       db.session.commit()
       print("Record successfully edited")
       return redirect(url_for('add_details'))

    


@app.route('/viewsales/<int:x>', methods = ['GET'])
def viewsales(x):
    if request.method == 'GET':
        item_sale = Sale.query.filter_by(inv_id = x).all()
        print(item_sale)
        return render_template('viewsales.html', posts = item_sale)


if __name__=="__main__":
    app.run(debug=True)

