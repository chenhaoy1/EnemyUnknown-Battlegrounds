---
layout: default
title: Status
---
Remaining Goals and Challenges: 
Our remaining goal is to make our agent more intelligent. 
To achieve this goal, our algorithm should be improved still. We plan to add the deep q learning algorithm to the evaluation part, which would perform better for larger state space and unknown transition probabilities. The most challenging part for our team right now is how to integrate this algorithm correctly in our current code. We need to add a linear function as our value function instead of using q-table. The neural network also could be considered in order to solve more complicated situation.
Our next goal is to add pigs into the world, which can be exploited to increase our health points by eliminating them. It is also challenging to integrate this action and reward to our algorithm. We will evaluate this action later.
We might use some pseudo code of deep q learning into our later modification.
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

   def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    #get action
    def act(self, state):
        #select random action with prob=epsilon else action=maxQ
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0]) 
=>Experience Replay
The resource for deep q learning tutorial: 
https://sergioskar.github.io/Deep_Q_Learning/
https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0
