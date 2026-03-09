from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Warga(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    no_kk = db.Column(db.String(20))
    nik = db.Column(db.String(20), unique=True)

    nama = db.Column(db.String(100))

    tanggal_lahir = db.Column(db.String(20))

    umur = db.Column(db.Integer)

    jenis_kelamin = db.Column(db.String(20))

    pekerjaan = db.Column(db.String(100))

    pendidikan = db.Column(db.String(50))