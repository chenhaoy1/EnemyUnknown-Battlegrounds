
import numpy as np
from builtins import range
import MalmoPython
import os
import sys
import time
import json
import agent

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

def position(num):
    positions = []
    for i in range(num):
        x = np.random.randint(-19,19)
        z = np.random.randint(-19,19)
        positions.append((x, z))
    return positions

def ground():
    return '''<DrawCuboid x1="-20" y1="226" z1="-20" x2="20" y2="226" z2="20" type="stone"/>
              <DrawCuboid x1="-20" y1="227" z1="-20" x2="20" y2="227" z2="-20" type="beacon"/>
              <DrawCuboid x1="20" y1="227" z1="-20" x2="20" y2="227" z2="20" type="beacon"/>
              <DrawCuboid x1="20" y1="227" z1="20" x2="-20" y2="227" z2="20" type="beacon"/>
              <DrawCuboid x1="-20" y1="227" z1="20" x2="-20" y2="227" z2="-20" type="beacon"/>
              <DrawCuboid x1="-20" y1="228" z1="-20" x2="20" y2="249" z2="-20" type="stone"/>
              <DrawCuboid x1="20" y1="228" z1="-20" x2="20" y2="249" z2="20" type="stone"/>
              <DrawCuboid x1="20" y1="228" z1="20" x2="-20" y2="249" z2="20" type="stone"/>
              <DrawCuboid x1="-20" y1="228" z1="20" x2="-20" y2="249" z2="-20" type="stone"/>
              <DrawCuboid x1="-20" y1="250" z1="-20" x2="20" y2="250" z2="20" type="beacon"/>'''


def trap(positions):
    traps = ""
    for p in positions:
        traps += '<DrawBlock x="' + str(p[0]) + '" y="226" z="' + str(p[1]) + '" type="lava" />'
    return traps

def monster(positions):
    monster_pool=['Zombie','Pig']
    monsters = ""
    count = 1
    index = 0
    for p in positions:
        monster = monster_pool[index]
        monsters += '<DrawEntity x="' + str(p[0]) + '" y="227" z="' + str(p[1]) + '" type="' + monster + '" />'
        if(count%3==0):
           index += 1
        count += 1
    return monsters

    

def GetMissionXML():
    positions1 = position(10)
    positions2 = position(5)
    print(positions1)
    print(positions2)
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                   <Time>
                      <StartTime>17000</StartTime>
                      <AllowPassageOfTime>false</AllowPassageOfTime>
                   </Time>
                   <Weather>clear</Weather>
                   <AllowSpawning>false</AllowSpawning>
                </ServerInitialCondition>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
                  <DrawingDecorator>
                     <DrawCuboid x1="-19" y1="226" z1="-19" x2="19" y2="240" z2="19" type="air"/>
                     '''+ground()+'''
                     '''+trap(positions1)+'''
                     '''+monster(positions2)+'''
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>sbplayer</Name>
                <AgentStart>
                   <Placement x="-0" y="227.0" z="-0" yaw="0"/>
                   <Inventory>
                      <InventoryItem slot="0" type="diamond_sword"/>
                   </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <MissionQuitCommands/>
                  <ObservationFromNearbyEntities>
                     <Range name="entities" xrange="12" yrange="2" zrange="12"/>
                  </ObservationFromNearbyEntities>
                  <ObservationFromGrid>
                     <Grid name="floor3x3">
                       <min x = "-1" y="-1" z="-1"/>
                       <max x = "1" y="-1" z = "1"/>
                     </Grid>
                  </ObservationFromGrid>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


# Create default Malmo objects:
if __name__=='__main__':
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
    num=0
    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print('ERROR:',e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)
    sur = agent.player();
    num_reps = 3000
    for iRepeat in range(num_reps):
        start = time.time()
        print(iRepeat,'start')
        my_mission = MalmoPython.MissionSpec(GetMissionXML(),True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        max_retries = 3
        for retry in range(max_retries):
            try:
               agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "sbplayer")
               break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission", e)
                    print("Is the game running?")
                    exit(1)
                else:
                    time.sleep(2)

        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
        if(iRepeat+1)%5==0:
           sur.best_move(agent_host)
        else:
           sur.run(agent_host)
        #while world_state.is_mission_running:
         #   world_state = agent_host.getWorldState()
          #  s = sur.get_current_state(agent_host)
           # pm = sur.get_possible_move(agent_host)
           # move = sur.choose_move('try',pm,1)
           # sur.act(agent_host,move)
           # print(s)   
        end = time.time()-start
        print('alive time =',end)
        if(iRepeat+1)%5==0:
            f=open("test3.txt",'a')
            print(num,end,file=f)
            f.close()
            num += 1
        print('running...')
        time.sleep(3)
