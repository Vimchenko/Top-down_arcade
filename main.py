import pygame
import math
import random
import pygame.locals
import pygame.sprite
# инициализация модулей для PyGame
pygame.init()
# настройка экрана
W = 600
H = 600
# частота кадров в секунду
FPS = 60

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('OOP')  # отображение названия игры
background = pygame.image.load('background.jpg')
player_file = pygame.image.load('player.png')
enemy_file = pygame.image.load('enemy.png')
trap_file = pygame.image.load('trap.png')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_file
        self.rect = self.image.get_rect()
        player_file.convert_alpha()
        # поялвение игрока в случайном месте экрана
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)

        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        # реализация передвижения игрока (стрелки)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -8
        if keys[pygame.K_RIGHT]:
            self.speed_x = 8
        if keys[pygame.K_UP]:
            self.speed_y = -8
        if keys[pygame.K_DOWN]:
            self.speed_y = 8
        # границы для передвижения игрока
        self.rect.x += self.speed_x
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += self.speed_y
        if self.rect.bottom > H:
            self.rect.bottom = H
        if self.rect.top < 0:
            self.rect.top = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_file
        self.rect = self.image.get_rect()
        enemy_file.convert_alpha()
        # появление врага в случайном месте экрана
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)

        self.speed_x = 8
        self.speed_y = 8

    def follow_player(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed_x
        self.rect.y += dy * self.speed_y


class Trap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = trap_file
        self.rect = self.image.get_rect()
        trap_file.convert_alpha()


all_sprites = pygame.sprite.Group()
player = Player()
enemy = Enemy()
trap = Trap()
all_sprites.add(player, enemy, trap)

running = True
while running:
    # держим цикл на нормальной скорости
    clock.tick(FPS)
    # ввод процесса (события)
    for event in pygame.event.get():
        # при выходе из игры, игровой процесс завершается
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, [0, 0])  # избавляет от "следов" при передвижении игрока
    all_sprites.update()  # обновление (дабы игрок видел передвижение спрайта)
    all_sprites.draw(screen)   # отрисовка изображений на экране (для компьютера)
    enemy.follow_player(player)  # вызываем функию, отвечающую за слежение за игроком
    pygame.display.flip()  # отображение игры игроку

pygame.quit()
