from PIL import Image
import random

img = Image.open(r"photo.jpg") 
 
left = random.randint(0, 150)
top = random.randint(50, 150)
right = random.randint(1294, 1424)
bottom = random.randint(650, 750)
 
img_res = img.crop((left, top, right, bottom)) 
img_res = img_res.convert('RGB')
 
# img_res.show()
img_res.save("photo.jpg")