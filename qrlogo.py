import qrcode
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# https://brentonmallen.com/posts/circular_qr_code/circular_qr/

def show_qr(img):
    plt.figure(figsize=(5,5))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# taking image which user wants
# in the QR code center
# local jpg file
Logo_link = 'Dominion_Energy_Logo.jpg'
logo = Image.open(Logo_link)

# image from url
# url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/360px-McDonald%27s_Golden_Arches.svg.png"
# response = requests.get(url)
# logo = Image.open(BytesIO(response.content))
# # logo = Image.open(requests.get(url, stream=True).raw)

# taking base width
basewidth = 100
 
# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth*2, hsize*2), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=18,
    mask_pattern=4,
)

# taking url or text
url = 'https://thermwisenc.ri-app.com/program/opt-out'
 
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make(fit=True)
 
# taking color name from user
QRcolor = 'Black'
 
# adding color to QR code
QRimg = QRcode.make_image(
    fill_color=QRcolor, back_color="white").convert('RGB')
 
# show_qr(QRimg)
# # set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)
 
# # save the QR code generated
# QRimg.save('QRHerLogo.png')

img_copy = QRimg.copy()
draw = ImageDraw.Draw(img_copy)
draw.ellipse(
    (30, 30, img_copy.size[1]-30, img_copy.size[1]-30),
    fill = None,
    outline ='black',
    width=30
)


# get fill texture
width, height = QRimg.size
left = 0
top = height // 3
right = width
bottom = 2 * height//3

img_copy = QRimg.copy()
draw_rec = ImageDraw.Draw(img_copy)
draw_rec.rectangle(
    (left, top, right, bottom),
    fill = None,
    outline ='red',
    width=5
)

cropped_section = QRimg.crop((left, top, right, bottom))
# show_qr(cropped_section)

rotated_crop = cropped_section.copy()
rotated_crop = rotated_crop.rotate(90, expand=True)
# show_qr(rotated_crop)
# fill top
QRimg.paste(cropped_section, (0, -cropped_section.size[1]//2 + 20 ))
# fill bottom
QRimg.paste(cropped_section, (0, QRimg.size[1] - cropped_section.size[1]//2 -20 ))
# fill left
QRimg.paste(rotated_crop, (-rotated_crop.size[0]//2 + 20, 0))
# fill right
QRimg.paste(rotated_crop, (QRimg.size[0] - rotated_crop.size[0]//2 - 20, 0))


# draw boundary circle
draw = ImageDraw.Draw(QRimg)
draw.ellipse(
    (30, 30, QRimg.size[1]-30, QRimg.size[1]-30),
    fill = None,
    outline ='black',
    width=30
)

draw.ellipse(
    (-rotated_crop.size[0],
     -cropped_section.size[1],
     QRimg.size[1] + rotated_crop.size[0],
     QRimg.size[1] + cropped_section.size[1]
     ),
    fill = None,
    outline ='white',
    width=340
)

show_qr(QRimg)
# save the QR code generated
QRimg.save('QRHerLogo.png')

# show_qr(img_copy)
print('QR code generated!')
