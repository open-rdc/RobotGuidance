import cv2
import os

folder = 'temp'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

images = load_images_from_folder(folder)

i = 0
while i < len(images):
	print(i+1)
	img = images[i]
	img2 = cv2.resize(img, (640, 480))
	#cv2.line(img2, (212,0), (212,480), (0,0,255),2)
	#cv2.line(img2, (428,0), (428,480), (0,0,255),2)
	cv2.imshow('image',img2)
	k = cv2.waitKey(0) & 0xFF
	if k == ord('a'):
		cv2.imwrite('left/'+folder+str(i)+'.png',img)
	elif k == ord('s'):
		cv2.imwrite('center/'+folder+str(i)+'.png',img)
	elif k == ord('d'):
		cv2.imwrite('right/'+folder+str(i)+'.png',img)
	elif k == ord('k'):
		cv2.imwrite('near/'+folder+str(i)+'.png',img)
	elif k == ord('l'):
		cv2.imwrite('none/'+folder+str(i)+'.png',img)
	elif k == ord(' '):
		cv2.imwrite('useless/'+folder+str(i)+'.png',img)
	else:
		i -= 1
	cv2.destroyAllWindows()
	i += 1
