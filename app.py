from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
#DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model Creation for DB
class Post(db.Model):
    id_no = db.Column(db.Integer,primary_key =True)
    account_no = db.Column(db.Integer)
    date = db.Column(db.Date)
    transaction_details = db.Column(db.String(255))
    value_date = db.Column(db.Date)
    withdrawal_amt = db.Column(db.String(50))
    deposit_amt = db.Column(db.String(50))
    balance_amt = db.Column(db.String(50)) 

# Schema Creation for json-parsing usage
class PostSchema(ma.Schema):
    class Meta:
        fields = ("account_no", "date", "transaction_details","value_date","withdrawal_amt","deposit_amt","balance_amt")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


#Request No 1
@app.route('/transactions/<date_>/',methods =['GET'])
def get_transaction(date_):
    date_ = datetime.strptime(date_, '%d-%m-%y')
    print(date_)
    return jsonify([
        { "Account No":transaction.account_no,"Date":transaction.date,"Transaction Details":transaction.transaction_details,"Value Date":transaction.value_date,"Withdrawal AMT":transaction.withdrawal_amt,"Deposit AMT":transaction.deposit_amt,"Balance AMT":transaction.balance_amt}
        for transaction in Post.query.filter_by(date=date_.date()).all()])

#Request No 2
@app.route('/balance/<date_>/',methods =['GET'])
def get_balance(date_):
    date_ = datetime.strptime(date_, '%d-%m-%y')
    print(date_)
    transaction =Post.query.filter_by(date=date_.date()).all()
    return jsonify(
        {"Balance AMT":transaction[-1].balance_amt})

#Request No 3
@app.route('/details/<ID>/',methods =['GET'])
def get_by_id(ID):
    transaction = Post.query.get(ID)
    return jsonify({ "Account No":transaction.account_no,"Date":transaction.date,"Transaction Details":transaction.transaction_details,"Value Date":transaction.value_date,"Withdrawal AMT":transaction.withdrawal_amt,"Deposit AMT":transaction.deposit_amt,"Balance AMT":transaction.balance_amt})

#Request No 4
@app.route('/add/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    transaction = Post.query.all()
    if 'Account No' not in data or  'Date' not in data or 'Transaction Details' not in data:
        return (jsonify({'error': 'Bad Request','message': 'Account No or Date or Transaction Details not given'}),400)
    if 'Balance AMT' not in data:
        return jsonify({'error': 'Bad Request','message': 'Balance Amount not given'}),400
    id_ = transaction[-1].id_no+1
    u = Post(id_no =id_, account_no = data['Account No'],date = datetime.strptime(data['Date'], '%d %b %y'),transaction_details = data['Transaction Details'],value_date = datetime.strptime(data['Value Date'], '%d %b %y'),withdrawal_amt = data['Withdrawal AMT'],deposit_amt = data['Deposit AMT'],balance_amt = data['Balance AMT'])
    db.session.add(u)
    db.session.commit()
    return ({'message':'sucess'},201)

if __name__ == '__main__':
    app.run()
