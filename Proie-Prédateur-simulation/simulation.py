import pygame
import numpy as np
import math

# Initialiser Pygame
pygame.init()

# Paramètres de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Proie-Prédateur")

# Couleurs
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (220, 220, 220)

# Paramètres du modèle
S0, I0, beta, lamda = 0.4, 0.2, 0.5, 12

# Conditions initiales
S = 1000000 * S0
I = 1000000 * I0
R = 0
D = 0

# Temps de simulation
t_max = lamda
dt = 0.1

# Modèle SIRD
def sird_model(S, I, R, D, beta, gamma, mu):
    dSdt = -beta * S * I / 1000000
    dIdt = beta * S * I / 1000000 - gamma * I - mu * I
    dRdt = gamma * I
    dDdt = mu * I
    return dSdt, dIdt, dRdt, dDdt

# Fonction pour dessiner un slider
def draw_slider(x, y, width, height, value, color):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))  # Fond du slider
    pygame.draw.rect(screen, color, (x, y, value * width, height))  # Barre du slider
    pygame.draw.circle(screen, color, (x + int(value * width), y + height // 2), 10)  # Curseur

# Fonction pour gérer les événements de slider
def handle_slider_event(slider_rect, value, event):
    if slider_rect.collidepoint(event.pos):  # Si on clique sur le slider
        new_value = (event.pos[0] - slider_rect.x) / slider_rect.width
        return min(max(new_value, 0), 1)  # Limiter entre 0 et 1
    return value

# Boucle principale
running = True
clock = pygame.time.Clock()
t = 0

# Liste pour stocker les données pour le tracé
S_data = []
I_data = []
R_data = []
D_data = []

# Définir les rectangles pour les sliders
slider_S0_rect = pygame.Rect(50, 500, 300, 20)
slider_I0_rect = pygame.Rect(50, 530, 300, 20)
slider_beta_rect = pygame.Rect(50, 560, 300, 20)
slider_lamda_rect = pygame.Rect(50, 590, 300, 20)

# Limite de population pour éviter des valeurs infinies
max_population = 1000000

# Boucle principale
while running and t < t_max:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des sliders (événements de souris)
    if event.type == pygame.MOUSEBUTTONDOWN:
        S0 = handle_slider_event(slider_S0_rect, S0, event)
        I0 = handle_slider_event(slider_I0_rect, I0, event)
        beta = handle_slider_event(slider_beta_rect, beta, event)
        lamda = handle_slider_event(slider_lamda_rect, lamda, event)

    # Mettre à jour les populations en fonction du modèle
    dSdt, dIdt, dRdt, dDdt = sird_model(S, I, R, D, beta, 0.1, 0.05)
    S += dSdt * dt
    I += dIdt * dt
    R += dRdt * dt
    D += dDdt * dt

    # Limiter les valeurs de population à une taille maximale
    S = min(S, max_population)
    I = min(I, max_population)
    R = min(R, max_population)
    D = min(D, max_population)

    # Ajouter les données à la liste
    S_data.append(S)
    I_data.append(I)
    R_data.append(R)
    D_data.append(D)

    # Effacer l'écran
    screen.fill(WHITE)

    # Tracer les courbes
    max_population = max(max(S_data), max(I_data), max(R_data), max(D_data))

    # Normaliser les populations pour les afficher à l'échelle de la fenêtre
    S_scaled = [height - (N / max_population) * height for N in S_data]
    I_scaled = [height - (N / max_population) * height for N in I_data]
    R_scaled = [height - (N / max_population) * height for N in R_data]
    D_scaled = [height - (N / max_population) * height for N in D_data]

    # Tracer les lignes pour les populations
    for i in range(1, len(S_scaled)):
        pygame.draw.line(screen, BLUE, (i - 1, S_scaled[i - 1]), (i, S_scaled[i]), 2)
        pygame.draw.line(screen, RED, (i - 1, I_scaled[i - 1]), (i, I_scaled[i]), 2)
        pygame.draw.line(screen, GREEN, (i - 1, R_scaled[i - 1]), (i, R_scaled[i]), 2)
        pygame.draw.line(screen, BLACK, (i - 1, D_scaled[i - 1]), (i, D_scaled[i]), 2)

    # Afficher les axes
    pygame.draw.line(screen, BLACK, (0, height), (width, height), 3)  # Axe X
    pygame.draw.line(screen, BLACK, (0, 0), (0, height), 3)  # Axe Y

    # Dessiner les sliders
    draw_slider(slider_S0_rect.x, slider_S0_rect.y, slider_S0_rect.width, slider_S0_rect.height, S0, BLUE)
    draw_slider(slider_I0_rect.x, slider_I0_rect.y, slider_I0_rect.width, slider_I0_rect.height, I0, RED)
    draw_slider(slider_beta_rect.x, slider_beta_rect.y, slider_beta_rect.width, slider_beta_rect.height, beta, GREEN)
    draw_slider(slider_lamda_rect.x, slider_lamda_rect.y, slider_lamda_rect.width, slider_lamda_rect.height, lamda, BLACK)

    # Afficher les valeurs des sliders
    font = pygame.font.SysFont("Arial", 16)
    text = font.render(f"S0: {S0:.2f}, I0: {I0:.2f}, β: {beta:.2f}, λ: {lamda:.2f}", True, BLACK)
    screen.blit(text, (50, 450))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Avancer dans le temps
    t += dt
    clock.tick(60)  # Limiter à 60 FPS

# Quitter Pygame
pygame.quit()
