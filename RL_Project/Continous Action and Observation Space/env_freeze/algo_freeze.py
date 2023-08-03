from stable_baselines3 import PPO
import gym
import env_freeze
from stable_baselines3.common.env_util import make_vec_env
env_name = 'AgentEnv-v2'
env = gym.make(env_name)   # Create the environment
# env = gym.make(env_name)
env = make_vec_env(env_name, n_envs = 1)
# model = PPO('MlpPolicy', env, verbose=1)  # Create the PPO agent
# model.learn(total_timesteps=500000)    # Train the agent for 10000 timesteps
# model.save(r'Final_trained_model\Stuck_5L')
model = PPO.load(r'Final_trained_model\Stuck_5L',env = env)

                  
obs = env.reset()
score_tot = 0
num_episodes = 5
for i in range(num_episodes):
    score = 0
    
    while True:
        action, _ = model.predict(obs)
        state1, reward, done, info = env.step(action)       
        score += reward
        # player_pos_ = [state1[0][0],state1[0][1]]
        env.render()
        if action.all() == 0 :
            print('yaay')
        
        if done == True:
            break
    print('Score: ' + str(score))
    obs = env.reset()
    score_tot += score
print('Avg Score = ' + str(score_tot/num_episodes))
env.close()