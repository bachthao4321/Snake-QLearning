import pygame
from snakeql import SnakeQAgent
from visualsnake import VisualSnake
def main():
    # Initialize the Q-learning agent
    agent = SnakeQAgent()

    # Start the training process
    agent.train()

    # After training, optionally run a visual demonstration
    pygame.quit()  # Ensure pygame is properly shutdown before restarting it in the demo
    demo(episode='10000')  # You might want to specify which model/episode to demo

def demo(episode):
    # Initialize the game with visuals
    game = VisualSnake()

    # Load and run the game using the trained Q-table
    game.run_game(episode)

if __name__ == "__main__":
    main()