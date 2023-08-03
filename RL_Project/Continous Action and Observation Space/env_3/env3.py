import gym
import pygame
import numpy as np
import math

import cv2


## This is the code which we are using now, feeding position of everything in the states and using pygame rect to avoid collision.
class AgentEnv(gym.Env):
    def __init__(self):     
        pygame.init()
        pygame.font.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = 5   # frame per second

        ## Create a videoWriter object to save the video
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter("File_name",self.fourcc,self.fps,(self.width,self.height))



        self.grid_size = 40 # This is the size of boxes
        self.count = 0
        self.action_space = gym.spaces.Box(-10,10, shape=(2,), dtype=np.float64)
        self.action = 0
        self.reward = 0
        self.observation_space = gym.spaces.Box(np.array([0,0]),np.array([self.width,self.height]))
        
        self.agent_image = pygame.image.load('TANK.png')
        self.agent_image = pygame.transform.scale(self.agent_image,(self.grid_size ,self.grid_size))
        self.player_image = pygame.transform.rotate(self.agent_image, 180)
        self.player = self.player_image.get_rect()
        self.player_vel = [0,0]
        self.target_pos = [650, 450]
        # self.target_pos = [np.random.randint(low=10,high=700,size=None), np.random.randint(low=10,high = 500,size=None)]
        # a  = np.random()

        self.target_image = pygame.Rect(self.target_pos[0],self.target_pos[1],self.grid_size,self.grid_size)
        
        self.obstacle1_pos = [400, 300]
        self.obstacle1_image = pygame.Rect(self.obstacle1_pos[0],self.obstacle1_pos[1],self.grid_size,self.grid_size)
        ## self.target_angle = math.degrees(math.atan(abs(self.target_pos[1]-self.player_pos[1]))/abs(self.target_pos[0]-self.player_pos[0]))
    def step(self,action):        
        #if action >= 0:
        # self.action = action

        # alpha = 0.9
        # self.prev_action = np.zeros((2,), dtype=np.float32) if not hasattr(self, 'prev_action') else self.prev_action
        # smoothed_action = alpha * self.prev_action + (1 - alpha) * action
        # self.prev_action = smoothed_action
        # action = smoothed_action
        self.reward = 0
        self.player_vel[0] += action[0]
        self.player_vel[1] += action[1]

        # if self.player_pos[0]+self.player_vel[0]>=0 and self.player_pos[0]+self.player_vel[0]<=700 and self.player_pos[1]+self.player_vel[1]>=0 and self.player_pos[1]+self.player_vel[1]<=550 : 
        self.player.x += self.player_vel[0]
        self.player.y += self.player_vel[1]
        #self.reward = -np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)*0.01
        if self.player.right > 700:
            self.player.right = 700
            self.player_vel[0] = 0
        if self.player.left < 0:
            self.player.left = 0
            self.player_vel[0] = 0
        if self.player.top < 0:
            self.player.top = 0
            self.player_vel[1] = 0
        if self.player.bottom > 550:
            self.player.bottom = 550
            self.player_vel[1] = 0



        if self.player.colliderect(self.target_image):
            self.reward +=20
            done = True

        elif self.player.colliderect(self.obstacle1_image):
            self.reward -= 10
            done = True
        else:
            self.reward += -(np.sqrt((self.player.x-self.target_pos[0])**2 + (self.player.y-self.target_pos[1])**2))*0.0001
            done = False
        if done == False:
            self.reward -= 0.01 

    
        # else:
            # if self.player_pos[0]+self.player_vel[0]<0:
            #     self.player_pos[0]=0
            # if self.player_pos[0]+self.player_vel[0]>700:
            #     self.player_pos[0]=700
            # if self.player_pos[1]+self.player_vel[1]<0:
            #     self.player_pos[1]=0
            # if self.player_pos[1]+self.player_vel[1]>550:
            #     self.player_pos[1]=550
                
            #self.reward -= 10000
            # self.player_pos[0] += self.player_vel[0]
            # self.player_pos[1] += self.player_vel[1]
    
            # self.reward -= np.sqrt((self.player_pos[0]-self.target_pos[0])**2 + (self.player_pos[1]-self.target_pos[1])**2)*0.01
            # done = False
            
            
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
        
            
        # state1 = np.array([self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1], self.target_pos[0], self.target_pos[1]])
        state1 = np.array([self.player.x,self.player.y])
        return state1, self.reward, done, {}
    
    def reset(self):
        [self.player.x,self.player.y] = [30, 30]
        self.obstacle1_pos = [400,300]
        self.target_pos = [650,450]
        self.target_image = pygame.Rect(self.target_pos[0],self.target_pos[1],self.grid_size,self.grid_size)
        
        # self.obs = [self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1]]
        # return np.array([self.player_pos[0],self.player_pos[1],self.obstacle1_pos[0],self.obstacle1_pos[1], self.target_pos[0], self.target_pos[1]])
        return np.array([self.player.x,self.player.y])
     

    def render(self,i,mode = "rgb_array"):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.player_image, (self.player.x, self.player.y))
        pygame.draw.rect(self.screen,(0,255,0),self.target_image)
        pygame.draw.rect(self.screen,(255,0,0),self.obstacle1_image)
        font = pygame.font.Font(None, 36)
        
        pos_text = font.render(f'player_pos: {[self.player.x,self.player.y]}',True,(0,0,255))
        pos_text1 = font.render(f'player_pos: {self.action}',True,(0,0,255))

        #score_text = font.render(f'Score: {self.reward}', True, (255, 0, 255))
        
        #self.screen.blit(score_text, (600, 60))
        self.screen.blit(pos_text,(10,20))
        self.screen.blit(pos_text1,(10,50))

        pygame.image.save(self.screen,'frame.png')

        self.frame = cv2.imread('frame.png')
        self.out.write(self.frame)



        #pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.fps)

        if i==4:
            self.out.release()



from gym.envs.registration import register
gym.register(
    id = 'AgentEnv-v0',
    entry_point= 'env3:AgentEnv',
    max_episode_steps= 500, 
)