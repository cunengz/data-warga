from flask import Flask, render_template, request, redirect, session, url_for, flash
from models import db, Admin, Warga   # gunakan db dari models.py
import os
from werkzeug.utils import secure_filename
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "admin123"
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder
app.config['UPLOAD_FOLDER'] = 'static/ktp'

# Inisialisasi db dari models.py
db.init_app(app)

# =========================
# BUAT DATABASE
# =========================
with app.app_context():
    db.create_all()
    if not Admin.query.first():
        admin = Admin(
            username="admin",
            password=generate_password_hash("admin")
        )
        db.session.add(admin)
        db.session.commit()
# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session.clear()
            session["admin"] = admin.username
            return redirect(url_for("dashboard"))
        else:
            flash("Username atau password salah")

    return render_template("login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
@login_required
def dashboard():
    if "admin" not in session:
        return redirect("/")
    total = Warga.query.count()
    laki = Warga.query.filter_by(jenis_kelamin="Laki-Laki").count()
    perempuan = Warga.query.filter_by(jenis_kelamin="Perempuan").count()
    return render_template("admin/dashboard.html", total=total, laki=laki, perempuan=perempuan)

# =========================
# DATA WARGA
# =========================
@app.route("/warga")
@login_required
def warga():
    if "admin" not in session:
        return redirect("/")
    data = Warga.query.all()
    return render_template("admin/warga.html", warga=data)

# =========================
# TAMBAH WARGA
# =========================
@app.route("/tambah_warga")
@login_required
def tambah_warga():
    if "admin" not in session:
        return redirect("/")
    return render_template("admin/tambah_warga.html")

# =========================
# SIMPAN WARGA
# =========================
@app.route("/simpan_warga", methods=["POST"])
def simpan_warga():
    data = Warga(
        no_kk=request.form['no_kk'],
        nik=request.form['nik'],
        nama=request.form['nama'],
        tanggal_lahir=request.form['tanggal_lahir'],
        umur=request.form['umur'],
        jenis_kelamin=request.form['jenis_kelamin'],
        pekerjaan=request.form['pekerjaan'],
        pendidikan=request.form['pendidikan']
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for("warga"))

# =========================
# EDIT WARGA
# =========================
@app.route("/edit_warga/<int:id>", methods=["GET","POST"])
def edit_warga(id):
    warga = Warga.query.get_or_404(id)
    if request.method == "POST":
        warga.nama = request.form["nama"]
        warga.tanggal_lahir = request.form["tanggal_lahir"]
        warga.jenis_kelamin = request.form["jenis_kelamin"]
        warga.pekerjaan = request.form["pekerjaan"]
        warga.pendidikan = request.form["pendidikan"]
        db.session.commit()
        return redirect(url_for("warga"))
    return render_template("admin/edit_warga.html", warga=warga)

# =========================
# UPDATE WARGA
# =========================
@app.route("/update_warga/<int:id>", methods=["POST"])
def update_warga(id):
    data = Warga.query.get_or_404(id)
    data.no_kk = request.form['no_kk']
    data.nik = request.form['nik']
    data.nama = request.form['nama']
    data.tanggal_lahir = request.form['tanggal_lahir']
    data.umur = request.form['umur']
    data.jenis_kelamin = request.form['jenis_kelamin']
    data.pekerjaan = request.form['pekerjaan']
    data.pendidikan = request.form['pendidikan']
    db.session.commit()
    return redirect(url_for("warga"))

# =========================
# HAPUS WARGA
# =========================
@app.route("/hapus_warga/<int:id>")
def hapus_warga(id):
    warga = Warga.query.get_or_404(id)
    db.session.delete(warga)
    db.session.commit()
    return redirect(url_for("warga"))

# =========================
# STATISTIK
# =========================
@app.route("/statistik")
def statistik():
    sql = text("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN jenis_kelamin='Laki-Laki' THEN 1 ELSE 0 END) AS laki,
            SUM(CASE WHEN jenis_kelamin='Perempuan' THEN 1 ELSE 0 END) AS perempuan,
            SUM(CASE WHEN pendidikan IN ('SD') THEN 1 ELSE 0 END) AS sd,
            SUM(CASE WHEN pendidikan IN ('SMP','SLTP') THEN 1 ELSE 0 END) AS smp,
            SUM(CASE WHEN pendidikan IN ('SMA','SMU') THEN 1 ELSE 0 END) AS sma,
            SUM(CASE WHEN CAST((julianday('now') - julianday(tanggal_lahir)) / 365.25 AS INT) BETWEEN 0 AND 12 THEN 1 ELSE 0 END) AS anak,
            SUM(CASE WHEN CAST((julianday('now') - julianday(tanggal_lahir)) / 365.25 AS INT) BETWEEN 13 AND 19 THEN 1 ELSE 0 END) AS remaja,
            SUM(CASE WHEN CAST((julianday('now') - julianday(tanggal_lahir)) / 365.25 AS INT) BETWEEN 20 AND 59 THEN 1 ELSE 0 END) AS dewasa,
            SUM(CASE WHEN CAST((julianday('now') - julianday(tanggal_lahir)) / 365.25 AS INT) >= 60 THEN 1 ELSE 0 END) AS lansia
        FROM warga
    """)
    result = db.session.execute(sql).mappings().first()
    total = result["total"] or 0
    laki = result["laki"] or 0
    perempuan = result["perempuan"] or 0
    sd = result["sd"] or 0
    smp = result["smp"] or 0
    sma = result["sma"] or 0
    anak = result["anak"] or 0
    remaja = result["remaja"] or 0
    dewasa = result["dewasa"] or 0
    lansia = result["lansia"] or 0
    persentase_sma = (sma / total * 100) if total > 0 else 0
    return render_template("statistik.html",
                           total=total, laki=laki, perempuan=perempuan,
                           sd=sd, smp=smp, sma=sma,
                           anak=anak, remaja=remaja, dewasa=dewasa, lansia=lansia,
                           persentase_sma=round(persentase_sma, 2))

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Anda berhasil logout")
    return redirect(url_for("login"))

# =========================
# IMPORT EXCEL
# =========================
from routes.import_excel import import_excel
app.register_blueprint(import_excel)

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)