import pygame
import sys
import os

# Add parent directory to import solver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from solver import solve_homogeneous_ode

# Pygame initialization
pygame.init()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Differential Equation Solver")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 32)

# Input boxes
input_boxes = {}
active_box = None

def create_input_box(name, x, y, w, h, text=''):
    input_boxes[name] = {'rect': pygame.Rect(x, y, w, h), 'text': text, 'active': False}

def draw_text(text, x, y, color=black):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    global active_box
    degree = 2
    solution_text = ""

    def generate_inputs():
        input_boxes.clear()
        y_pos = 100
        create_input_box('degree', 200, 50, 50, 32, str(degree))

        # Equation coefficients
        for i in range(degree, -1, -1):
            create_input_box(f'coeff{i}', 200 + (degree - i) * 100, y_pos, 50, 32)
        
        # Initial conditions
        y_pos += 100
        for i in range(degree):
            create_input_box(f'ic{i}', 200 + i * 100, y_pos, 50, 32)

    generate_inputs()
    
    solve_button = pygame.Rect(400, 400, 100, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, box in input_boxes.items():
                    box['active'] = box['rect'].collidepoint(event.pos)
                    if box['active']:
                        active_box = name

                if solve_button.collidepoint(event.pos):
                    coeffs = {}
                    ics = {}
                    for name, box in input_boxes.items():
                        if name.startswith('coeff'):
                            order = name.replace('coeff', '')
                            try:
                                coeffs[order] = int(box['text'])
                            except ValueError:
                                coeffs[order] = 0
                        elif name.startswith('ic'):
                            order = name.replace('ic', '')
                            try:
                                ics[order] = int(box['text'])
                            except ValueError:
                                ics[order] = 0
                    solution_text = solve_homogeneous_ode(coeffs, ics)

            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]['text'] = input_boxes[active_box]['text'][:-1]
                else:
                    # Allow digits and minus sign at start
                    if event.unicode.isdigit() or (event.unicode == '-' and input_boxes[active_box]['text'] == ''):
                        input_boxes[active_box]['text'] += event.unicode
                
                if active_box == 'degree':
                    try:
                        degree = int(input_boxes['degree']['text'])
                    except ValueError:
                        degree = 2
                    generate_inputs()

        screen.fill(white)

        # Draw labels
        draw_text("Degree:", 50, 55)
        
        y_pos = 100
        draw_text("Equation:", 50, y_pos + 5)
        for i in range(degree, -1, -1):
            if i == 0:
                term = "y"
            elif i == 1:
                term = "y'"
            else:
                term = f"y{i}''"
            draw_text(f"{term} +", 260 + (degree - i) * 100, y_pos + 5)

        y_pos += 100
        draw_text("Initial Conditions:", 50, y_pos + 5)
        for i in range(degree):
            if i == 0:
                term = "y(0)"
            elif i == 1:
                term = "y'(0)"
            else:
                term = f"y{i}(0)"
            draw_text(term, 150 + i * 100, y_pos + 5)

        # Draw input boxes
        for name, box in input_boxes.items():
            pygame.draw.rect(screen, gray, box['rect'], 2)
            draw_text(box['text'], box['rect'].x + 5, box['rect'].y + 5)

        # Draw solve button
        pygame.draw.rect(screen, gray, solve_button)
        draw_text("Solve", solve_button.x + 20, solve_button.y + 15)

        # Display solution
        if solution_text:
            draw_text(f"Solution: y(x) = {solution_text}", 50, 500)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
