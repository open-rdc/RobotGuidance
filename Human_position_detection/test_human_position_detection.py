import chainer
import chainer.functions as F
import chainer.links as L
import chainer.serializers
from chainer.datasets import tuple_dataset
from chainer import Chain, Variable, optimizers
from chainer import training
from chainer.training import extensions
from PIL import Image
import argparse
import numpy as np
import glob
import alexLike
import cv2


def main():

	#=======================chainer setting=======================
	parse = argparse.ArgumentParser(description='test human position detection')
	parse.add_argument('--batchsize', '-b', type=int, default=100)
	parse.add_argument('--gpu', '-g', type=int, default=0) #change to -1 for use only CPU
	parse.add_argument('--model','-m', default='my_output_5.model')
	parse.add_argument('--channel', '-c', default=3)
	args = parse.parse_args()
	#=======================chainer setting=======================

	#=======================read images & labels set=======================
	pathsAndLabels = []
	pathsAndLabels.append(np.asarray(['./test/center/', 0]))
	pathsAndLabels.append(np.asarray(['./test/left/', 1]))
	pathsAndLabels.append(np.asarray(['./test/right/', 2]))
	pathsAndLabels.append(np.asarray(['./test/near/', 3]))
	pathsAndLabels.append(np.asarray(['./test/none/', 4]))

	allData = []
	for pathAndLabel in pathsAndLabels:
		path = pathAndLabel[0]
		label = pathAndLabel[1]
		imagelist = glob.glob(path + "*")
		for imgName in imagelist:
			allData.append([imgName, label])
	print('Number of datas is ' + str(len(allData)))
	print('')
	#=======================read images & labels set=======================

	#=======================testing program=======================
	outNumStr = args.model.split(".")[0].split("_")
	outnum = int(outNumStr[ len(outNumStr)-1 ])
	correct = 0

	model = L.Classifier(alexLike.AlexLike(outnum))
	chainer.serializers.load_npz(args.model, model)

	count = 1
	val = ['center', 'left', 'right', 'near', 'none']
	for pathAndLabel in allData:
		img = Image.open(pathAndLabel[0])
		r,g,b = img.split()
		rImgData = np.asarray(np.float32(r)/255.0)
		gImgData = np.asarray(np.float32(g)/255.0)
		bImgData = np.asarray(np.float32(b)/255.0)
		imgData = np.asarray([[[rImgData, gImgData, bImgData]]])
		x = Variable(imgData)
		y = F.softmax(model.predictor(x.data[0]))
		predR = np.round(y.data[0])
		for pre_i in np.arange(len(predR)):
			if predR[pre_i] == 1:
				if pathAndLabel[1].astype(int) == pre_i:
					correct += 1
					print('image number ', count, 'is correct')
				else:
					print('image number', count, 'is incorrect')
					a = imgData[0][0]
					a = np.swapaxes(a,0,2)
					a = np.swapaxes(a,0,1)
					a = a*255
					a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
					a = cv2.resize(a, (640, 480))
					cv2.putText(a,val[pre_i],(550,450), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
					cv2.putText(a,val[pathAndLabel[1].astype(int)],(20,450), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
					cv2.imwrite('wrong/'+str(count)+'.png',a)
		count += 1

	print('correct = ', correct/len(allData)*100, '%')
	#=======================testing program=======================

if __name__ == '__main__':
	main()
