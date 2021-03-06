import gym
import numpy as np
env = gym.make("MountainCar-v0")


learning_rate = 0.17
discount= 0.97
episodes = 600

show_every = 120

epsilon = 0.9  # higher epsilon is better for start

# we do not need the epsilon decay since the environment and episde number is quite low and agent learns in 400 episodes
start_epsilon_decay =1
end_epsilon_decay= episodes //2
epsilon_decay_value = epsilon /episodes

#print(env.observation_space.high)
#print(env.observation_space.low)
#print(env.action_space.n)


DISCRETE_OS_SIZE =[20]*len(env.observation_space.high)
#print(DISCRETE_OS_SIZE)
discrete_os_win_size=(env.observation_space.high - env.observation_space.low)/ DISCRETE_OS_SIZE
#print(discrete_os_win_size)

q_table = np.random.uniform(low=-2, high=0, size =(DISCRETE_OS_SIZE + [env.action_space.n]))
#print(q_table.shape)
#print(q_table)


def get_discrete_state(state):
    discrete_state=(state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

for episode in range(episodes):
    if episode % show_every == 0:
        print(episode)
        render = True
    else:
        render = False
        
    discrete_state = get_discrete_state(env.reset())
    #print(discrete_state)
    #print(np.argmax(q_table[discrete_state]))
    #Q = reward + discount *max()
    
    done = False
    
    while not done:
        action = np.argmax(q_table[discrete_state])
        new_state,reward,done, _ = env.step(action)
        new_discrete_state = get_discrete_state(new_state)
        if render:
            env.render()
        #print(reward, new_state)
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q =q_table[discrete_state + (action, )]
            new_q = (1-learning_rate) * current_q + learning_rate*(reward + discount*max_future_q)
            q_table[discrete_state + (action, )] = new_q
        elif new_state[0] >+ env.goal_position:
            print(f"We made it on episode {episode}")
            q_table[discrete_state + (action,)] =0
            
        discrete_state = new_discrete_state
    
    if end_epsilon_decay >= episode >= start_epsilon_decay:
        epsilon -= epsilon_decay_value

env.close()
