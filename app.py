from flask import Flask, render_template, request, jsonify, session
import sqlite3
from models import init_db

app = Flask(__name__)
app.secret_key = "oasis_secret"

init_db()

# =====================
# الصفحات
# =====================
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

# =====================
# تسجيل
# =====================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (data['name'], data['email'], data['password']))
        conn.commit()
        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "error"})
    finally:
        conn.close()

# =====================
# تسجيل دخول
# =====================
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE email=? AND password=?",
              (data['email'], data['password']))
    user = c.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})

# =====================
# بيانات المستخدم
# =====================
@app.route('/me')
def me():
    if 'user_id' not in session:
        return jsonify({"error": "not logged in"})

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT name, email, balance FROM users WHERE id=?",
              (session['user_id'],))
    u = c.fetchone()
    conn.close()

    return jsonify({
        "name": u[0],
        "email": u[1],
        "balance": u[2]
    })

# =====================
# ADMIN APIs
# =====================

@app.route('/api/admin/pending')
def pending():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT id, email, type, amount, txid FROM requests WHERE status='pending'")
    rows = c.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "email": r[1],
            "type": r[2],
            "amount": r[3],
            "txid": r[4]
        })

    return jsonify({"pending": data})

@app.route('/api/admin/add_balance_by_email', methods=['POST'])
def add_balance():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("UPDATE users SET balance = balance + ? WHERE email=?",
              (data['amount'], data['email']))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "تم الشحن"})

@app.route('/api/admin/confirm_deposit', methods=['POST'])
def confirm_dep():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("UPDATE requests SET status='done' WHERE id=?", (data['id'],))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/admin/confirm_withdrawal', methods=['POST'])
def confirm_withdraw():
    data = request.json

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("UPDATE requests SET status='done' WHERE id=?", (data['id'],))

    conn.commit()
    conn.close()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
