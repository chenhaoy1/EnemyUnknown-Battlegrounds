---
layout: default
title: Status
---

Project Summary: 
Our agent in this submission is a prototype of our final agent. The agent should survive in the world as long as possible by learning to avoid enemies’ attacks. If attacked, the agent’s health points will be deducted and it will die and quit immediately when its health points reaches 0. Our goal is make our agent survive in a random world longer by integrating q learning algorithm in its learning part.


Remaining Goals and Challenges: 

Our remaining goal is to make our agent more intelligent. To achieve this goal, our algorithm should be improved still. We plan to add the deep q learning algorithm to the learning part, which would perform better for larger state space and unknown transition probabilities. The most challenging part for our team right now is how to integrate this algorithm correctly in our current code. We need to add a linear function as our value function to q_table. The neural network also could be considered in order to solve more complicated situation.

Our next goal is to add pigs into the world, which can be exploited to increase our health points by eliminating them. It is also challenging to integrate this action and reward to our algorithm. We will evaluate this action later.
We might use some similar pseudo code of deep q learning into our later modification.


Resources Used:

1.The resource used for deep q learning tutorial: https://sergioskar.github.io/Deep_Q_Learning/
2.The simple reinforcement learning tutorial: https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0
