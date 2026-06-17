from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "bdb_secure_key_2026" 

# --- DATA STORAGE ---
accounts = {
    "1001": {
        "name": "Manisha", 
        "pin": "1234", 
        "balance": 5000.0,
        "history": ["Account opened with initial deposit of ₹5000.0"]
    }
}

@app.route('/')
def home():
    user_data = accounts.get(session.get('user'))
    return render_template('index.html', user=user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc_no = request.form.get('acc_no')
        pin = request.form.get('pin')
        if acc_no in accounts and accounts[acc_no]['pin'] == pin:
            session['user'] = acc_no
            flash(f"Welcome back, {accounts[acc_no]['name']}!")
            return redirect(url_for('home'))
        flash("Invalid Account Number or PIN.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Successfully logged out.")
    return redirect(url_for('login'))

@app.route('/create_page')
def create_page():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    acc_no = request.form.get('acc_no')
    pin = request.form.get('pin')
    try:
        bal = float(request.form.get('balance', 0))
        if acc_no in accounts:
            flash("Account number already exists!")
            return redirect(url_for('create_page'))
        
        accounts[acc_no] = {
            'name': name, 'pin': pin, 'balance': bal, 
            'history': [f"Account created with ₹{bal}"]
        }
        session['user'] = acc_no
        flash(f"Account created! Welcome, {name}.")
        return redirect(url_for('home'))
    except ValueError:
        flash("Invalid balance amount.")
        return redirect(url_for('create_page'))

# --- TRANSACTIONS ---

@app.route('/deposit_page')
def deposit_page():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('deposit.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    acc_no = session.get('user')
    try:
        amount = float(request.form.get('amount', 0))
        if amount > 0:
            accounts[acc_no]['balance'] += amount
            accounts[acc_no]['history'].append(f"Deposited: ₹{amount}")
            flash(f"Deposited ₹{amount} successfully.")
            return redirect(url_for('home'))
        flash("Enter a valid amount.")
    except: pass
    return redirect(url_for('deposit_page'))

@app.route('/withdraw_page')
def withdraw_page():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('withdraw.html')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    acc_no = session.get('user')
    try:
        amount = float(request.form.get('amount', 0))
        if 0 < amount <= accounts[acc_no]['balance']:
            accounts[acc_no]['balance'] -= amount
            accounts[acc_no]['history'].append(f"Withdrew: ₹{amount}")
            flash(f"Withdrew ₹{amount} successfully.")
            return redirect(url_for('home'))
        flash("Insufficient funds.")
    except: pass
    return redirect(url_for('withdraw_page'))

@app.route('/enquiry_page')
def enquiry_page():
    if 'user' not in session: return redirect(url_for('login'))
    acc_no = session['user']
    return render_template('enquiry.html', user=accounts[acc_no], acc_no=acc_no)

@app.route('/history')
def history():
    if 'user' not in session: return redirect(url_for('login'))
    acc_no = session['user']
    user_history = accounts[acc_no].get('history', [])
    return render_template('history.html', history=user_history)

if __name__ == '__main__':
    app.run(debug=True)
