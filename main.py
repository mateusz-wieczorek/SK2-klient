import time
import tkinter

import pygame
import math
import socket
import struct
from tkinter import *
from functools import partial

from threading import Thread

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('CS2D')
player_image = pygame.image.load('arrow.png')
enemy_image = pygame.image.load('arrow_enemy.png')
ally_image = pygame.image.load('arrow_ally.png')
cursor_image = pygame.image.load('cursor.png')
background_image = pygame.image.load('background.png')

pygame.display.set_icon(player_image)

player_image = pygame.transform.rotate(player_image, 90)
player_image = pygame.transform.scale_by(player_image, 0.1)
enemy_image = pygame.transform.rotate(enemy_image, 90)
enemy_image = pygame.transform.scale_by(enemy_image, 0.1)
ally_image = pygame.transform.rotate(ally_image, 90)
ally_image = pygame.transform.scale_by(ally_image, 0.1)
cursor_image = pygame.transform.scale_by(cursor_image, 0.1)
cursor_image_rect = cursor_image.get_rect()
player_image_rect = player_image.get_rect()

pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
run = True

obstacles_centers = [(650, 650), (950, 1750), (1600, 1000), (2050, 2050), (1100, 2500)]
obstacles_radius = [150, 450, 400, 350, 200]


class Player:
    def __init__(self):
        self.name = 'name'
        self.pos_x = 400
        self.pos_y = 400
        self.angle = 0
        self.is_shooting = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.team = 0

    def move(self):
        obstacles_centers = [(650, 650), (950, 1750), (1600, 1000), (2050, 2050), (1100, 2500)]
        obstacles_radius = [150, 450, 400, 350, 200]
        players = game_status.split(";")[2:-1]
        for pl in players:
            if len(pl) == 0:
                continue
            player_data = pl.split(',')
            #if player_data[1] != player.name and player.team != player_data[2]:
            #    obstacles_centers.append((int(float(player_data[4])) + 38, int(float(player_data[5])) + 38))
            #    obstacles_radius.append(38)
        not_collided = 0
        temp_x = min(max(self.velocity_x * 10 + self.pos_x, 0 + WINDOW_WIDTH//2), background_image.get_width() -
                             WINDOW_WIDTH//2 - player_image.get_width())
        temp_y = min(max(self.velocity_y * 10 + self.pos_y, 0 + WINDOW_HEIGHT//2), background_image. get_height() -
                             WINDOW_HEIGHT//2 - player_image.get_height())
        for i in range(len(obstacles_centers)):
            if (temp_x + player_image.get_width() / 2 - obstacles_centers[i][0]) ** 2 + (
                    temp_y + player_image.get_height() / 2 - obstacles_centers[i][1]) ** 2 < (
                    obstacles_radius[i] + player_image.get_height() / 2) ** 2:
                break
            else:
                not_collided += 1

        if not_collided == len(obstacles_centers):
            self.pos_x = temp_x
            self.pos_y = temp_y

    def rotate(self,  topleft):
        global player_image
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # połowa szerokości gracza, aby obracać się wokół środka obrazka
        rel_x, rel_y = mouse_x - WINDOW_WIDTH//2 - player_image.get_width()//2, mouse_y - WINDOW_HEIGHT//2 - player_image.get_height()//2
        angle = (90 / math.pi) * -math.atan2(rel_y, rel_x)
        self.angle = angle
        rotated_player_image = pygame.transform.rotate(player_image, int(angle))
        rotated_image = pygame.transform.rotate(rotated_player_image, angle)
        new_rect = rotated_image.get_rect(center=player_image.get_rect(topleft=topleft).center)

        return rotated_image, new_rect


def rotate_other_player(topleft, angle, team):
    global ally_image
    global enemy_image
    if player.team == team:
        rotated_player_image = pygame.transform.rotate(ally_image, int(float(angle)))
    else:
        rotated_player_image = pygame.transform.rotate(enemy_image, int(float(angle)))
    rotated_image = pygame.transform.rotate(rotated_player_image, angle)
    new_rect = rotated_image.get_rect(center=enemy_image.get_rect(topleft=topleft).center)
    return rotated_image, new_rect


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

def draw_scene(game_status):
    global ally_image
    global enemy_image
    team_0_points = 0
    team_1_points = 0
    screen.blit(background_image, (0, 0), (player.pos_x - WINDOW_WIDTH // 2, player.pos_y - WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT))
    cursor_image_rect.center = pygame.mouse.get_pos()
    new_image, new_rect = player.rotate((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(new_image, new_rect)
    screen.blit(cursor_image, cursor_image_rect)
    players = game_status.split(";")[2:-1]
    # players_data = [el.split(",") for el in game_status.split(";")]
    for pl in players:
        if len(pl) == 0:
            continue
        player_data = pl.split(',')
        if player_data[1] == player.name:
            player.team = player_data[2]
            #print(player_data)
            #print(player.team)
        if player_data[1] != player.name:
            rotated_image, new_rect = rotate_other_player((400 - (player.pos_x - float(player_data[4])), 400 - (player.pos_y - float(player_data[5]))), int(float(player_data[6])), player_data[2])
            screen.blit(rotated_image, new_rect)
        if player_data[2] == '0':
            team_0_points += int(player_data[8])
            #print(0)
        if player_data[2] == '1':
            team_1_points += int(player_data[8])
            #print(1)
    if player.is_shooting == 1:
        pygame.draw.line(screen, WHITE, (WINDOW_WIDTH//2 + player_image.get_width()//2, WINDOW_HEIGHT//2 + player_image.get_height()//2), pygame.mouse.get_pos(), 2)

    font = pygame.font.Font('freesansbold.ttf', 16)
    try:
        text = font.render('TIME LEFT: ' + game_status.split(";")[1], False, WHITE, BLACK)
    except:
        text = font.render('waiting', False, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (WINDOW_WIDTH // 2, 20)
    screen.blit(text, textRect)
    your_team_text = font.render('YOU ARE TEAM ' + str(player.team), False, WHITE, BLACK)
    your_team_text_rect = your_team_text.get_rect()
    your_team_text_rect.center = (WINDOW_WIDTH//2, 40)
    screen.blit(your_team_text, your_team_text_rect)
    team_0_points_text = font.render('TEAM 0 POINTS: ' + str(team_0_points), False, WHITE, BLACK)
    team_0_points_text_rect = team_0_points_text.get_rect()
    team_0_points_text_rect.center = (120, 20)
    screen.blit(team_0_points_text, team_0_points_text_rect)
    team_1_points_text = font.render('TEAM 1 POINTS: ' + str(team_1_points), False, WHITE, BLACK)
    team_1_points_text_rect = team_0_points_text.get_rect()
    team_1_points_text_rect.center = (WINDOW_WIDTH - 120, 20)
    screen.blit(team_1_points_text, team_1_points_text_rect)
    pygame.display.update()


def get_input():
    global player
    global run
    global game_restart
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                player.is_shooting = 1
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] == 0:
                player.is_shooting = 0


def game_loop():
    global game_status
    global run, game_restart
    while run:
        print(game_status)
        get_input()
        player.move()
        clock.tick(60)
        draw_scene(game_status)
        #print(player.pos_x, player.pos_y)

root = Tk()


def join_game(name_var):
    connection.call_server(name_var.get())
    root.destroy()
    player.name = name_var.get()


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


def communicate_with_server():
    global game_status
    global connection
    global game_restart
    while game_restart:
        last_x = player.pos_x
        last_y = player.pos_y
        game_status = connection.call_server("3")
        game_status = connection.call_server(
            "1:" + str(last_x) + "," + str(last_y) + "," + str(player.angle) + "," + str(
                player.is_shooting))
        players = game_status.split(";")[2:-1]
        for pl in players:
            player_data = pl.split(',')
            if player_data[1] == player.name:
                if abs(last_x - float(player_data[4])) > 1:
                    player.pos_x =  float(player_data[4])
                    print('cos')
                if abs(last_y - float(player_data[5])) > 1:
                    player.pos_y = float(player_data[5])
    connection.call_server("2")


player = Player()
connection = Connection()
login_screen()
game_restart = True
game_status = ""

server_communication_thread = Thread(target=communicate_with_server)
server_communication_thread.start()
while game_restart:
    game_loop()
server_communication_thread.join()

pygame.quit()
quit()
