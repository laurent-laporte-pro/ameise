"""
Animation d'une fourmi sur l'axe horizontal de gauche à droite.

Animation avec pygame.
"""

import math

import pygame
from PIL import Image, ImageSequence

from ameise.resources import RESOURCE_DIR

BACKGROUND = RESOURCE_DIR / "mur-briques-peintes-blanc.jpg"

ANT_IMAGE = RESOURCE_DIR / "ant-walking-3.gif"  # 300 x 230 pixels


def pil_image_to_surface(pil_image):
    mode, size, data = pil_image.mode, pil_image.size, pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def load_gif(filename, size=(100, 77), white=(255, 255, 255)):
    pil_image = Image.open(filename)
    frames = []
    if pil_image.format == "GIF" and pil_image.is_animated:
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.resize(size)
            # convert white background to transparent
            frame = frame.convert("RGBA")
            frame_data = frame.getdata()
            new_data = []
            for item in frame_data:
                d = math.sqrt(
                    (item[0] - white[0]) ** 2
                    + (item[1] - white[1]) ** 2
                    + (item[2] - white[2]) ** 2
                )
                if d < 10:
                    item = item[:3] + (0,)
                new_data.append(item)
            frame.putdata(new_data)

            pygame_image = pil_image_to_surface(frame)
            frames.append(pygame_image)
    else:
        frames.append(pil_image_to_surface(pil_image))
    return frames


def animate_ant():
    screen_size = (1024, 768)
    sleep_time = 3

    # creation d'une image de fond blanche
    background = pygame.image.load(BACKGROUND)
    background = pygame.transform.scale(background, screen_size)

    # initialisation de pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Fourmi")

    # chargement de la GIF animée de la fourmi
    gif_frame_list = load_gif(ANT_IMAGE)

    # position initiale de la fourmi
    x = screen_size[0] // 2
    y = screen_size[1] // 2

    # boucle d'animation
    running = True
    curr_frame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # si la fourmi est au voisinage de la souris, elle s'arrête
        mouse_pos = pygame.mouse.get_pos()
        if math.hypot(x - mouse_pos[0], y - mouse_pos[1]) < 2:
            pygame.time.wait(sleep_time)
            continue

        # calcul de l'angle entre la fourmi et la souris
        angle = math.atan2(mouse_pos[1] - y, mouse_pos[0] - x)
        angle_deg = math.degrees(angle)

        # effacement de l'écran
        screen.blit(background, (0, 0))

        # affiche la position de la fourmi en haut à droite
        font = pygame.font.Font(None, 24)
        text = font.render(f"position: ({x:.1f}, {y:.1f})", True, (0, 0, 0))
        screen.blit(text, (screen_size[0] - 200, 20))

        # affiche l'angle en haut à droite
        font = pygame.font.Font(None, 24)
        text = font.render(f"angle: {angle_deg:.2f}°", True, (0, 0, 0))
        screen.blit(text, (screen_size[0] - 200, 40))

        # affiche la distance en haut à droite
        font = pygame.font.Font(None, 24)
        dist = math.hypot(x - mouse_pos[0], y - mouse_pos[1])
        text = font.render(f"distance: {dist:.2f}", True, (0, 0, 0))
        screen.blit(text, (screen_size[0] - 200, 60))

        # dessine le triangle rectangle formé par la fourmi et la souris
        pygame.draw.line(screen, (0, 0, 190), (x, y), mouse_pos, 2)
        pygame.draw.line(screen, (190, 0, 0), (x, y), (x, mouse_pos[1]), 2)
        pygame.draw.line(screen, (0, 190, 0), (x, mouse_pos[1]), mouse_pos, 2)

        # fourmi se tourne vers la souris
        rotated = pygame.transform.rotate(gif_frame_list[curr_frame], -angle_deg)

        # affichage de la fourmi taille / 3
        rect = rotated.get_rect(center=(x, y), size=(100, 77))
        screen.blit(rotated, rect)

        # mise à jour de l'écran
        pygame.display.flip()

        # animation de la fourmi
        curr_frame = (curr_frame + 1) % len(gif_frame_list)

        # La fourmi se déplace vers la souris
        x = x + math.cos(angle)
        y = y + math.sin(angle)

        # attente de 10 ms
        pygame.time.wait(sleep_time)

    # fin de l'animation
    pygame.quit()


if __name__ == "__main__":
    animate_ant()
