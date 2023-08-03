from stable_baselines3 import PPO, SAC
import gym
import env_continuos
from stable_baselines3.common.env_util import make_vec_env
env_name = 'AgentEnv-v0'
env = gym.make(env_name)   # Create the environment
# env = gym.make(env_name)
env = make_vec_env(env_name, n_envs = 1)
model = PPO('MlpPolicy', env, verbose=1, gamma=0.999, learning_rate=0.0003, n_epochs=10)  # Create the PPO agent
# model = PPO('MlpPolicy', env, verbose=1, learning_rate=1e-4, n_steps=2048, batch_size=64, gamma=0.95, gae_lambda=0.95, n_epochs=10,)
model.learn(total_timesteps=10000, progress_bar=True)    # Train the agent for 10000 timesteps
model.save('Ashutosh/ver2/Final_trained_model/current_all_continuos_10k')
# model = PPO.load('Ashutosh/ver2/Final_trained_model/Current_all_10k_continuos.zip')

# model = SAC(
#     'MlpPolicy',
#     env,
#     verbose=0,
#     learning_rate=1e-3,
#     buffer_size=int(1e5),
#     batch_size=256,
#     train_freq=1,
#     gradient_steps=1,
#     gamma=0.99,
#     tau=0.005,
#     policy_kwargs=dict(
#         net_arch=[256, 256]
#     )
# )

# model.learn(total_timesteps=100000)
# model.save('Ashutosh/ver2/Final_trained_model/New_SAC_continuos_action_100k')
# model = SAC.load('Ashutosh/ver2/Final_trained_model/New_SAC_continuos_action.zip')                  

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