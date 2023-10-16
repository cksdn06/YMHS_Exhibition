import qrcode

img_url = qrcode.make("https://drive.google.com/file/d/1_vp6fNGR2gFjfuewSK3kWiUKJjgF7qwH/view?usp=sharing")
img_url.save("C:\\Users\\User\\Desktop\\111\\output.jpg")
print(img_url.size)
