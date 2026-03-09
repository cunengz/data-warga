from flask import Blueprint, request, redirect, render_template
import pandas as pd
from models import db, Warga

import_excel = Blueprint('import_excel', __name__)

@import_excel.route("/import_warga", methods=["GET","POST"])
def import_warga():

    if request.method == "POST":

        file = request.files['file']

        if file:

            df = pd.read_excel(file)

            for i, row in df.iterrows():

                cek = Warga.query.filter_by(nik=str(row['NIK'])).first()

                if not cek:

                    data = Warga(

                        no_kk=str(row['No KK']),
                        nik=str(row['NIK']),
                        nama=row['Nama Lengkap'],
                        tanggal_lahir=str(row['Tanggal Lahir']),
                        umur=int(row['umur']),
                        jenis_kelamin=row['Jenis Kelamin '],
                        pekerjaan=row['Pekerjaan'],
                        pendidikan=row['Pendidikan ']

                    )

                    db.session.add(data)

            db.session.commit()

        return redirect("/warga")

    return render_template("admin/import_warga.html")