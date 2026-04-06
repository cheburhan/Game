import pygame
import settings
pygame.mixer.init()
fire_sound = pygame.mixer.Sound("0406.MP3")
fire_sound.set_volume(0.7)

class Projectile:
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y - 10  # Поднимаем снаряд чуть выше, чтобы он не рождался в ногах бойца
        self.width = 40      
        self.height = 40
        self.direction = direction  # 1 - вправо, -1 - влево
        self.speed = 8       # [НОВОЕ] Не быстрая скорость
        self.owner = owner   # Кто запустил снаряд
        self.damage = 40     # [НОВОЕ] Отнимает 40 HP
        self.active = True   # Активен ли снаряд
        self.WIDTH = settings.WIDTH   # Ширина экрана
        fire_sound.play()
        
    def update(self, enemy):
        if not self.active:
            return
            
        # Движение снаряда
        self.x += self.speed * self.direction
        
        # Проверка попадания в противника
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        

        
        if projectile_rect.colliderect(enemy_rect):
            enemy.health -= self.damage
            if enemy.health <= 0:
                enemy.health = 0
            self.active = False  # Снаряд исчезает после попадания
            
        # Проверка выхода за пределы экрана
        if self.x + self.width < 0 or self.x > settings.WIDTH:
            self.active = False
    
    def draw(self, screen):
        if self.active:
            # [НОВОЕ] Рисуем снаряд (красный цвет, видимый)
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
            # [НОВОЕ] Добавляем эффект свечения (обводка для красоты)
            pygame.draw.rect(screen, (255, 100, 0), (self.x, self.y, self.width, self.height), 3)
