from stable_baselines3 import PPO, SAC
import gym
import env_
from stable_baselines3.common.env_util import make_vec_env
env_name = 'AgentEnv-v0'
env = gym.make(env_name)   # Create the environment
env = make_vec_env(env_name, n_envs = 1)
model = PPO('MlpPolicy', env, verbose=1, gamma=0.99, learning_rate=0.0003, n_epochs=10)  # Create the PPO agent
model.learn(total_timesteps=10000, progress_bar=True)    # Train the agent for 10000 timesteps
model.save('Ashutosh/ver2/Final_trained_model/env_2')
# model = PPO.load('Ashutosh/ver2/Final_trained_model/env_2.zip')

obs = env.reset()
score_tot = 0
num_episodes = 5
for i in range(num_episodes):
    score = 0
    obs = env.reset()
    while True:
        action, _ = model.predict(obs)
        state1, reward, done, info = env.step(action)       
        score += reward
        # player_pos_ = [state1[0][0],state1[0][1]]
        env.render()
        if action.all() == 0 :
            print('yaay')
        
        if done == True:
            # env.reset()
            break
    print('Score: ' + str(score))
    obs = env.reset()
    score_tot += score
print('Avg Score = ' + str(score_tot/num_episodes))
env.close()