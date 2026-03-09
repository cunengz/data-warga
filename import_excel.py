import pandas as pd
from flask import Blueprint, request, jsonify
from models import db, Warga

import_excel = Blueprint('import_excel', __name__)

@import_excel.route('/api/import-warga', methods=['POST'])
def import_warga():

    file = request.files['file']
    df = pd.read_excel(file)

    total = len(df)
    success = 0
    duplicate = 0

    for index, row in df.iterrows():

        nik = str(row['NIK'])

        # cek nik ganda
        cek = Warga.query.filter_by(nik=nik).first()

        if cek:
            duplicate += 1
            continue

        warga = Warga(
            kk=str(row['No KK']),
            nik=nik,
            nama=row['Nama Lengkap'],
            alamat="Pasir Luhur",
            rt="01",
            rw="02",
            umur=int(row['umur']),
            pekerjaan=row['Pekerjaan'],
            pendidikan=row['Pendidikan']
        )

        db.session.add(warga)
        success += 1

    db.session.commit()

    return jsonify({
        "total": total,
        "success": success,
        "duplicate": duplicate
    })