import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

#Neural network module designed for Q-value approximation in reinforcement learning. """

class QNetModel(nn.Module):
    def __init__(self, num_inputs, num_hidden_units, num_outputs):
        super(QNetModel, self).__init__()
        self.input_to_hidden = nn.Linear(num_inputs, num_hidden_units)  # First layer: Input to Hidden
        self.hidden_to_output = nn.Linear(num_hidden_units, num_outputs)  # Second layer: Hidden to Output

    def forward_pass(self, inputs):  # Computes forward pass through the network using ReLU activation.
        activation = F.relu(self.input_to_hidden(inputs))  # Activation function for hidden layer
        output = self.hidden_to_output(activation)  # Output layer computation
        return output

    def save_model(self, filename='model.pth'): # Persist the model parameters to disk.
        directory = './saved_models'  # Custom directory for storing models
        if not os.path.exists(directory):
            os.makedirs(directory)  # Ensure the directory exists
        filepath = os.path.join(directory, filename)  # Construct file path
        torch.save(self.state_dict(), filepath)  # Save the model parameters

class ModelTrainer: # Encapsulates training logic for Q-learning based neural network.
    
    def __init__(self, model, learning_rate, discount_rate): # Initialize the trainer with model and hyperparameters.
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.q_net = model
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.loss_function = nn.MSELoss()

    def optimize(self, states, actions, rewards, next_states, terminal_flags): # Update model weights based on training batch data using MSE loss.
        states = torch.tensor(states, dtype=torch.float)
        next_states = torch.tensor(next_states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)
        terminal_flags = torch.tensor(terminal_flags, dtype=torch.bool)

        # Ensure data is in batch form
        if states.ndim == 1:
            states = states.unsqueeze(0)
            next_states = next_states.unsqueeze(0)
            actions = actions.unsqueeze(0)
            rewards = rewards.unsqueeze(0)
            terminal_flags = terminal_flags.unsqueeze(0)

        # Compute the target Q-value
        current_pred = self.q_net(states)
        target_pred = current_pred.clone()
        for i in range(len(terminal_flags)):
            updated_q = rewards[i]
            if not terminal_flags[i]:
                updated_q += self.discount_rate * torch.max(self.q_net(next_states[idx]))
            target_pred[i][actions[i].argmax().item()] = updated_q

        # Backpropagation
        self.optimizer.zero_grad()
        calcloss = self.loss_function(target_pred, current_pred)
        calcloss.backward()
        self.optimizer.step()
