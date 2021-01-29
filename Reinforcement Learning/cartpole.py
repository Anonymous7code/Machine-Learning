# -*- coding: utf-8 -*-
"""CartPole

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MFfa7RMDtW5DhTq6vaKV324zurSJmpJs

# Importing Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import gym
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

"""# Setting up the display"""

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython: from IPython import display

"""# Deep Q-Network"""

class DQN(nn.Module):       # Module is the base class for all NN modules
    def __init__(self, img_height, img_width):      # The module recieves the screenshot of the images as input
        super().__init__()

        # The Network here contains only 2 Fully Connected layers and the output layer
        self.fc1 = nn.Linear(in_features=img_height*img_width*3, out_features=24)   
        self.fc2 = nn.Linear(in_features=24, out_features=32)
        self.out = nn.Linear(in_features=32, out_features=2)
    
    def forward(self, t):
        t = t.flatten(start_dim=1)
        t = F.relu(self.fc1(t))
        t = F.relu(self.fc2(t))
        t = self.out(t)
        return t

"""# Experience Class"""

Experience = namedtuple(
    'Experience',
    ('state','action','reward','next_state')
)

"""# Replay Memory class"""

class ReplayMemory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0
    
    # Pushing the Experience in memory Stack
    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.push_count % self.capacity] = experience   # Overwriting the very first experience
        self.push_count += 1

    # Returns Random sample of batch_size
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    # Allows to check weather we can retrive sample from the memory; are there sufficient samples present in memory
    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size

"""# Epsilon Greedy Stratagy"""

class EpsilonGreedyStrategy():
    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * \
            math.exp(-1. * current_step * self.decay)

"""# RL Agent

"""

class Agent():
    def __init__(self, strategy, num_actions, device):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions          # Available action for agent Here 2 --> Left and Right 
        self.device = device
    
    def select_action(self, state, policy_net):
        rate = self.strategy.get_exploration_rate(self.current_step)
        self.current_step += 1

        if rate > random.random():
            action = random.randrange(self.num_actions)
            return torch.tensor([action]).to(self.device) # explore      
        else:
            with torch.no_grad():
                return policy_net(state).argmax(dim=1).to(self.device) # exploit

"""# Environment Manager"""

class CartPoleEnvManager():
    def __inti__(self,device):
        self.device = device
        self.env = gym.make('CartPole-v0').unwrapped # Calling unwrapped gives the behind the scene dynamics that are not avaialbe otherwise
        self.env.reset()
        self.current_screen =None # This render the current screen of the env but when None denotes that it's an initial observation
        self.done = False

    # Now below are the reset render and close function with gym module reset render and close functions
    def close(self):
        self.env.close()
    def reset(self):
        self.env.reset()
        self.current_screen = None      # Setting screen for next episode for initial observation
    def render(self,mode='human'):
        return self.env.render(mode)

    def num_actions_available(self):
        return self.env.action_space.n

    def take_action(self,action):
        _, reward,self.done, _ = self.env.step(action.item())   # Since we only need reward and self.done here
                                                                # And the action passed to the function is tensor 
                                                                # therefore we pass action.item() as it returns a standard python number
        return torch.tensor([reward], device=self.device)
    
    def just_starting(self):
        return self.current_screen is None

    # This function returns the environment in form of processed image of the screen
    def get_state(self):
        if self.just_starting() or self.done:
            self.current_screen = self.get_processed_screen()      # If we are not starting we convert that in black screen
            black_screen = torch.zeros_like(self.current_screen)   # torch.zeros_like() converts into black screen of size current_screen
            return black_screen

        else:
            s1 = self.current_screen
            s2 = self.get_processed_screen()
            self.current_screen = s2
            return s2 - s1
        
    def get_screen_height(self):
        screen = self.get_processed_screen()
        return screen.shape[2]

    def get_screen_height(self):
        screen = self.get_processed_screen()
        return screen.shape[3]

    def get_processed_screen(self):
        screen = self.render('rgb_array').transpose((2,0,1)) #Transpose of rgb_array as height width 
        screen = self.crop_screen(screen)
        return self.transform_screen_data(screen)

    def crop_screen(self,screen):
        screen_height = screen.shape[1]

        # Striping Off top and Bottom
        top = int(screen_height * 0.4)
        bottom = int(screen_height * 0.8)
        screen = screen[:,top:bottom,:]
        return screen

    def transform_screen_data(self,screen):
        #Convert to float, rescale, convert to tensor
        screen = np.ascontiguousarray(screen,dtype=np.float32) /255
        screen = torch.from_numpy(screen)   #Now we convert the numpy array into pytorch tensor

        # Using torchvision package to compare image transforms
        resize = T.Compose([                                    # This is done to chain together several transformations
                            T.ToPILImage(),                     # Passed tensor is converted into PIL image
                            T.Resize((40,90)),                  # Then resized to (40,90)
                            T.ToTensor()                        # Then again converted to tensor
        ])
        return resize(screen).unsqueeze(0).to(self.device)      # add a batch dimension (BCHW)
                                                                # unsqueeze adds an extra dimmension to the image which
                                                                # represents batch dimmnession since the processed images
                                                                # will be passed into batches in DQN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
em = CartPoleEnvManager()
em.reset
screen = em.render('rgb_array')

plt.figure()
plt.imshow(screen)
plt.title('Non-processed screen example')
plt.show()

em.reset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
em = CartPoleEnvManager(device)
em.reset()
screen = em.render('rgb_array')

plt.figure()
plt.imshow(screen)
plt.title('Non-processed screen example')
plt.show()



"""#Non-Processed Screen"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
em = CartPoleEnvManager()
em.reset
screen = em.render('rgb_array')

plt.figure()
plt.imshow(screen)
plt.title('Non-processed screen example')
plt.show()

"""#Processed Screen"""

screen = em.get_processed_screen()

plt.figure()
plt.imshow(screen.squeeze(0).permute(1, 2, 0).cpu(), interpolation='none')
plt.title('Processed screen example')
plt.show()

"""Starting State"""

screen = em.get_state()

plt.figure()
plt.imshow(screen.squeeze(0).permute(1, 2, 0).cpu(), interpolation='none')
plt.title('Starting state example')
plt.show()

"""Non-Starting State"""

for i in range(5):
    em.take_action(torch.tensor([1]))
screen = em.get_state()

plt.figure()
plt.imshow(screen.squeeze(0).permute(1, 2, 0).cpu(), interpolation='none')
plt.title('Non starting state example')
plt.show()

"""Ending State"""

em.done = True
screen = em.get_state()

plt.figure()
plt.imshow(screen.squeeze(0).permute(1, 2, 0).cpu(), interpolation='none')
plt.title('Ending state example')
plt.show()
em.close()

"""Utility Functions"""

def plot(values, moving_avg_period):
    plt.figure(2)
    plt.clf()        
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(values)
    plt.plot(get_moving_average(moving_avg_period, values))
    plt.pause(0.001)
    if is_ipython: display.clear_output(wait=True)
def get_moving_average(period, values):
    values = torch.tensor(values, dtype=torch.float)
    if len(values) >= period:
        moving_avg = values.unfold(dimension=0, size=period, step=1) \
            .mean(dim=1).flatten(start_dim=0)
        moving_avg = torch.cat((torch.zeros(period-1), moving_avg))
        return moving_avg.numpy()
    else:
        moving_avg = torch.zeros(len(values))
        return moving_avg.numpy()

# Example Plot
plot(np.random.rand(300), 100)

"""# Hyperparameters"""

batch_size = 256
gamma = 0.999
eps_start = 1
eps_end = 0.01
eps_decay = 0.001
target_update = 10
memory_size = 100000
lr = 0.001
num_episodes = 1000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

em = CartPoleEnvManager(device)
strategy = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
agent = Agent(strategy, em.num_actions_available(), device)
memory = ReplayMemory(memory_size)

policy_net = DQN(em.get_screen_height(), em.get_screen_width()).to(device)
target_net = DQN(em.get_screen_height(), em.get_screen_width()).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(params=policy_net.parameters(), lr=lr)

"""#Training Loop"""

episode_durations = []
for episode in range(num_episodes):
    em.reset()
    state = em.get_state()
    for timestep in count():
        action = agent.select_action(state, policy_net)
        reward = em.take_action(action)
        next_state = em.get_state()
        memory.push(Experience(state, action, next_state, reward))
        state = next_state

        if memory.can_provide_sample(batch_size):
            experiences = memory.sample(batch_size)
            states, actions, rewards, next_states = extract_tensors(experiences)

            current_q_values = QValues.get_current(policy_net, states, actions)
            next_q_values = QValues.get_next(target_net, next_states)
            target_q_values = (next_q_values * gamma) + rewards

            loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if em.done:
            episode_durations.append(timestep)
            plot(episode_durations, 100)
            break
em.close()

"""Tensor Processing"""

def extract_tensors(experiences):
    # Convert batch of Experiences to Experience of batches
    batch = Experience(*zip(*experiences))

    t1 = torch.cat(batch.state)
    t2 = torch.cat(batch.action)
    t3 = torch.cat(batch.reward)
    t4 = torch.cat(batch.next_state)

    return (t1,t2,t3,t4)

e1 = Experience(1,1,1,1)
e2 = Experience(2,2,2,2)
e3 = Experience(3,3,3,3)

experiences = [e1,e2,e3]
experiences

batch = Experience(*zip(*experiences))
batch

"""#Calculating Q-Values"""

class QValues():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def get_current(policy_net, states, actions):
        return policy_net(states).gather(dim=1, index=actions.unsqueeze(-1))

    @staticmethod        
    def get_next(target_net, next_states):                
        final_state_locations = next_states.flatten(start_dim=1) \
            .max(dim=1)[0].eq(0).type(torch.bool)
        non_final_state_locations = (final_state_locations == False)
        non_final_states = next_states[non_final_state_locations]
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size).to(QValues.device)
        values[non_final_state_locations] = target_net(non_final_states).max(dim=1)[0].detach()
        return values

"""#Update To Plot"""

def plot(values, moving_avg_period):
    plt.figure(2)
    plt.clf()        
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(values)

    moving_avg = get_moving_average(moving_avg_period, values)
    plt.plot(moving_avg)    
    plt.pause(0.001)
    print("Episode", len(values), "\n", \
        moving_avg_period, "episode moving avg:", moving_avg[-1])
    if is_ipython: display.clear_output(wait=True)

plot(np.random.rand(300), 100)