import pygame
import sys
import pandas as pd
from random import uniform
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000  # Larger screen width
SCREEN_HEIGHT = 800  # Larger screen height
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OUTER_SQUARE_SIZE = 600  # Larger size of the larger square


# Sample DataFrame with matching rows
data = []

for j in range(20):
  name = f"Square {j}"
  size = round(uniform(10, 30))

  data.append({
      "Name": name,
      "Area": size*5
  })


df = pd.DataFrame(data)

# Binary array (determines which rows from the database to choose)
num_rows = df.shape[0]
binary_array = np.random.randint(2, size=num_rows).tolist()  # Match the number of selected rows

# Create a boolean index based on the binary_array
boolean_index = [x == 1 for x in binary_array]

# Filter the DataFrame using the boolean index
selected_data = df[boolean_index]

# Sizes for the inner squares
inner_square_sizes = selected_data["Area"].tolist()

# Labels for the inner squares
inner_square_labels = selected_data["Name"].tolist()

def draw_squares(data, screen):
    x = (SCREEN_WIDTH - OUTER_SQUARE_SIZE) // 2  # Center the larger square horizontally
    y = (SCREEN_HEIGHT - OUTER_SQUARE_SIZE) // 2  # Center the larger square vertically

    for i, value in enumerate(data):
        if i >= len(inner_square_sizes):
            #print(f"Index out of range: i={i}, inner_square_sizes={inner_square_sizes}")
            break

        inner_square_size = inner_square_sizes[i]
        label = inner_square_labels[i]

        pygame.draw.rect(screen, BLACK, (x, y, inner_square_size, inner_square_size), 1)  # Draw a black outline for inner squares

        # Create a font and render the label text with a smaller font size
        font = pygame.font.Font(None, 30)  # Adjust the font size here
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=(x + inner_square_size // 2, y + inner_square_size // 2))

        # Draw the label text on the square
        screen.blit(text, text_rect)

        x += inner_square_size  # Increment the x position for the next square

        # Move to the next row if we reach the end of the larger square
        if x + inner_square_size > (SCREEN_WIDTH - OUTER_SQUARE_SIZE) // 2 + OUTER_SQUARE_SIZE:
            x = (SCREEN_WIDTH - OUTER_SQUARE_SIZE) // 2  # Reset x position
            y += inner_square_size

            # Check if we need to move to the next row
            if y + inner_square_size > (SCREEN_HEIGHT - OUTER_SQUARE_SIZE) // 2 + OUTER_SQUARE_SIZE:
                x = (SCREEN_WIDTH - OUTER_SQUARE_SIZE) // 2  # Reset x position
                y = (SCREEN_HEIGHT - OUTER_SQUARE_SIZE) // 2  # Reset y position

# Create a window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Drawer")

# Main loop
running = True
data = binary_array

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  # Set background to white
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - OUTER_SQUARE_SIZE // 2, SCREEN_HEIGHT // 2 - OUTER_SQUARE_SIZE // 2, OUTER_SQUARE_SIZE, OUTER_SQUARE_SIZE), 1)  # Draw the larger square
    draw_squares(data, screen)  # Draw inner squares with labels and sizes based on the binary array

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
