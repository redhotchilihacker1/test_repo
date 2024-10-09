from PIL import Image
import pytesseract
import cv2
import numpy as np

# Tesseract'ı kullanmak için Tesseract binary dosyasının yolunu belirtiyoruz
# Kali'de Tesseract yolunu belirtmeye gerek yok, varsayılan yol kullanılacaktır

# Görüntüyü yükleyin
image_path = 'captcha_image.png'  # Çözülecek captcha'nın dosya yolu
image = cv2.imread(image_path)

# Görüntüyü gri tonlamaya çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Görüntü üzerindeki gürültüyü azalt
gray = cv2.medianBlur(gray, 3)

# OCR işlemi yap
text = pytesseract.image_to_string(gray, config='--psm 6')

print(f'Çözülen Captcha Metni: {text}')
