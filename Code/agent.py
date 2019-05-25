import numpy as np

import MalmoPython
import os
import random 
import sys
import time
import json 
import random
import math
import errno
import assignment2_submission as submission
from collections import defaultdict, deque
from timeit import default_timer as timer

class player(object):
    def __init__(self,alpha=0.3,gamma=1,n=1):
       self.epsilon = 0.3
       self.n, self.alpha,self.gamma = n, alpha, gamma
       self.entities = {}
       self.q_table = {}


    def _get_entities_position(self,agent_host):
        while True:
          world_state = agent_host.getWorldState()
          if world_state.number_of_observations_since_last_state > 0:
              msg = world_state.observations[-1].text
              ob = json.loads(msg)
              n=0
              m=0
              nearyby_obs={}
              nearyby_obs['mon']={}
              #print(ob)
              for ent in ob['entities']:
                if(ent['name']=='sbplayer' or ent['name']=='Pig'):
                  if(ent['name'] in nearyby_obs.keys()):
                      name = ent['name']+str(n)
                      n += 1
                  else:
                      name = ent['name']
                  nearyby_obs[name] = (ent['x'], ent['z'])
                else:
                  name = ent['name']+str(m)
                  nearyby_obs['mon'][name] = (ent['x'], ent['z'])
                  m += 1
              nearyby_obs['nearblock'] = ob['floor3x3']
              nearyby_obs['life']=ob['Life']
              return nearyby_obs


    def actions(self,agent_host,act):
      if(act=='forward'):
        agent_host.sendCommand("setYaw 0")
        agent_host.sendCommand("strafe 0")
        agent_host.sendCommand("move 1")
        
      elif(act=='backward'):
        agent_host.sendCommand("setYaw 0")
        agent_host.sendCommand("strafe 0")
        agent_host.sendCommand("move -1")
     
      elif(act=='left'):
        agent_host.sendCommand("setYaw 0")
        agent_host.sendCommand("move 0")
        agent_host.sendCommand("strafe -1")

      elif(act=='right'):
        agent_host.sendCommand("setYaw 0")
        agent_host.sendCommand("move 0")
        agent_host.sendCommand("strafe 1")


    def get_curr_state(self,agent_host):
      state_matrix = self._get_entities_position(agent_host)
      cur_state = []
      if(state_matrix['life']==20):
         cur_state.append(2)
      elif(state_matrix['life']==0):
         cur_state=[0,(-1,-1),(-1,-1)]
         return tuple(cur_state)
      elif(state_matrix['life']<20 and state_matrix['life']!=0):
         cur_state.append(1)
      x0 = state_matrix['sbplayer'][0]
      z0 = state_matrix['sbplayer'][1]
      #print('player',x0,z0)
      mon_dic = {}
      for name,info in state_matrix['mon'].items():
        x1 = info[0]
        z1 = info[1]
        x = x1-x0
        y = z1-z0
        dis = np.sqrt(pow(abs(x),2)+pow(abs(y),2))
        if(dis<=8):
          d = 1;
        else:
          d = 0

        p=-1
        if(x>0 and y>0 and y/x>=1):
          p = 0
        elif(x>0 and y>0 and y/x<1):
          p = 7
        elif(x>0 and y<0  and y/x>=-1):
          p = 6
        elif(x>0 and y<0 and y/x<-1):
          p = 5
        elif(x<0 and y>0 and y/x<=-1):
          p = 1
        elif(x<0 and y>0 and y/x>-1):
          p = 2
        elif(x<0 and y<0 and y/x<=1):
          p = 3
        elif(x<0 and y <0 and y/x>1):
          p =4
        mon_dic[name] = (dis,d,p)
      mon_dic = sorted(mon_dic.items(),key=lambda x:x[1][0])
      a = (-1,-1)
      b = (-1,-1)
      if(len(mon_dic)==1):
        a1 = mon_dic[0][1]
        a = (a1[1],a1[2])
      elif(len(mon_dic)>=2):
        a1 = mon_dic[0][1]
        a = (a1[1],a1[2])
        b1 = mon_dic[1][1]
        b = ((b1[1],b1[2]))
      cur_state.append(a)
      cur_state.append(b)
      return tuple(cur_state)
    

    def get_possible_move(self,agent_host):
      action_list = []
      state_matrix = self._get_entities_position(agent_host)
      #print(state_matrix)
      player = state_matrix['sbplayer']
      blocks = state_matrix['nearblock']
      if(player[0]<19 and blocks[5]!='lava'):
        action_list.append('left')
      if(player[0]>-19 and blocks[3]!='lava'):
        action_list.append('right')
      if(player[1]<19 and blocks[7]!='lava'):
        action_list.append('forward')
      if(player[1]>-19 and blocks[1]!='lava'):
        action_list.append('backward')
      return action_list


    def act(self,agent_host,action):
      self.actions(agent_host,action)
  

    def choose_move(self,c_state,pm,eps):
      if c_state not in self.q_table:
         self.q_table[c_state] = {}
         for action in pm:
            if action not in self.q_table[c_state]:
               self.q_table[c_state][action] = 0

      rnd = random.random()
      if(rnd<=eps):
        a = random.randint(0,len(pm)-1)
        return pm[a]

      else:
        max_list = []
        act_reward = sorted(self.q_table[c_state].items(),key=lambda x:x[1],reverse = True)
        maxa =  act_reward[0][1]
        for item in act_reward:

            if item[1] == maxa:
               max_list.append(item[0])
        a = random.randint(0,len(max_list)-1)
        return max_list[a]

    def best_move(self,agent_host):
        curr_r = 0 
        curr_state = self.get_curr_state(agent_host)
        while(curr_state[0]!=0):
           pm = self.get_possible_move(agent_host)
           move = self.choose_move(curr_state,pm,-1)
           self.act(agent_host,move)
           curr_state = self.get_curr_state(agent_host)
           if(curr_state[0]==0):
             curr_r=-1000
             print('reward',curr_r)
             break
           else:
             if(curr_state[0]==1):
                curr_r=curr_r-50
             for y in range(1,3):
                if(curr_state[y][0]==0):
                  curr_r = curr_r-10
                elif(curr_state[y][0]==1):
                  curr_r = curr_r-50
        print('best policy for now')

    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.

        Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
        """
        print(S,A,R)
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        print(G) 
        if tau + self.n < T:
            try:
               G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
            except:
               pass
        if(curr_s not in self.q_table):
           self.q_table[curr_s] = {}
        if(curr_a not in self.q_table[curr_s]):
           self.q_table[curr_s][curr_a] = 0
        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def run(self, agent_host):
        print(len(self.q_table))
        """Learns the process to compile the best gift for dad. """
        S, A, R = deque(), deque(), deque()
        present_reward = 0
        done_update = False

        reward = 0
        while not done_update:
            s0 = self.get_curr_state(agent_host)
            possible_actions = self.get_possible_move(agent_host)
            a0 = self.choose_move(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)

            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.1)
                if t < T:
                    current_r = 0
                    self.act(agent_host,A[-1])
                    temp_s = self.get_curr_state(agent_host)
                    #print(temp_s[0])
                    if(temp_s[0]==0):
                      current_r=-1000
                      time.sleep(1)
                    elif(temp_s[0]==1):
                      current_r=current_r-50
                    elif(temp_s[0]==2):
                      current_r=current_r+50

                    for y in range(1,3):
                       if(temp_s[y][0]==0):
                         current_r = current_r+50
                       elif(temp_s[y][0]==1):
                            current_r = current_r-50
                    R.append(current_r)

                    if(temp_s[0]==0):
                        # Terminating state
                        agent_host.sendCommand('quit')
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                        print("Reward:", present_reward)
                    else:
                        #s = self.get_curr_state(agent_host)
                        S.append(temp_s)
                        possible_actions = self.get_possible_move(agent_host)
                        next_a = self.choose_move(temp_s, possible_actions, self.epsilon)
                        A.append(next_a)

                tau = t - self.n + 1
                if tau >= 0:
                    #print('update')
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

