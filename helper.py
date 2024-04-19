import matplotlib.pyplot as plt
from IPython import display

plt.ion()  # Switch to interactive mode to refresh plots dynamically

#Graphically represents the AI's performance over games.
#Parameters:
#game_scores (list): List of scores from each game.
#average_scores (list): Computed average scores after each game.

def display_progress(game_scores, average_scores):
    
    # Refresh the display to show updated figures
    display.clear_output(wait=True)
    display.display(plt.gcf())  # Display the current figure
    plt.clf()  # Clear the plot to prepare for new data
    plt.xlabel('Game Count')  # Label for the x-axis
    plt.ylabel('Scores')  # Label for the y-axis
    plt.title('Performance Over Time')  # Set the title of the plot

    # Create plots for both scores and average scores
    plt.plot(game_scores, label='Scores per Game')  # Line plot of scores
    plt.plot(average_scores, label='Average Scores')  # Line plot of average scores
    plt.ylim(bottom=0)  # Set the minimum y-axis value to 0 for better clarity

    # Label the most recent score and average score directly on the plot
    plt.text(len(game_scores)-1, game_scores[-1], str(game_scores[-1]))  # Show last game score
    plt.text(len(average_scores)-1, average_scores[-1], str(average_scores[-1]))  # Show last average score
    plt.legend(loc='upper left')  # Position the legend on the plot
    plt.show(block=False)  # Display the plot and continue executing code
    plt.pause(0.1)  # Short pause to update the plot
