from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nelsonkimathi123@localhost:5432/sales_database'
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class Item(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), unique=True, nullable=False)
    buying_price = db.Column(db.Integer, unique=True, nullable=False)
    selling_price = db.Column(db.Integer, unique=True, nullable=False)



@app.route('/', methods = ['GET','POST'])
def add_details():
    if request.method == 'POST':
       name = request.form['name']
       type = request.form['type']
       buying_price = request.form['buying_price']
       selling_price = request.form['selling_price']
     
       
       print(name ,type ,buying_price ,selling_price)
       inventories = Item(name = name, type = type, buying_price = buying_price, selling_price = selling_price)
       print('Record successfully added')
       db.session.add(inventories)
       db.session.commit()
       return redirect(url_for('add_details'))
    else:
        goods = Item.query.all()
        return render_template('items.html',goods = goods)



if __name__=="__main__":
    app.run(debug=True)


