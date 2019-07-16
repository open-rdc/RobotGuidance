import chainer
import chainer.functions as F
import chainer.links as L
from chainer import Chain, variable
import numpy as np
import matplotlib as plt
from collections import namedtuple
import os
from os.path import expanduser
'''
Transition = namedtuple(
    'Transition',(state, action, next_state)
)

# HYPER PARAM
MAX_STEPS = 200
NUM_EPISODE = 500
BATCH_SIZE = 32
CAPACITY = 10000

class ReplayMemory:

    def __init__(self,CAPACITY):
        self.capacity = CAPACITY
        self.memory = []
        self.index = 0

    def push(self,state,action,next_state):
        if len(self.memory) < self.capacity:
            self.memory.append(None)

        self.memory[self.index] = Transition(state, action, next_state)
        self.index = (self.index + 1) % self.capacity

    def sample(self, batch_size):
        return ramdom.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
'''

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

class deep_learning:
    def __init__(self, n_channel=3, n_action=3):
        self.n_action = n_action
        self.cnn = CNN(n_channel, n_action)
        self.optimizer = chainer.optimizers.Adam(eps=1e-2)
        self.optimizer.setup(self.cnn)


    def act_and_trains(self, imgobj, correct_action):

        n_epoch = MAX_STEPS
        n_batchsize = BATCH_SIZE
        iteration = 0

        results_train = {
            'loss': [],
            'accuracy': []
        }
        results_valid = {
            'loss': [],
            'accuracy': []
        }

        for epoch in range(n_epoch):

            order = np.random.permutation(range(len(imgobj)))

            loss_list = []
            accuracy_list = []

            for i in range(0, len(order), n_batchsize):
                index = order[i:i+n_batchsize]
                x_train_batch = imgobj[index,:]
                t_train_batch = correct_action[index]

                y_train_batch = self.cnn(x_train_batch)

                loss_train_batch = F.softmax_cross_entropy(y_train_batch, t_train_batch)
                accuracy_train_batch = F.accuracy(y_train_batch, t_train_batch)

                loss_list.append(loss_train_batch.array)
                accuracy_list.append(accuracy_train_batch.array)

                self.cnn.cleargrads()
                loss_train_batch.backward()

                optimizer.update()

                iteration += 1

            loss_train = np.mean(loss_list)
            accuracy_train = np.mean(accuracy_list)

            with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
                y_val = self.cnn(x_val)

            loss_val = F.softmax_cross_entropy(y_val, t_val)
            accuracy_val = F.accuracy(y_val, t_val)

            print('epoch: {}, iteration: {}, loss (train): {:.4f}, loss (valid): {:.4f}'.format(
            epoch, iteration, loss_train, loss_val.array))

            results_train['loss'] .append(loss_train)
            results_train['accuracy'] .append(accuracy_train)
            results_valid['loss'].append(loss_val.array)
            results_valid['accuracy'].append(accuracy_val.array)
            chainer.serializers.save_npz('my_iris.net', self.cnn)

            self.n_action = y_val

        return self.action

#	def act(self, obs):
#		with chainer.using_config('train', False), chainer.using_config('enable_backprop', False);

if __name__ == '__main__':
        dl = deep_learning()
