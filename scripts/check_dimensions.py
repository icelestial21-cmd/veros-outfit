import os
from PIL import Image

current_master = Image.open(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\web\assets\model_baku_master.jpg')
print("Current master size:", current_master.size)

frame0 = Image.open(r'C:\Users\User\Documents\Moradin Industries\04_Projects\Marko_Digital_Atelier\00_Working\silk_first_half_second\f_00.jpg')
print("Frame 0 size:", frame0.size)
