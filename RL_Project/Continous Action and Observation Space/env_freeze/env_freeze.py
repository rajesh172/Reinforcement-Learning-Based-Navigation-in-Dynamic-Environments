import gym
import pygame
import numpy as np
import math

class AgentEnv(gym.Env):
    def __init__(self):  
        ##super(AgentEnv, self).__init__()      
        pygame.init()
        pygame.font.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = 500   # frame per second
        self.grid_size = 40
        #self.grid_width = self.width//self.grid_size ## no. of grids in row
        #self.grid_height = self.height//self.grid_size  ## no. of grids in column
        self.count = 0
        self.action_space = gym.spaces.Box(-30,30, shape=(2,), dtype=np.float32)
        self.action = 0
        # self.reward = 0
        
    
        #self.action_space = self.action_space2.sample()
        ## self.observation_space = gym.spaces.Tuple((gym.spaces.Discrete(self.grid_width),gym.spaces.Discrete(self.grid_height)))
        self.observation_space = gym.spaces.Box(np.array([0,0,0,0]),np.array([self.width-50,self.height-50,self.width-50,self.height-50]))
        
        self.agent_image = pygame.image.load('TANK.png')
        self.agent_image = pygame.transform.scale(self.agent_image,(self.grid_size ,self.grid_size))
        self.player_image = pygame.transform.rotate(self.agent_image, 0)
        self.player = self.player_image.get_rect()
        self.player_pos = [30, 30]
        
        self.target_pos = [600, 400]
        self.target_image = pygame.Rect(self.target_pos[0],self.target_pos[1],self.grid_size,self.grid_size)
        
        self.obstacle1_pos = [400, 300]
        self.obstacle1_image = pygame.Rect(self.obstacle1_pos[0],self.obstacle1_pos[1],self.grid_size,self.grid_size)
        ## self.target_angle = math.degrees(math.atan(abs(self.target_pos[1]-self.player_pos[1]))/abs(self.target_pos[0]-self.player_pos[0]))
    def step(self,action):        
        #if action >= 0:
        # self.action = action
        
        if self.player_pos[0]+action[0]>=0 and self.player_pos[0]+action[0]<=760 and self.player_pos[1]+action[1]>=0 and self.player_pos[1]+action[1]<=560 : 
            self.player_pos[0] += action[0]
            self.player_pos[1] += action[1]
            self.reward = -np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)*0.01
        
            if self.player.colliderect(self.target_image):
                self.reward +=20000
                done = True

            elif self.player.colliderect(self.obstacle1_image):
                self.reward -= 10000
                done = True
            else:
                self.reward -= 1
                done = False
        
        else:
            # if self.player_pos[0]+action[0]<0:
            #     self.player_pos[0]=0
            # if self.player_pos[0]+action[0]>760:
            #     self.player_pos[0]=760
            # if self.player_pos[1]+action[1]<0:
            #     self.player_pos[1]=0
            # if self.player_pos[1]+action[1]>560:
            #     self.player_pos[1]=560

            self.reward -= 10
            self.reward -= np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)*0.01
    
            done = False
            
            
            #apply something here
        # elif action < 0: 
        #     self.player_pos[0] -= int(action)*math.cos(math.radians(self.target_angle))
        #     self.player_pos[1] -= int(action)*math.sin(math.radians(self.target_angle))
        #     reward = -np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)
        # elif action == 2:  # left
        #     self.player_pos[0] = max(0, self.player_pos[0] - 1)
        #     reward = -np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)
        # elif action == 3:  # right
        #     self.player_pos[0] = min(self.grid_width - 1, self.player_pos[0] + 1)
        #     reward = -np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)
        # if pygame.surface.get_at(self.player_pos[0],self.player_pos[1])[:3] == [255,0,0]:
        #     reward -= 1000
        #     done = True
        
            
        state1 = np.array([self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1]])
        return state1, self.reward, done, {}
    
    def reset(self):
        self.player_pos = [30, 30]
        self.obstacle1_pos = [400,300]
        
        # self.obs = [self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1]]
        return np.array([self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1]])
    # 

    def render(self,_):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.player_image, (self.player_pos[0], self.player_pos[1]))
        pygame.draw.rect(self.screen,(255,0,0),self.target_image)
        pygame.draw.rect(self.screen,(200,150,50),self.obstacle1_image)
        font = pygame.font.Font(None, 36)
        
        pos_text = font.render(f'player_pos: {self.player_pos}',True,(0,255,0))
        pos_text1 = font.render(f'player_pos: {self.action}',True,(0,255,0))

        #score_text = font.render(f'Score: {self.reward}', True, (255, 0, 255))
        
        #self.screen.blit(score_text, (600, 60))
        self.screen.blit(pos_text,(10,20))
        self.screen.blit(pos_text1,(10,50))

        #pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.fps)


from gym.envs.registration import register
gym.register(
    id = 'AgentEnv-v2',
    entry_point= 'env_freeze:AgentEnv',
    max_episode_steps= 200000, 
)