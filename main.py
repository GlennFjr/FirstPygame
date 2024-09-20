from typing import Self
import pygame
from sys import exit
import random
from random import randint, choice
#Self.music.play()
#Self.music = pygame.mixer.Sound('graphics/Avenged Sevenfold - Blinded In Chains [Instrumental].mp3')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/walk1.png').convert_alpha()
        player_walk_1 = pygame.transform.scale(player_walk_1, (60, 80))
        player_walk_2 = pygame.image.load('graphics/walk2.png').convert_alpha()
        player_walk_2 = pygame.transform.scale(player_walk_2, (60, 80))
        player_jump = pygame.image.load('graphics/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.player_jump = pygame.transform.scale(player_jump, (60, 80))

        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0



    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('graphics/bat1.png').convert_alpha()
            bat_2 = pygame.image.load('graphics/bat2.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 210
        else:
            knight_1 = pygame.image.load('graphics/knight1.png').convert_alpha()
            knight_2 = pygame.image.load('graphics/knight2.png').convert_alpha()
            knight_1 = pygame.transform.rotozoom(knight_1, 0, 2)
            knight_2 = pygame.transform.rotozoom(knight_2, 0, 2)
            self.frames = [knight_1, knight_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -50:
            self.kill()

#     def destroy(self):
#         if self.rect.x <= -50 or self.rect.x >= 850 or self.rect.y <= -50 or self.rect.y >= 450:
#             self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render('Score: ' + str(current_time), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# def obstacle_movement(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#
#             if obstacle_rect.bottom == 300:
#                 screen.blit(knight_surf, obstacle_rect)
#             else:
#                 screen.blit(bat_surf, obstacle_rect)
#
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#
#         return obstacle_list
#     else:
#         return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# def player_animation():
#     global player_surf, player_index
#
#     if player_rect.bottom < 300:
#         player_surf = player_jump
#     else:
#         player_index += 0.1
#         if player_index >= len(player_walk):
#             player_index = 0
#         player_surf = player_walk[int(player_index)]
#     # Play walking animation if player is on the floor
#     # Play jumping animation if player is off the floor


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('My Python Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Fancy.otf', 50)
game_active = False
start_time = 0
score = 0
# bg_Music = pygame.mixer.Sound('graphics/Avenged Sevenfold - Blinded In Chains [Instrumental].mp3')
# bg_Music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

background_surface = pygame.image.load('graphics/back.jpg').convert()
ground_surface = pygame.image.load('graphics/ground.jpg').convert()

# text_surf = test_font.render('My game', False, (64, 64, 64))
# text_rect = text_surf.get_rect(center=(400, 50))

# Knight
knight_frame_1 = pygame.image.load('graphics/knight1.png').convert_alpha()
knight_frame_2 = pygame.image.load('graphics/knight2.png').convert_alpha()
knight_frame_1 = pygame.transform.rotozoom(knight_frame_1, 0, 2)
knight_frame_2 = pygame.transform.rotozoom(knight_frame_2, 0, 2)
knight_frames = [knight_frame_1, knight_frame_2]
knight_index = 0
knight_surf = knight_frames[knight_index]

# Bat
bat_frame1 = pygame.image.load('graphics/bat1.png').convert_alpha()
bat_frame2 = pygame.image.load('graphics/bat2.png').convert_alpha()
bat_frames = [bat_frame1, bat_frame2]
bat_index = 0
bat_surf = bat_frames[bat_index]

obstacle_rect_list = []

#Player
player_walk_1 = pygame.image.load('graphics/walk1.png').convert_alpha()
player_walk_1 = pygame.transform.scale(player_walk_1, (60, 80))
player_walk_2 = pygame.image.load('graphics/walk2.png').convert_alpha()
player_walk_2 = pygame.transform.scale(player_walk_2, (60, 80))
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/jump.png').convert_alpha()
player_jump = pygame.transform.scale(player_jump, (60, 80))

player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Screen
titleman_surf = pygame.image.load('graphics/TitleMan.png')
titleman_surf = pygame.transform.rotozoom(titleman_surf, 0, 0.75)
titleman_rect = titleman_surf.get_rect(center=(400, 170))

game_name = test_font.render('Run Man', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 50))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

knight_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(knight_animation_timer, 400)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #User Input
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        # Timers
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bat', 'knight', 'knight', 'knight'])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(knight_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(knight_surf.get_rect(bottomright=(randint(900, 1100), 200)))
            if event.type == knight_animation_timer:
                if knight_index == 0:
                    knight_index = 1
                else:
                    knight_index = 0
                knight_surf = knight_frames[knight_index]
            if event.type == bat_animation_timer:
                if bat_index == 0:
                    bat_index = 1
                else:
                    bat_index = 0
                bat_surf = bat_frames[bat_index]

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', text_rect)
        # pygame.draw.rect(screen, '#c0e8ec', text_rect, 10)
        # screen.blit(text_surf, text_rect)
        score = display_score()

        # Knight
        # knight_rect.x -= 6
        # if knight_rect.right <= 0:
        #     knight_rect.left = 800
        # screen.blit(knight_surf, knight_rect)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacles
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(titleman_surf, titleman_rect)
        obstacle_rect_list.clear()
        # player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render('Your score: ' + str(score), False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 350))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
