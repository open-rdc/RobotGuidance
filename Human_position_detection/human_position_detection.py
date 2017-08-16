import argparse
import numpy as np
from PIL import Image
import glob
import pickle
import chainer
import chainer.functions as F
import chainer.links as L
import chainer.serializers
from chainer.datasets import tuple_dataset
from chainer import Chain, Variable, optimizers
from chainer import training
from chainer.training import extensions
import alexLike

def main():

	#=======================chainer setting=======================
	parse = argparse.ArgumentParser(description='human detection train')
	parse.add_argument('--batchsize','-b',type=int, default=5,
						help='Number if images in each mini batch')
	parse.add_argument('--epoch','-e',type=int, default=20,
						help='Number of sweeps over the dataset to train')
	parse.add_argument('--gpu','-g',type=int, default=0,
						help='GPU ID(negative value indicates CPU')
	parse.add_argument('--out','-o', default='result',
						help='Directory to output the result')
	parse.add_argument('--resume','-r', default='',
						help='Resume the training from snapshot')
	parse.add_argument('--unit','-u', type=int, default=1000,
						help='Number of units')
	parse.add_argument('--path','-p', default='')
	parse.add_argument('--channel','-c', default=3)

	args = parse.parse_args()

	print('GPU: {}'.format(args.gpu))
	print('# unit: {}'.format(args.unit))
	print('# Minibatch-size: {}'.format(args.batchsize))
	print('# epoch: {}'.format(args.epoch))
	print('')
	#=======================chainer setting=======================

	#=======================read images & labels set=======================
	pathsAndLabels = []
	pathsAndLabels.append(np.asarray(['./data/center/', 0]))
	pathsAndLabels.append(np.asarray(['./data/left/', 1]))
	pathsAndLabels.append(np.asarray(['./data/right/', 2]))
	pathsAndLabels.append(np.asarray(['./data/near/', 3]))
	pathsAndLabels.append(np.asarray(['./data/none/', 4]))

	allData = []
	for pathAndLabel in pathsAndLabels:
		path = pathAndLabel[0]
		label = pathAndLabel[1]
		imagelist = glob.glob(path + "*")
		for imgName in imagelist:
			allData.append([imgName, label])
	allData = np.random.permutation(allData)
	#=======================read images & labels set=======================

	#=======================set up data format=======================
	imageData = []
	labelData = []
	for pathAndLabel in allData:
		img = Image.open(pathAndLabel[0])
		r,g,b = img.split()
		rImgData = np.asarray(np.float32(r)/255.0)
		gImgData = np.asarray(np.float32(g)/255.0)
		bImgData = np.asarray(np.float32(b)/255.0)
		imgData = np.asarray([rImgData, gImgData, bImgData])
		imageData.append(imgData)
		labelData.append(np.int32(pathAndLabel[1]))

	threshold = np.int32(len(imageData)/5*4)
	train = tuple_dataset.TupleDataset(imageData[0:threshold], labelData[0:threshold])
	test  = tuple_dataset.TupleDataset(imageData[threshold:],  labelData[threshold:])
	#=======================set up data format=======================

	#=======================learning program=======================
	model = L.Classifier(alexLike.AlexLike(len(pathsAndLabels)))
	if args.gpu >= 0:
		chainer.cuda.get_device(args.gpu).use()  # Make a specified GPU current
		model.to_gpu()  # Copy the model to the GPU

	# Setup an optimizer
	optimizer = chainer.optimizers.Adam()
	optimizer.setup(model)

	#chainer.serializers.load_npz(args.model, model)
	#chainer.serializers.load_npz(args.optimizer, optimizer)

	train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
	test_iter = chainer.iterators.SerialIterator(test, args.batchsize,
												repeat=False, shuffle=False)

	# Set up a trainer
	updater = training.StandardUpdater(train_iter, optimizer, device=args.gpu)
	trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)

	trainer.extend(extensions.Evaluator(test_iter, model, device=args.gpu))
	trainer.extend(extensions.dump_graph('main/loss'))
	trainer.extend(extensions.LogReport())
	if extensions.PlotReport.available():
		trainer.extend(
			extensions.PlotReport(['main/loss', 'validation/main/loss'],
									'epoch', file_name='loss.png'))
		trainer.extend(
			extensions.PlotReport(
				['main/accuracy', 'validation/main/accuracy'],
				'epoch', file_name='accuracy.png'))

	trainer.extend(extensions.PrintReport(
		['epoch', 'main/loss', 'validation/main/loss',
		'main/accuracy', 'validation/main/accuracy']))
	trainer.extend(extensions.ProgressBar())

	trainer.run()	

	outputname = 'my_output_' + str(len(pathsAndLabels))
	modelOutName = outputname + '.model'
	OptimOutName = outputname + '.state'

	chainer.serializers.save_npz(modelOutName, model)
	chainer.serializers.save_npz(OptimOutName, optimizer)
	#=======================learning program=======================

if __name__ == '__main__':
	main()
