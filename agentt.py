import torch
import random
import numpy as np
from collections import deque
from gamee import AutomatedSnakeGame, Movement, Coordinates
from mod import NeuralQNet, ModelTrainer
from helper import display_progress

# Setup parameters
MAX_RECALL = 100000  # Maximum memory capacity
BATCH_SIZE = 1000  # Size of training batches
ALPHA = 0.001  # Learning rate coefficient

class GameAgent: #This class is designed to manage the AI operations for snake gameplay.      
    def __init__(self):
        self.games_played = 0  # Track the total number of games played
        self.remembered_states = deque(maxlen=MAX_RECALL)  # Memory for past states
        self.brain = NeuralQNet()  # Neural network for decision making
        self.coach = ModelTrainer(self.brain, lr=ALPHA, gamma=0.9)  # Trainer for the network

    def memorize(self, state, action, reward, next_state, finished): # Store the game state in memory for future training.
        if len(self.remembered_states) > MAX_RECALL:
            self.remembered_states.popleft()
        self.remembered_states.append((state, action, reward, next_state, finished))

    def replay_experience(self): # Train the model using a randomly selected batch of stored states.
        if len(self.remembered_states) > BATCH_SIZE:
            mini_batch = random.sample(self.remembered_states, BATCH_SIZE)
        else:
            mini_batch = self.remembered_states

        batch_states, batch_actions, batch_rewards, batch_next_states, batch_finished = zip(*mini_batch)
        self.coach.train_step(batch_states, batch_actions, batch_rewards, batch_next_states, batch_finished)

    def learn_quickly(self, state, action, reward, next_state, finished): # Immediate training using the most recent experience.
        self.coach.train_step(state, action, reward, next_state, finished)

def execute_training():
    score_history = []
    average_scores = []
    total_score = 0
    record_score = 0
    agent = GameAgent()
    game_instance = AutomatedSnakeGame()
    
    while True:
        current_state = game_instance.get_state()
        
        next_action = agent.brain.predict_move(current_state)
        
        reward, game_over, score = game_instance.play_step(next_action)
        next_state = game_instance.get_state()
        
        agent.learn_quickly(current_state, next_action, reward, next_state, game_over)
        
        agent.memorize(current_state, next_action, reward, next_state, game_over)

        if game_over:
            game_instance.reset()
            agent.games_played += 1
            agent.replay_experience()
            
            if score > record_score:
                record_score = score
                agent.brain.save()
            
            print(f'Game {agent.games_played}, Score: {score}, Record: {record_score}')
            
            score_history.append(score)
            total_score += score
            mean_score = total_score / agent.games_played
            average_scores.append(mean_score)
            display_progress(score_history, average_scores)

if __name__ == "__main__":
    execute_training()
