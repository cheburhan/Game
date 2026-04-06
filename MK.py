import pygame
import sys
from projectiles import Projectile
from fighter import Fighter
import settings

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('Mortal Kombat - Maine Theme (Original).mp3')
pygame.mixer.music.play(3)
pygame.mixer.music.set_volume(0.6)

# ------------------- НОВОЕ -------------------
game_over = False
winner_text = ""

font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)
# --------------------------------------------

projectiles_list = []

player1 = Fighter(200, (0, 100, 255), pygame.K_a, pygame.K_d, pygame.K_f, pygame.K_w, pygame.K_s, pygame.K_r,
                  "BLUE FIGHTER", (100, 150, 255))
player2 = Fighter(900, (255, 100, 0), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SLASH, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT,
                  "ORANGE FIGHTER", (255, 150, 50))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ----------- РЕСТАРТ -----------
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_g:
                player1.health = 100
                player2.health = 100

                projectiles_list.clear()

                player1.x = 200
                player2.x = 900

                game_over = False
        # --------------------------------

    keys = pygame.key.get_pressed()

    # ----------- ОБНОВЛЕНИЕ ТОЛЬКО ЕСЛИ НЕ GAME OVER -----------
    if not game_over:
        for projectile in projectiles_list[:]:
            projectile.update(player1 if projectile.owner == player2 else player2)
            if not projectile.active:
                projectiles_list.remove(projectile)

        player1.update(keys, player2, projectiles_list)
        player2.update(keys, player1, projectiles_list)

        # ----------- ПРОВЕРКА ПОБЕДЫ -----------
        if player1.health <= 0:
            winner_text = "PLAYER 2 WINS!"
            game_over = True
        elif player2.health <= 0:
            winner_text = "PLAYER 1 WINS!"
            game_over = True
        # ---------------------------------------

    # ----------- ОТРИСОВКА -----------
    if settings.background:
        settings.screen.blit(settings.background, (0, 0))
    else:
        settings.screen.fill((0,0,0))

    player1.draw_ui(settings.screen, 50)
    player2.draw_ui(settings.screen, settings.WIDTH - 350)

    player1.draw(settings.screen)
    player2.draw(settings.screen)

    for projectile in projectiles_list:
        projectile.draw(settings.screen)

    # ----------- ЭКРАН ПОБЕДЫ -----------
    if game_over:
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        settings.screen.blit(overlay, (0, 0))

        text = font.render(winner_text, True, (255, 255, 255))
        settings.screen.blit(text, (settings.WIDTH // 2 - 250, settings.HEIGHT // 2 - 50))

        restart_text = small_font.render("Press G to restart", True, (200, 200, 200))
        settings.screen.blit(restart_text, (settings.WIDTH // 2 - 150, settings.HEIGHT // 2 + 30))
    # -----------------------------------

    pygame.display.flip()
    settings.clock.tick(60)

pygame.quit()
sys.exit()