from django.shortcuts import render
from smtplib import SMTPException
from kupon.models import Kupon
from .models import Payment
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from cart.forms import CartAddProductForm
from kupon.forms import KuponApplyForm
from cart.cart import Cart
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
import requests
import hmac
import hashlib
import json



PAYMENT_METHOD = (
    'banktransfer',  # Bank Transfer
    'va',            # Virtual Account
    'cstore',        # Convenience Store
    'qris',          # QRIS
)

PAYMENT_CHANNEL_VA = (
    'mandiri',
    'bni',
    'cimb',
)

PAYMENT_CHANNEL_TRANSFER = (
    'bca',
    'mandiri',
    'bni',
)

PAYMENT_CHANNEL_CONVENIENCE = (
    'alfamart',
    'indomaret',
)

PAYMENT_CHANNEL_QRIS = (
    'linkaja'
)

def ProsesPayment(request):
    print("Halaman Proses Pembayaran")
    if request.method == "POST":
        type = request.POST['type']
        nama = request.POST['nama']
        email = request.POST['email']
        nohp = request.POST['nohp']
        alamat = request.POST['alamat']
        note = request.POST['note']

        cart = Cart(request)

        if cart.kupon:
            harga = cart.get_total_price_after_discount()
            print("Harga Ada diskon", harga)
        else:
            harga = cart.get_total_price()
            print("Harga tidak diskon", harga)

        try:
            print("Validate Email")
            validate_email(email)
        except ValidationError:
            print("Email Error")
            return False

        # Method Payment
        if type == '1' or type == '2' or type == '3' or type == '4':
            print("Masuk tipe 1 - 4")
            paymentChannel = PAYMENT_CHANNEL_TRANSFER[int(type) - 1 ]
            paymentMethod = PAYMENT_METHOD[0]
        elif type == '5' or type == '6' or type == '7' or type == '8' or type == '9' or type == '10':
            print("Masuk tipe 5 - 10")
            paymentChannel = PAYMENT_CHANNEL_VA[int(type) - 5]
            paymentMethod = PAYMENT_METHOD[1]
        elif type == '11' or type == '12':
            print("Masuk tipe 11-12")
            paymentChannel = PAYMENT_CHANNEL_CONVENIENCE[int(type) - 11]
            paymentMethod = PAYMENT_METHOD[2]
        elif type == '13':
            print("Masuk tipe 13")
            paymentChannel = 'linkaja'
            paymentMethod = PAYMENT_METHOD[3]
        else:
            tipe = "Belum Berhasil"


        # API Sistem Pembayaran iPaymu
        ipaymyUrl = "https://sandbox.ipaymu.com"
        ipaymuVa = "0000005158644691"  # 1179000899
        ipaymuKey = "SANDBOX47DAF383-E52A-4A3D-AC88-809DB0307CA9-20220129084902"  # QbGcoO0Qds9sQFDmY0MWg1Tq.xtuh1
        encrypt_referenceId = hashlib.sha256(str(request.user.id).encode()).hexdigest()

        body = {
            "name": nama,
            "phone": nohp,
            "email": email,
            "amount": int(harga),
            "notifyUrl": "http://belajarprogram.com",
            "expired": '24',
            "expiredType": 'hours',
            "comments": note,
            "referenceId": encrypt_referenceId,
            "paymentMethod": paymentMethod,
            "paymentChannel": paymentChannel
        }

        data_body = json.dumps(body)
        data_body = json.dumps(body, separators=(',', ':'))
        encrypt_body = hashlib.sha256(data_body.encode()).hexdigest()
        stringtosign = "{}:{}:{}:{}".format("POST", ipaymuVa, encrypt_body, ipaymuKey)
        signature = hmac.new(ipaymuKey.encode(), stringtosign.encode(), hashlib.sha256).hexdigest().lower()
        timestamp = datetime.today().strftime('%Y%m%d%H%M%S')

        headers = {
            'Content-Type': 'application/json',
            'signature': signature,
            'va': ipaymuVa,
            'timestamp': timestamp,
        }

        response = requests.post(ipaymyUrl + '/api/v2/payment/direct', headers=headers, data=data_body)

        result = json.loads(response.text)
        print("Hasil Pembayaran", result)
        if result["Status"] == 200:
            pesan = "Pembayaran Anda Berhasil"
            cart.clear()
            request.session['kupon_id'] = None
        else:
            pesan = "Pembayaran anda tidak berhasil, cek kembali data yang anda input"
            data = {
                'pesan':pesan
            }
            return render(request, 'payment/payment.html', data)

        context = {
            'data': pesan
        }

        if type == '1' or type == '2' or type == '3' or type == '4' or type == '5' or type == '6' or type == '7' or type == '8' or type == '9' or type == '10':
            data_retrieve = {
                'nama': nama,
                'notransaksi': result["Data"]["TransactionId"],
                'nominal': result["Data"]["Total"],
                'expired': result["Data"]["Expired"],
                'atasnama': result["Data"]["PaymentName"],
                'norek': result["Data"]["PaymentNo"],
                'paymentmethod': paymentMethod,
            }

            subject = 'Pembayaran E-Commerce Media Belajarku'
            html_message = render_to_string('notify_email.html', data_retrieve)
            plain_message = strip_tags(html_message)
            from_email = 'E-Commerce Media Belajarku <belajar.program2022@gmail.com>'
            to = email

            try:
                # mail.send_mail(subject, plain_message, 'monses2785@gmail.com', ['hermanit08@yahoo.com'], html_message=html_message)
                data_payment = Payment(amount=harga, timestamp=timestamp, nama=nama, email=email, nohp=nohp, alamat=alamat)
                data_payment.save()
            except SMTPException as e:
                print('1. Terjadi kesalahan ketika mengirimkan email: ', e)


        elif type == '11' or type == '12':
            if type == '11':
                namaPaymentChannel = "Alfamart"
            else:
                namaPaymentChannel = "Indomaret"

            data_retrieve = {
                'nama': nama,
                'notransaksi': result["Data"]["TransactionId"],
                'nominal': int(harga.replace(".", "")),
                'expired': result["Data"]["Expired"],
                'paymentNo': result["Data"]["PaymentNo"],
                'paymentChannel': namaPaymentChannel,
                'title': note
            }

            subject = 'Pembayaran E-Commerce Media Belajarku'
            html_message = render_to_string('notify_email_convenience.html', data_retrieve)
            plain_message = strip_tags(html_message)
            from_email = 'E-Commerce Media Belajarku <belajar.program2022@gmail.com>'
            to = email

            try:
                # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                data_payment = Payment(amount=harga, timestamp=timestamp, nama=nama, email=email, nohp=nohp, alamat=alamat)
                data_payment.save()
            except SMTPException as e:
                print('2. Terjadi kesalahan ketika mengirimkan email: ', e)

        elif type == '13':
            try:
                data_payment = Payment(amount=harga, timestamp=timestamp, nama=nama, email=email, nohp=nohp, alamat=alamat)
                data_payment.save()
            except SMTPException as e:
                print('3. Terjadi kesalahan ketika mengirimkan email: ', e)

    return render(request, 'payment/success.html', context)

def PreparePayment(request):
    return render(request, 'payment/payment.html')
