import pygame
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('CS2D')
player_image = (pygame.image.load('arrow.png'))
cursor_image = pygame.image.load('cursor.png')
background_image = pygame.image.load('background.png')

pygame.display.set_icon(player_image)

player_image = pygame.transform.rotate(player_image, 90)
player_image = pygame.transform.scale_by(player_image, 0.1)
cursor_image = pygame.transform.scale_by(cursor_image, 0.1)
cursor_image_rect = cursor_image.get_rect()
player_image_rect = player_image.get_rect()


pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
run = True


class Player:
    def __init__(self):
        self.name = 'name'
        self.pos_x = 400
        self.pos_y = 400
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        self.pos_x = min(max(self.velocity_x * 10 + self.pos_x, 0 + WINDOW_WIDTH//2), background_image.get_width() -
                         WINDOW_WIDTH//2 - player_image.get_width())  #min i max aby nie wyjść poza ekran
        self.pos_y = min(max(self.velocity_y * 10 + self.pos_y, 0 + WINDOW_HEIGHT//2), background_image. get_height() -
                         WINDOW_HEIGHT//2 - player_image.get_height())
        #print(self.pos_x, self.pos_y, pygame.mouse.get_pos())

    def rotate(self,  topleft):
        global player_image
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # połowa szerokości gracza, aby obracać się wokół środka obrazka
        rel_x, rel_y = mouse_x - WINDOW_WIDTH//2 - player_image.get_width()//2, mouse_y - WINDOW_HEIGHT//2 - player_image.get_height()//2
        angle = (90 / math.pi) * -math.atan2(rel_y, rel_x)
        rotated_player_image = pygame.transform.rotate(player_image, int(angle))
        rotated_image = pygame.transform.rotate(rotated_player_image, angle)
        new_rect = rotated_image.get_rect(center=player_image.get_rect(topleft=topleft).center)

        return rotated_image, new_rect

player = Player()


def game_loop():
    global run, game_restart
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_restart = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.velocity_y = -1
                if event.key == pygame.K_s:
                    player.velocity_y = 1
                if event.key == pygame.K_a:
                    player.velocity_x = -1
                if event.key == pygame.K_d:
                    player.velocity_x = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.velocity_y = 0
                if event.key == pygame.K_s:
                    player.velocity_y = 0
                if event.key == pygame.K_a:
                    player.velocity_x = 0
                if event.key == pygame.K_d:
                    player.velocity_x = 0
        player.move()
        screen.blit(background_image, (0, 0), (player.pos_x - WINDOW_WIDTH//2, player.pos_y - WINDOW_HEIGHT//2, WINDOW_WIDTH, WINDOW_HEIGHT))
        cursor_image_rect.center = pygame.mouse.get_pos()
        new_image, new_rect = player.rotate((WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(new_image, new_rect)
        screen.blit(cursor_image, cursor_image_rect)
        clock.tick(60)
        pygame.display.update()

game_restart = True
while game_restart:
    game_loop()
pygame.quit()
quit()
