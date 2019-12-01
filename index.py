# randomness was too high so gadhe ka bacha ni chal raha tha
import numpy as np 
import cv2
from PIL import Image
import pickle 
import copy

EPISODS = 25000
SHOW_AT_EVERY = 5000
SIZE = 3
epsilon = 0.5
EPSILON_DECAY = 0.9

q_table = {}
show = False

PENALITY_SETP_ON_SELF = 9
PENALITY_SETP_ON_OTHER = 9
PENALITY_SETP_ON_LOOSE = 800
REWARD_SETP_ON_EMPTY = 10
REWARD_ON_WIN = 400

LEARNING_RATE = 0.01
DISCOUNT = 0.9

# only 3 states are possible 
# 0 for red
# 1 for green
# 2 for empty
compute = True
# after 3 we find bug that we are only exploring upto 0,1,2 not the full 0-9 thing
start_q_table = f"qtable-{5}.pickle"
# with open(start_q_table, "rb") as f:
    # compute = False
    # q_table = pickle.load(f)

# while True:
#     x1 = int(input('x1'))
#     x2 = int(input('x2'))
#     x3 = int(input('x3'))
#     x4 = int(input('x4'))
#     x5 = int(input('x5'))
#     x6 = int(input('x6'))
#     x7 = int(input('x7'))
#     x8 = int(input('x8'))
#     x9 = int(input('x9'))
#     print(q_table[x1,x2,x3,x4,x5,x6,x7,x8,x9])

all_possibilites = []

if not q_table:
    for x1 in range(3):
        for x2 in range(3):
            for x3 in range(3):
                for x4 in range(3):
                    for x5 in range(3):
                        for x6 in range(3):
                            for x7 in range(3):
                                for x8 in range(3):
                                    for x9 in range(3):
                                        # unique state                         # actions of red
                                        # current_state = (x1,x2,x3,x4,x5,x6,x7,x8,x9)
                                        # player_turns = current_state.count(0)
                                        # enemy_turns = current_state.count(1)
                                        # vacant_space = current_state.count(2)
                                        # if enemy_turns <0:
                                        #     enemy_turns = 0

                                        # q_table[x1,x2,x3,x4,x5,x6,x7,x8,x9]= [ np.inf*-1 for i in range(9)]
                                        # if player_turns <=5 and enemy_turns < player_turns and vacant_space == (9-player_turns-enemy_turns):
                                        # all_possibilites.append((x1,x2,x3,x4,x5,x6,x7,x8,x9))                        
                                        q_table[x1,x2,x3,x4,x5,x6,x7,x8,x9]= [ -9 for i in range(9)]
else:
    print('Loded')
red = []
green = []
d = {

    0:(155,15,0),
    1:(0,255,0),
}

# print(all_possibilites)

# red is 0
if True:
    def check_if_red_win(red_places):
        print('checking ')
        print(red_places)
        print()
        diagnol_1 = red_places[0] == 0 and red_places[4] == 0 and red_places[8] == 0 
        diagnol_2 = red_places[2] == 0 and red_places[4] == 0 and red_places[6] == 0
        border_1 = red_places[0] == 0 and red_places[1] == 0 and red_places[2] == 0
        border_2 = red_places[2] == 0 and red_places[5] == 0 and red_places[8] == 0
        border_3 = red_places[6] == 0 and red_places[7] == 0 and red_places[8] == 0
        border_4 = red_places[0] == 0 and red_places[3] == 0 and red_places[6] == 0
        center_horizontal = red_places[3] == 0 and red_places[4] == 0 and red_places[5] == 0
        center_verticle = red_places[1] == 0 and red_places[4] == 0 and red_places[7] == 0
        # if diagnol_1:
        #     print("diagnol_1")
        # if diagnol_2:
        #     print("diagnol_2")
        # if border_1:
        #     print("border_1")
        # if border_2:
        #     print("border_2")
        # if border_3:
        #     print("border_3")
        # if border_4:
        #     print('border_4')
        # if center_horizontal:
        #     print("center_horizontal")
        # if center_verticle:
        #     print("center_verticle")

        return diagnol_1 or diagnol_2 or border_1 or border_2 or border_3 or border_4 or center_horizontal or center_verticle

    def check_if_red_loose(player_places):
        player_places = list(player_places)
        print('checking ')
        print(player_places)
        diagnol_1 = player_places[0] == 1 and player_places[4] == 1 and player_places[8] == 1 
        diagnol_2 = player_places[2] == 1 and player_places[4] == 1 and player_places[6] == 1
        border_1 = player_places[0] == 1 and player_places[1] == 1 and player_places[2] == 1
        border_2 = player_places[2] == 1 and player_places[5] == 1 and player_places[8] == 1
        border_3 = player_places[6] == 1 and player_places[7] == 1 and player_places[8] == 1
        border_4 = player_places[0] == 1 and player_places[3] == 1 and player_places[6] == 1
        center_horizontal = player_places[3] == 1 and player_places[4] == 1 and player_places[5] == 1
        center_verticle = player_places[1] == 1 and player_places[4] == 1 and player_places[7] == 1
        # if diagnol_1:
        #     print("diagnol_1")
        # if diagnol_2:
        #     print("diagnol_2")
        # if border_1:
        #     print("border_1")
        # if border_2:
        #     print("border_2")
        # if border_3:
        #     print("border_3")
        # if border_4:
        #     print('border_4')
        # if center_horizontal:
        #     print("center_horizontal")
        # if center_verticle:
        #     print("center_verticle")

        return diagnol_1 or diagnol_2 or border_1 or border_2 or border_3 or border_4 or center_horizontal or center_verticle

    episode_rewards = []

    for episode in range(EPISODS):

        reward = 0

        if episode % SHOW_AT_EVERY == 0:
            env = np.zeros((SIZE,SIZE,3), dtype=np.uint8)
            show = True
        else:
            show = False

        for j in range(10):
            obs = tuple([np.random.randint(0,3) for i in range(9)]) #q_table[np.random.randint(0,len(all_possibilites))] 
            #print(obs)
            if epsilon > np.random.random():
                action = np.random.randint(0,9)
            else:
                #print(obs)
                action = np.argmax(q_table[obs])

            new_obs = copy.deepcopy(obs)
                # play red
            temp_list_1 = []
            temp_list_1 = list(new_obs)
            temp_list_1[action] = 1
            new_obs = tuple(temp_list_1)

            if obs[action] == 0:
                reward = -PENALITY_SETP_ON_OTHER
                print('not checking')
            elif  obs[action] == 1:
                reward = -PENALITY_SETP_ON_SELF
                print('not checking')
            elif check_if_red_loose(new_obs):
                reward = REWARD_ON_WIN
            elif check_if_red_win(new_obs):
                reward = -PENALITY_SETP_ON_LOOSE
            elif obs[action] == 2:
                reward = REWARD_SETP_ON_EMPTY
           
            max_future_q = np.max(q_table[new_obs])
            current_q = q_table[obs][action]

            if reward == REWARD_ON_WIN:
                new_q = REWARD_ON_WIN
            elif reward == -PENALITY_SETP_ON_SELF:
                new_q = -PENALITY_SETP_ON_SELF
            elif reward == -PENALITY_SETP_ON_OTHER:
                new_q = -PENALITY_SETP_ON_OTHER
            else:
                new_q = (1-LEARNING_RATE)*current_q+LEARNING_RATE*(reward + DISCOUNT*max_future_q)

            q_table[obs][action] = new_q
            if show:
                # createing rgb plane
                # setting colors at that position
                print(list(np.array(new_obs).reshape(3,3)))
                env_array = list(np.array(new_obs).reshape(3,3))
                for t1 in range(3):
                    for t2 in range(3):
                        if env_array[t1][t2] == 0:
                            env[t1][t2] = d[0]
                        elif env_array[t1][t2] == 1:
                            env[t1][t2] = d[1]
                        else :
                            env[t1][t2] = (0,0,0)
                img = Image.fromarray(env,"RGB")
                img = img.resize((300,300))
                cv2.imshow("",np.array(img))
                if reward == REWARD_ON_WIN:
                    # wait to show win
                    print('winnningggg')
                    print(new_obs)
                    if cv2.waitKey(500) & 0xFF == ord('q'):
                        break
                elif  reward == -PENALITY_SETP_ON_SELF or reward == -PENALITY_SETP_ON_OTHER:
                    print('panality')
                    print(new_obs)
                    if cv2.waitKey(500) & 0xFF == ord('q'):
                        break 
                else:
                    # wait to show steps
                    print('stepping')
                    print(new_obs)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break 
                # for graph
                episode_reward = reward
                # when game over
                if reward == REWARD_ON_WIN:
                    break
            # for graph
            episode_rewards.append(episode_reward)
            # reducing epsilon
            epsilon *= EPSILON_DECAY

    moving_avg = np.convolve(episode_rewards,np.ones((SHOW_AT_EVERY,))/ SHOW_AT_EVERY, mode="valid")

    # plt.plot([i for i in range(len(moving_avg))], moving_avg)
    # plt.ylabel(f"reward {SHOW_EVERY}")
    # plt.xlabel("episode #")
    # plt.show()

    with open( start_q_table,"wb") as f:
        pickle.dump(q_table,f)

print(q_table)

while True:
    init_state = [2,2,2,2,2,2,2,2,2]
    reward_user = 0
    reward_enemy = 0
    for j in range(5):

        for a in range(3):
            print(f" : {init_state[a*3 + 0]} : {init_state[a*3 + 1]} : {init_state[a*3 + 2]}")

        user_input = input("choose number")
        user_input = int(user_input)
        init_state[user_input] = 1
        print(tuple(init_state)," User will  ",q_table[tuple(init_state)])
        print("reward is ",q_table[tuple(init_state)][user_input])
        reward_user+=q_table[tuple(init_state)][user_input]
        print("Computer will ",q_table[tuple(init_state)])
        init_state[np.argmax(q_table[tuple(init_state)])]=0
        reward_enemy+=np.max(q_table[tuple(init_state)])  
    
    print (f"reward_user:{reward_user}, reward_enemy:{reward_enemy}")
    is_break = input("quit?y/n")
    
    if is_break == "y":
        break
                
