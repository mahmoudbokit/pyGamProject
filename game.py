
import pygame
import pytmx
import pyscroll

from player import Player


class Game:
    def __init__(self):

        # Creer la fenetre du jeu (Создание окна игры)
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("MyPygame - Aventure")

        # Charger la carte(tmx) (Загрузка карты (tmx))
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Générer un joueur (Создание игрока)
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Definir une liste qui va stocker les rectangles de collision
        # Определите список, в котором будут храниться прямоугольники столкновений
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques (Нарисуйть группу слоев)
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.group.update()

        # Verification de collision (Проверка на столкновение)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # La boucle du jeu (Цикл игры)
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

        pygame.quit()