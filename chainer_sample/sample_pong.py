import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import gym
import numpy as np
import datetime
from skimage.color import rgb2gray
from skimage.transform import resize
#import csv

env = gym.make('Pong-v0')
obs = env.reset()
env.render()

class QFunction(chainer.Chain):
    def __init__(self, n_history=4, n_action=6):
        initializer = chainer.initializers.HeNormal()
        super(QFunction, self).__init__(
            l1=L.Convolution2D(n_history, 32, ksize=8, stride=4, nobias=False, initialW=initializer),
            l2=L.Convolution2D(32, 64, ksize=4, stride=2, nobias=False, initialW=initializer),
            l3=L.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, initialW=initializer),
            l4=L.Linear(2304, 512, initialW=initializer),
            out=L.Linear(512, n_action, initialW=np.zeros((n_action, 512), dtype=np.float32))
        )

    def __call__(self, x, test=False):
        s = chainer.Variable(x)
        h1 = F.relu(self.l1(s))
        h2 = F.relu(self.l2(h1))
        h3 = F.relu(self.l3(h2))
        h4 = F.relu(self.l4(h3))
        h5 = self.out(h4)
        return chainerrl.action_value.DiscreteActionValue(h5)

n_action = env.action_space.n
n_history=4
q_func = QFunction(n_history, n_action)
#q_func.to_gpu()

optimizer = chainer.optimizers.Adam(eps=1e-2)
#optimizer = chainer.optimizers.RMSpropGraves(lr=0.00025, alpha=0.95, momentum=0.95, eps=0.0001)
optimizer.setup(q_func)

gamma = 0.99

explorer = chainerrl.explorers.ConstantEpsilonGreedy(
    epsilon=0.3, random_action_func=env.action_space.sample)

replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10**5)

phi = lambda x: x.astype(np.float32, copy=False)

agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    minibatch_size=32, replay_start_size=100, update_interval=1,
    target_update_interval=10**4, phi=phi)

last_time = datetime.datetime.now()
n_episodes = 10000
#state = np.zeros([4,80,80])
for i in range(1, n_episodes + 1):
    state = np.zeros([4,80,80], dtype=np.float32)
    obs = resize(rgb2gray(env.reset()),(80,80),mode='constant')
#    obs = obs[np.newaxis, :, :]

    reward = 0
    done = False
    R = 0

    while not done:
        env.render()
        print(state)
        action = agent.act_and_train(state, reward)
        obs, reward, done, _ = env.step(action)
        obs = resize(rgb2gray(obs), (80, 80), mode='constant')
        state = np.asanyarray([state[1], state[2], state[3], obs], dtype=np.float32)
#        with open('file.csv', 'wt') as f:
#            writer = csv.writer(f)
#            writer.writerows(state[1])
#        obs = obs[np.newaxis, :, :]

        if reward != 0:
            R += reward

    elapsed_time = datetime.datetime.now() - last_time
    print('episode:', i, '/', n_episodes,
          'reward:', R,
          'minutes:', elapsed_time.seconds/60)
    last_time = datetime.datetime.now()

    if i % 100 == 0:
        filename = 'agent_Breakout' + str(i)
        agent.save(filename)

    agent.stop_episode_and_train(state, reward, done)
print('Finished.')
