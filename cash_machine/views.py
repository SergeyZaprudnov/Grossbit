from datetime import datetime
import pdfkit
import qrcode
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.decorators import api_view
from cash_machine.models import Item


@api_view(['POST'])
def cashe_machine(request):
    # получение списка товаров
    item_id = request.data.get('items', [])
    items = Item.objects.filter(id__in=item_id)

    # вычисление стоимости
    total_quantity = len(items)
    total_price = sum([item.price for item in items])

    # создание данных чека
    context = {
        'items': items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:')
    }

    # получение шаблона чека
    template = get_template('check.html')
    html = template.render(context)

    # создание чека в PDF-файле
    options = {
        'page-size': 'A6',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in'
    }
    pdf = pdfkit.from_string(html, False, options=options)

    # присвоение имени файла для сохранения
    file_name = 'check.pdf'
    file_path = f'media/{file_name}'

    # чтение и сохранение чека
    with open(file_path, 'wb') as file:
        file.write(pdf)

    # создание и сохранение QR-кода
    qr = qrcode.make(f'{{root}}/media/{file_name}')
    qr_file_path = 'media/qr_code.png'
    qr.save(qr_file_path)

    # чтение и отправка QR-кода в ответ
    with open(qr_file_path, 'rb') as file:
        qr_code = file.read()
    return HttpResponse(qr_code, content_type='image/png')
