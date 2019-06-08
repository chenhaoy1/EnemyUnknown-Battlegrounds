---
layout: default
title: Final
---

## Project Summary:

As its name suggest, our project idea is inspired by the most polular vedio game PlayerUnknown's Battlegrouds. The goal of this project is to have an agent to survive in the 40x40 flat ground with three enemies(zombies), two pigs, and ten traps spawned randomly in the environment. The agent should survive as long as possible to escape from the acttack of zombies or to kill pigs to increase its health points. The picture below for reference:
<div align="center">
<img src="9.png" width="50%">
</div>


As for the challenges, we have lots of possible states should be defined in the 40x40 environment. Also, the agent has five actions should be taken into consideration. In the trainning process, the agent should learn to avoid enemies' attacks and make some predictions according to their moves. After trainning the agent, the agent can intelligently avoid the enemies attacks and even attack them to protect itself - this is where we use an AL/ML algorithm. We mainly use reinforcement learning for problem, and we focus on Q-learning in this project.

This project is non-trivial because it is a brand-new experience for us to a create something original program developing from nothing. We implement the most decent algorithm to solve the problem by searching lots of resources online. It is also a kind of process for us to learn new knowledge as a team by communicating, cooperating, and integrating different opinions to reach unanimity. 

## Approaches

We have 3 enemies(zombies), 2 pigs and 10 traps spawn randomly in a 40X40 flat ground. The agent has 5 actions (left, right, forward, backward, attack) and the agent should try to escape from zombies as far as possible to survive in the environment. It can also kill pigs to increase its health point and survival time in the world. 

### Algorithm
And our basic algorithm idea is from CS 175 classes. We decision to use Q-learning algorithm to solve the problem. The Q-learning algorithm's logic is quite similar to the pseudo code given below. The Q-learning algorithm will choose the action with the highest Q-value for each state. The Q-value is calculated based on our defined rewards resulting from a state. The constant α(alpha), γ(gamma), ε(epsilon), and n(backsteps) were used to trim the algorihm and improve the performance.
<div align="center">
<img src="Pseudocode.jpg" width="50%">
<img src="Pseudocode1.jpg" width="50%">
</div>

First of all, the agent with its current state will get a list of possible actions and choose a move by implementing ε-Greedy Policy. Instead, The agent returns a random action with probability eps, but with (1-eps) it picks the action with the highest Q-value. The code below perform the above description.

<div align="center">
<img src="10.jpg" width="50%">
</div>

After every move of our agent, the agent will get a current state and store the privous state. There are states we have. The first one is our health points, the second  and third one is the relative distance of the closest two enemies surrounding the agent. The health points of 0 means the agent dies and reward is -1000. 1 means half alive and the reward is -50. 2 means full alive and the reward is +50. The distance value of 0 means greater distance between the agent and the enemy and the reward is +50. The distance value of 1 means closer distance and reward is -50. The agent will always compute the total reward it gains by checking its current state and it stores current and next status, action, reward for upating q-table. If agent find its health points reach 0, it will return the final reward to the terminal and quit the game immediately without continuing any afterward steps. If it is still alive, the agent will continue to find the next action and act. The code below perform the above description.

<img src="2.jpg" width="50%">
<img src="3.jpg" width="50%">

The agent will deal with the current reward after getting into each move. The agent will update the q_table, which we stores the table as one of our agent. The basic logic of the implementation of updating q_table is Bellman equation provided during the lectures. The equation looks like this: Q(s,a) <- Q(s,a)+alpha(r+y(maxQ(s',a')-Q(s,a))). According to the tutorial online, the formula means “the expected long-term reward for a given action is equal to the immediate reward from the current action combined with the expected reward from the best future action taken at the following state.”
The code below perform the above description.

<img src="4.jpg" width="50%">

### State Space
<img src="8.png" width="50%">
From the picture draw above, we use the tangent calculated by the agent position and the enemy's postion to detect the nearby enemies. In the circle with radius 2, the agent can attack to kill a pig to increase its health points, and the reward is (). The agent can also detect the enemies in the circle with radius 8. There are 8 different areas which seperated by tangent. In these areas, the agent can try to escape from the enemies as far as possible with a reward (). 
