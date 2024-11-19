import uuid
import base64
import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from .models import storeURL
from io import BytesIO
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def input_url(request):
    url = None
    unique_id = None
    img_base64 = None
    error_message = None
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            validator = URLValidator()
            try:
                validator(url)
                unique_id = str(uuid.uuid4())
                # Save to the database
                store_url = storeURL(url=url, unique_id=unique_id)
                store_url.save()
                # Generate QR Code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                # Convert image to Base64
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
                response = HttpResponse(buffer, content_type="image/png")
                response['Content-Disposition'] = f'attachment; filename="qr_code_{unique_id}.png"'
                return response

            except ValidationError:
                error_message = "Invalid URL. Please enter a valid URL."
    # Fetch all stored URLs
    url_records = storeURL.objects.all()
    # Render the template
    return render(request, 'qr_generator/base.html', {
        'url': url,
        'unique_id': unique_id,
        'img_base64': img_base64,
        'url_records': url_records,
        'error_message': error_message
    })
