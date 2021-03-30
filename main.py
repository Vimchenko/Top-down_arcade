import pygame
import math
import random
import pygame.locals
import pygame.sprite
# инициализация модулей для PyGame
pygame.init()
pygame.mixer.init()
# настройка экрана
W = 700
H = 700
# частота кадров в секунду
FPS = 60
# определили оттенок чёрного цвета (для текста)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('FASTFIST')  # отображение названия игры
clock = pygame.time.Clock()

font_name = pygame.font.match_font('clarendon')  # шрифт


# функция, в которой мы определили параметры текста
def text_front(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# функция, отвечающая за содержимое экрана конца игры
def screen_of_the_end():
    screen.blit(background, [0, 0])
    text_front(screen, "Дабы начать игру, нажмите SPACE!", 35, W / 2, H * 1 / 4)
    text_front(screen, str(score), 50, W / 2, H * 2 / 3)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_file
        self.rect = self.image.get_rect()
        self.radius = 10
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
            self.speed_x = -14
        if keys[pygame.K_RIGHT]:
            self.speed_x = 14
        if keys[pygame.K_UP]:
            self.speed_y = -14
        if keys[pygame.K_DOWN]:
            self.speed_y = 14
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


class Trap(pygame.sprite.Sprite):
    def __init__(self, pace=10, turn_after=67):
        super().__init__()
        self.image = trap_file
        self.rect = self.image.get_rect()
        self.radius = 6
        self.direction = -1
        self.pace_count = 0
        self.turn_after = turn_after
        self.pace_size = pace
        trap_file.convert_alpha()

        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)

        self.speed = 25

        self.moving = True

    def horizontal_movement(self):
        self.pace_count += 1
        self.rect.x += self.direction * self.pace_size
        if self.pace_count >= self.turn_after:
            self.direction *= -1
            self.pace_count = 0
        if self.rect.x <= 0:
            self.direction = 1
            self.pace_count = 0
        elif self.rect.x >= W:
            self.direction = -1
            self.pace_count = 0

    def random(self):
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_file
        self.rect = self.image.get_rect()
        self.radius = 25
        enemy_file.convert_alpha()
        # появление врага в случайном месте экрана
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)

        self.speed_x = 11
        self.speed_y = 11

    # следование за игроком
    def follow_player(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed_x
        self.rect.y += dy * self.speed_y

    # отдельная функция случайного появления Врага для цикла hit_3
    def randomize(self):
        self.rect.x = random.randrange(0, W - self.rect.width)
        self.rect.y = random.randrange(0, H - self.rect.height)


background = pygame.image.load('background.jpg')
player_file = pygame.image.load('player.png')
enemy_file = pygame.image.load('enemy.png')
trap_file = pygame.image.load('trap.png')

all_sprites = pygame.sprite.Group()
player = Player()
enemy = Enemy()
trap = Trap()
all_sprites.add(player, enemy, trap)
# счётчик
score = 0
# цикл активностей игрового процесса
game_over = True
running = True
while running:
    if game_over:
        screen_of_the_end()
        score = 0  # обнуление счётчика после начала новой игры
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        enemy = Enemy()
        trap = Trap()
        all_sprites.add(player, enemy, trap)
    # держим цикл на нормальной скорости
    clock.tick(FPS)
    # ввод процесса (события)
    for event in pygame.event.get():
        # при выходе из игры, игровой процесс завершается
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  # обновление (дабы игрок видел передвижение спрайта)
    # соприкосновения между классами и циклы (if), отвечающие за результат от столкновений
    hit = pygame.sprite.collide_circle(player, enemy)
    hit_2 = pygame.sprite.collide_circle(player, trap)
    hit_3 = pygame.sprite.collide_circle(enemy, trap)
    if hit:
        game_over = True
    if hit_2:
        game_over = True
    if hit_3:
        enemy.randomize()
        trap.random()
        score += 1

    screen.blit(background, [0, 0])  # избавляет от "следов" при передвижении игрока
    all_sprites.draw(screen)   # отрисовка изображений на экране (для компьютера)
    enemy.follow_player(player)  # вызываем функию, отвечающую за слежение за игроком
    trap.horizontal_movement()  # вызываем функцию, отвечающую за горизонтальное передвижение ловушки
    pygame.display.flip()  # отображение игры игроку

pygame.quit()

''' ДОРАБОТАТЬ: 
   1) Передвижение Trap вверх-виз
   '''
