import chainer
import chainer.functions as F
import chainer.links as L
from chainer import Chain, iterators, optimizers, Variable, training
from chainer.datasets import TupleDataset, split_detaset_random
import numpy as np
import os
from os.path import expanduser


class Dataset(self, self.control):
	def 







class CNN(chainer.Chain):
	def __init__(self, n_channel=3, n_action=3):
		initializer = chainer.initializers.HeNormal()
		super(CNN, self).__init__(
			conv1=L.Convolution2D(n_channel, 32, ksize=8, stride=4, nobias=False, initialW=initializer),
			conv2=L.Convolution2D(32, 64, ksize=3, stride=2, nobias=False, initialW=initializer),
			conv3=L.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, initialW=initializer),
			conv4=L.Linear(960, 512, initialW=initializer),
			fc5=L.Linear(512, n_action, initialW=np.zeros((n_action, 512), dtype=np.float32))
		)

	def __call__(self, x, test=False):
		s = chainer.Variable(x)
		h1 = F.relu(self.conv1(s))
		h2 = F.relu(self.conv2(h1))
		h3 = F.relu(self.conv3(h2))
		h4 = F.relu(self.conv4(h3))
		h = self.fc5(h4)
		return h


class learning:
	def __init__(self, n_channel=3, n_action=3):
		self.cnn= CNN(n_channel, n_action)
		try:
			self.cnn.to_gpu()
		except:
			print("No GPU")
		self._iteraters = iterater
		batch_size = 4
		trainer

		self.optimizer = chainer.optimizers.Adam(eps=1e-2)
		self.optimizer.setup(self.cnn)
		self.n_action = n_action

		
		home = expanduser("~")1:
		if os.path.isdir(home + '/agent'):
			self.agent.load('agent')
		
	def 





if __name__ == '__main__':
	dl = deep_learning()
