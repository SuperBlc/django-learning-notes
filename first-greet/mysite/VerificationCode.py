from PIL import Image, ImageDraw, ImageFont
import random

def VerificationCode():
	bgcolor = (random.randrange(20, 120), random.randrange(20, 120),
		random.randrange(20, 120))
	width = 100
	height = 50

	img = Image.new('RGB', (width, height), bgcolor)
	draw = ImageDraw.Draw(img)
	for i in range(0, 30):
		xy = [(random.randrange(0, width), random.randrange(0, height)),
			(random.randrange(0, width), random.randrange(0, height))]
		fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
		draw.line(xy, fill=fill, width=1)
	
	candidate = [str(i) for i in range(10)] + \
		[chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
	
	rand_str = ""
	for i in range(0,4):
		rand_str += candidate[random.randrange(0, len(candidate)-1)]

	text_font = ImageFont.truetype("arial.ttf", 40)
	for i in range(4):
		text_fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
		draw.text((i*20+10,2), rand_str[i], font=text_font, fill=text_fill)

	for i in range(0, 300):
		xy = (random.randrange(0, width), random.randrange(0, height))	
		fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
		draw.point(xy, fill=fill)
	print(rand_str)
	img.save("VerifyCode-%s.png"%rand_str)

def main():
	VerificationCode()

if __name__=="__main__":
	main()