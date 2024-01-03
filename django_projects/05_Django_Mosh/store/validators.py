from django.core.exceptions import ValidationError

def simgle_image_size_vsalidator(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Files cannot be larger than {max_size_mb} MB")
