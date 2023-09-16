import os
import base64
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.conf import settings  # Import Django settings

def save_captured_image(request):
    if request.method == "POST":
        data = request.POST.get("image", "")
        
        # Generate a unique filename (you can use any logic you prefer)
        random_filename = generate_random_filename()

        # Create the file path for the collected image
        file_path = os.path.join(settings.MEDIA_ROOT, "collected_data", f"{random_filename}.jpg")

        # Decode the Data URL and save it as a JPG image
        try:
            image_data = base64.b64decode(data.split(',')[1])
            with open(file_path, 'wb') as f:
                f.write(image_data)
            return JsonResponse({"message": "Image saved successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Error saving image: {str(e)}"}, status=500)

    return JsonResponse({"message": "Bad request"}, status=400)

def generate_random_filename():
    # You can implement your own logic to generate a random filename here
    # For simplicity, here's a basic example using a timestamp:
    import time
    timestamp = int(time.time() * 1000)
    return str(timestamp)
