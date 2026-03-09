from reportlab.pdfgen import canvas

def buat_surat(nama,alamat):

    file = "surat_"+nama+".pdf"

    c = canvas.Canvas(file)

    c.drawString(100,750,"SURAT KETERANGAN DOMISILI")

    c.drawString(100,700,"Nama : "+nama)

    c.drawString(100,680,"Alamat : "+alamat)

    c.save()

    return file