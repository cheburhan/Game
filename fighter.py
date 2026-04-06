import pygame
import settings
import projectiles
pygame.mixer.init()

hit_sound = pygame.mixer.Sound("mixkit-soft-quick-punch-2151.wav")
hit_sound.set_volume(0.7)

# Check Sprites
class Fighter:
    def __init__(self, x, color, left_key, right_key, attack_key, jump_key, sit_key, ability_key, name, ability_color):
        self.x = x
        self.y = settings.HEIGHT - 150
        self.width = 60
        self.height = 100
        self.original_height = 100  # Сохраняем оригинальную высоту
        self.color = color
        self.health = 100
        self.speed = 5
        self.attack_cooldown = 0
        self.ability_cooldown = 0
        self.ability_max_cooldown = 240
        self.name = name
        self.ability_color = ability_color
        
        # Управление
        self.left_key = left_key
        self.right_key = right_key
        self.attack_key = attack_key
        self.jump_key = jump_key
        self.ability_key = ability_key
        self.sit_key = sit_key

        # Физика прыжка
        self.is_jumping = False
        self.vertical_speed = 0
        self.gravity = 1
        self.jump_power = -15
        
        # Присед
        self.is_sitting = False
        self.sitting_height = self.height // 2
        self.sitting_y_offset = self.sitting_height  # Смещение для Y координаты

        # Хитбокс
        self.attack_zone_visible = 0
        self.last_attack_zone = None
    
    def update(self, keys, enemy, projectiles_list):
        ground_y = settings.HEIGHT - 150

        # Кулдауны
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1
        
        # ======================
        # ДВИЖЕНИЕ
        # ======================
        if keys[self.left_key] and self.x > 0:
            self.x -= self.speed
        if keys[self.right_key] and self.x < settings.WIDTH - self.width:
            self.x += self.speed

        # ======================
        # ПРЫЖОК
        # ======================
        if not self.is_jumping:
            if keys[self.jump_key] and not self.is_sitting:
                self.is_jumping = True
                self.vertical_speed = self.jump_power
                # При прыжке выходим из приседа
                self.is_sitting = False
        else:
            self.y += self.vertical_speed
            self.vertical_speed += self.gravity

            if self.y >= ground_y:
                self.y = ground_y
                self.is_jumping = False
                self.vertical_speed = 0

        # ======================
        # ПРИСЕД (ИСПРАВЛЕННЫЙ)
        # ======================
        if not self.is_jumping:  # Приседать можно только на земле
            if keys[self.sit_key]:
                if not self.is_sitting:
                    # Начинаем приседать - корректируем Y позицию
                    self.is_sitting = True
                    # Сдвигаем персонажа вниз, чтобы ноги оставались на земле
                    self.y += (self.original_height - self.sitting_height)
                    self.height = self.sitting_height
            else:
                if self.is_sitting:
                    # Заканчиваем приседать - возвращаем исходную позицию
                    self.is_sitting = False
                    # Возвращаем Y позицию обратно вверх
                    self.y -= (self.original_height - self.sitting_height)
                    self.height = self.original_height
        else:
            # Если в воздухе и был присед - отменяем его
            if self.is_sitting:
                self.is_sitting = False
                self.y -= (self.original_height - self.sitting_height)
                self.height = self.original_height

        # ======================
        # АТАКА
        # ======================
        if keys[self.attack_key] and self.attack_cooldown == 0:
            self.attack_cooldown = 30
            self.attack_zone_visible = 5
        
            if self.x < enemy.x:
                self.last_attack_zone = pygame.Rect(self.x + self.width, self.y, 50, 20)
            else:
                self.last_attack_zone = pygame.Rect(self.x - 50, self.y, 50, 20)
        
            if self.last_attack_zone.colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                enemy.health -= 10
            if enemy.health <= 0:
                enemy.health = 0
            hit_sound.play()

        # ======================
        # СПОСОБНОСТЬ
        # ======================
        if keys[self.ability_key] and self.ability_cooldown == 0:
            self.ability_cooldown = self.ability_max_cooldown
        
            if self.x < enemy.x:
                direction = 1
                projectile_x = self.x + self.width
            else:
                direction = -1
                projectile_x = self.x - 50
        
            projectile_y = self.y + self.height // 2 - 35
        
            projectiles_list.append(projectiles.Projectile(projectile_x, projectile_y, direction, self))

        # Таймер хитбокса
        if self.attack_zone_visible > 0:
            self.attack_zone_visible -= 1
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        if self.attack_zone_visible > 0 and self.last_attack_zone:
            attack_surface = pygame.Surface((self.last_attack_zone.width, self.last_attack_zone.height))
            attack_surface.set_alpha(128)
            attack_surface.fill((255, 0, 0))
            screen.blit(attack_surface, (self.last_attack_zone.x, self.last_attack_zone.y))
            pygame.draw.rect(screen, (255, 255, 0), self.last_attack_zone, 2)
    
    def draw_ui(self, screen, x_offset):
        font = pygame.font.Font(None, 36)
        
        name_text = font.render(self.name, True, self.color)
        screen.blit(name_text, (x_offset, 10))
        
        pygame.draw.rect(screen, (255, 0, 0), (x_offset, 50, 300, 30))
        pygame.draw.rect(screen, (0, 255, 0), (x_offset, 50, 300 * (self.health / 100), 30))
        
        health_text = font.render(f"HP: {self.health}/100", True, (255, 255, 255))
        screen.blit(health_text, (x_offset + 10, 52))
        
        if self.ability_cooldown > 0:
            cooldown_percent = (self.ability_max_cooldown - self.ability_cooldown) / self.ability_max_cooldown
            
            pygame.draw.rect(screen, (50, 50, 50), (x_offset, 90, 300, 20))
            pygame.draw.rect(screen, self.ability_color, (x_offset, 90, 300 * cooldown_percent, 20))
            
            cooldown_seconds = round(self.ability_cooldown / 60, 1)
            ability_text = font.render(f"Ability: {cooldown_seconds}s", True, (255, 255, 255))
            screen.blit(ability_text, (x_offset + 10, 88))
        else:
            pygame.draw.rect(screen, self.ability_color, (x_offset, 90, 300, 20))
            ability_text = font.render("Ability: READY!", True, (255, 255, 255))
            screen.blit(ability_text, (x_offset + 10, 88))