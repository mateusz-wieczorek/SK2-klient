import time
import tkinter

import pygame
import math
import socket
import struct
from tkinter import *
from functools import partial

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


class Connection():
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 4000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def __del__(self):
        self.socket.close()

    def call_server(self, message):
        message_length = len(message)
        encoded_message_length = struct.pack('!H', message_length)
        self.socket.send(encoded_message_length)
        self.socket.send(message.encode())
        received_data_length = self.socket.recv(2)
        received_uint16 = struct.unpack('!H', received_data_length)[0]
        server_response = self.socket.recv(received_uint16).decode()
        return server_response


def draw_scene():
    screen.blit(background_image, (0, 0), (player.pos_x - WINDOW_WIDTH // 2, player.pos_y - WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT))
    cursor_image_rect.center = pygame.mouse.get_pos()
    new_image, new_rect = player.rotate((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(new_image, new_rect)
    screen.blit(cursor_image, cursor_image_rect)
    pygame.display.update()


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
        draw_scene()
        clock.tick(60)


root = Tk()

connection = Connection()

def join_game(name_var):
    connection.call_server(name_var.get())
    root.destroy()
    #connection.call_server()

def login_screen():
    name_var = tkinter.StringVar(root, value='username')
    root.geometry("400x400")
    name_entry = Entry(root, textvariable=name_var)
    name_entry.place(relx=0.5, rely=0.4, anchor=CENTER)
    name_label = Label(root, text="Username", font=("Helvetica", 11))
    name_label.place(relx=0.5, rely=0.3, anchor=CENTER)
    enter_button = Button(root, text="Join the game!", command=partial(join_game, name_var))
    enter_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()


login_screen()
game_restart = True
while game_restart:
    game_loop()
pygame.quit()
quit()
