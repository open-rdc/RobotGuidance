import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import gym
import numpy as np
import datetime
from skimage.color import rgb2gray
from skimage.transform import resize

env = gym.make('Pong-v0')
obs = env.reset()
env.render()

class QFunction(chainer.Chain):
    def __init__(self, n_history=1, n_action=6):
        initializer = chainer.initializers.HeNormal()
        super().__init__(
            l1=L.Convolution2D(n_history, 32, ksize=8, stride=4, nobias=False, initialW=initializer),
            l2=L.Convolution2D(32, 64, ksize=3, stride=2, nobias=False, initialW=initializer),
            l3=L.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, initialW=initializer),
            l4=L.Linear(3136, 512, initialW=initializer),
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
n_history=1
q_func = QFunction(n_history, n_action)

optimizer = chainer.optimizers.Adam(eps=1e-2)
optimizer.setup(q_func)

gamma = 0.95

explorer = chainerrl.explorers.ConstantEpsilonGreedy(
    epsilon=0.3, random_action_func=env.action_space.sample)

replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 4)

phi = lambda x: x.astype(np.float32, copy=False)

agent = chainerrl.agents.DoubleDQN(
    q_func, optimizer, replay_buffer, gamma, explorer,
    minibatch_size=4, replay_start_size=500, update_interval=1,
    target_update_interval=100, phi=phi)

last_time = datetime.datetime.now()
n_episodes = 1000
for i in range(1, n_episodes + 1):
    obs = resize(rgb2gray(env.reset()),(80,80))
    obs = obs[np.newaxis, :, :]

    reward = 0
    done = False
    R = 0

    while not done:
        env.render()
        action = agent.act_and_train(obs, reward)
        obs, reward, done, _ = env.step(action)
        obs = resize(rgb2gray(obs), (80, 80))
        obs = obs[np.newaxis, :, :]

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

    agent.stop_episode_and_train(obs, reward, done)
print('Finished.')
