from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
            new_transaction = Transaction(description=description, amount=float(amount), date=date)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding transaction: {e}', 'danger')
        return redirect(url_for('transactions'))
    else:
        transactions = Transaction.query.order_by(Transaction.date).all()
        return render_template('transactions.html', transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
            new_transaction = Transaction(description=description, amount=float(amount), date=date)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding transaction: {e}', 'danger')
        return redirect(url_for('transactions'))
    return render_template('add_transaction.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        transaction.description = request.form['description']
        transaction.amount = request.form['amount']
        date = request.form['date']
        try:
            transaction.date = datetime.strptime(date, '%Y-%m-%d')
            db.session.commit()
            flash('Transaction updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating transaction: {e}', 'danger')
        return redirect(url_for('transactions'))
    return render_template('update_transaction.html', transaction=transaction)

@app.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    try:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting transaction: {e}', 'danger')
    return redirect(url_for('transactions'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
