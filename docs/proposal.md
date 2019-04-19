---
layout: default 
title: Proposal
---

## Project Summary

We plan to develop and implement an AI model, which can survive as long as possible in its world, while its world has different enemies, such as cave spiders, Magma Cube and Vindicators. The main objective would focus on eliminating more monsters with less damage on its health. In order to reach this objective, the agent may find any materials in its world and produce weapons to kill the enemies and defend itself. Besides, in order to maintain its life, the agent may hunt for preys to gain meat and recover a certain health points.

The input should be the agent's nearby environment, which would be represented as a grid map. The output should be a tuple of state and actions,which includes the agent's current state and one or more actions for agent to implement.



## AI/ML Algorithms 

Dijkstra algorithm wll be used as AI algorithm. We also will use Q-learning to train the agent get the max rewards, as well as decision tree and random forests. For further, we may explore more useful algorithm.

## Evaluation Plans 

We plan to evaluate our agent based on two categories: quantitatively and qualitatively. 

For the quantitative category, we have some metrics to evaluate the final result. The first one is N, the number of different monster eliminated during the whole game. The second one is S, the score of different types of monsters gained by killing it. The third one is the total time the agent stays alive.We will give the agent 8 mins to train himself before we star the game. 

For the qualitative category, we have a formula to measure the AI model's preformance. The Performance qualitative score should be W1*Sum(Ni*Si) + W2*T.(the weights for each metric will be determined later)





## Instructor Appointment

Our meeting time is: 01:45pm - 2:00pm Thursday, April 25, 2019
The meeting place is: DBH 4204
