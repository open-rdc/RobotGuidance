import cv2
import os

def load_images_from_folder(folder):
	images = []
	for filename in os.listdir(folder):
	    img = cv2.imread(os.path.join(folder,filename))
	    if img is not None:
	        images.append(img)
	return images

folder = ['center', 'left', 'right', 'near', 'none']
for folder_name in folder:
	images = load_images_from_folder(folder_name)

	i = 0
	while i < len(images):
		img = images[i]
		img = cv2.flip(img,1)
		if folder_name == 'left':
			cv2.imwrite('right'+'/'+str(i)+'.png',img)
		elif folder_name == 'right':
			cv2.imwrite('left'+'/'+str(i)+'.png',img)
		else:
			cv2.imwrite(folder_name+'/'+str(i)+'.png',img)
		i += 1
	print(folder_name, 'done')
