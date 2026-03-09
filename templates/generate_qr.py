import qrcode

def generate_qr(nik):

    img = qrcode.make(nik)

    path = "static/qrcode/"+nik+".png"

    img.save(path)

    return path