# Instructions:
# pip install pygame
# run code

# Imports
import pygame # pygame library
from sys import exit # closes any kind of code once it's called
from random import choice, randint 
import random

# Player/Enemies

class Cowboy(pygame.sprite.Sprite): # Player sprite (Sprite is class that contains a surface and a rectangle, and it can be drawn and updated very easily)

   def __init__(self):
      super().__init__()
      self.image = pygame.image.load('thegame/characters/cowboy_1.png').convert_alpha() # load player image
      self.rect = self.image.get_rect(midbottom = (100,370)) # create a rectangle around image. 1 argument - cooridates (on screen)
      self.gravity = 0 # default gravity for player
      self.jump_sound = pygame.mixer.Sound("thegame/audio/jump_1.mp3") # add sound file to self.variable
      self.jump_sound.set_volume(0.9) # set volume for the sound

   def cowboy_input(self):
      keys = pygame.key.get_pressed() # key.get_pressed = if any key is pressed down
      if keys[pygame.K_SPACE] and self.rect.bottom >= 370: # if key is space and player rectangle is on ground (ground y axis is 370)
         self.gravity = -18 # jump mechanics
         self.jump_sound.play() # play sound effect/audio

   def apply_gravity(self): 
      self.gravity += 1
      self.rect.y += self.gravity
      if self.rect.bottom >= 370: # if player hits ground
         self.rect.bottom = 370 #  spawn it back on ground (to prevent falling out of screen)

   def update(self):
      self.cowboy_input() # if loop ends, update player
      self.apply_gravity() # update gravity every next loop

class Obstacle(pygame.sprite.Sprite): # Obstacle sprite (Sprite is class that contains a surface and a rectangle, and it can be drawn and updated very easily)
   def __init__(self,type):
      super().__init__()

      if type == "banana":
         banana_1 = pygame.image.load('thegame/characters/banana_1.png').convert_alpha() # load image of banana
         banana_2 = pygame.image.load('thegame/characters/banana_2.png').convert_alpha() # .convert_alpha() to run image smoother (optional)
         self.frames = [banana_1, banana_2] # add frames of images in one list
         y_pos = 270 # default y axis position for banana object
      else:
         monkey_1 = pygame.image.load('thegame/characters/monkey_1.png').convert_alpha() # load image of monkey
         monkey_2 = pygame.image.load('thegame/characters/monkey_2.png').convert_alpha() # .convert_alpha() to run image smoother (optional)
         self.frames =  [monkey_1, monkey_2]  add frames of images in one list
         y_pos = 370 # default y axis position for monkey object

      self.animation_index = 0 # default
      self.image = self.frames[self.animation_index]
      self.rect = self.image.get_rect(midbottom = (random.randint(900,1300), y_pos)) # rectangle for image. random.randint to spawn obstacles on random time

   def animation_state(self): # animation effect with 2 frames
      self.animation_index += 0.1
      if self.animation_index >= len(self.frames): self.animation_index = 0
      self.image = self.frames[int(self.animation_index)]

   def update(self):
      self.animation_state() # update animation every loop
      self.rect.x -= 6 # move obstacles left (+ to move right)
      self.destroy() # if obstacle is out of left side, destory it

   def destroy(self):
      if self.rect.x <= -100: # if obstacle is out of screen
         self.kill() # destory sprite
   
# Score display

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # time in milliseconds and subtract start_time to zero time again. divise with 1000 to convert milliseconds
    score_surface = font1.render(f'Score: {current_time}',False,(200,64,100)) # 3 arguments- time, anti aliasing, color. # anti aliasing - smooth the edges of the text . False - when pixel art
    score_rect = score_surface.get_rect(center = (450,70)) # x, y axis (width,height)
    screen.blit(score_surface,score_rect)
   
    return current_time

# Obstacle movement/collision

def obstacle_movement(obstacle_list):
   if obstacle_list:  # this statement is True if atleast one element is in [] . If list is empty, Python sees it as False, so it won't run
      for obstacle_rect in obstacle_list:
          obstacle_rect.x -= 5 # move obstacles by x axis, 5 pixels per loop

          if obstacle_rect.bottom == 370: # if enemy is equal to gorund
             screen.blit(monkey_surface, obstacle_rect) # draw monkey
          else:
             screen.blit(banana_surface, obstacle_rect) # if not, draw banana

      obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # list comperhension. if obstacle is out of screen, delete it
      return obstacle_list
   
   else: return [] # return empty list. important to add to prevent AttributeError (NoneType)

def collisions(cowboy, obstacles):
   if obstacles:
      for obstacle_rect in obstacles:
         if cowboy.colliderect(obstacle_rect): return False # if collision, game_active = False
   return True # if no collision yet, game_active = True

def collision_sprite():
  death_sound = pygame.mixer.Sound("thegame/audio/death_1.mp3")
  if pygame.sprite.spritecollide(cowboy.sprite,obstacle_group, False): # 3 argumements - sprite, group, bool(is destroyed or not?(True/False))
     death_sound.play()
     obstacle_group.empty() # empty all obstacles if collision
     return False
  else: return True

# Game display/screen  
pygame.init() # starts pygame (render images, play sounds, ...)
pygame.display.set_caption("The game") # caption for program
screen = pygame.display.set_mode((900,500)) # display surface. must contain one argument as a tuple (width,height)
clock = pygame.time.Clock() # helps with time and controlling framerate
game_active = False
start_time = 0
score = 0 

# Groups
cowboy = pygame.sprite.GroupSingle() # Group
cowboy.add(Cowboy()) # Sprite

obstacle_group = pygame.sprite.Group()

# Map surfaces/font/rectangles

font1 = pygame.font.Font('thegame/font/Pixeltype.ttf', 100) # 2 arguments - font type, font size. default = None
sky_surface = pygame.image.load('thegame/graphics/sky_1.jpg').convert_alpha() # any time you import an image into pygame you're gonna put it on a separate surface(every graphical import is new surface)
ground_surface = pygame.image.load('thegame/graphics/ground_1.png').convert_alpha() # optional .convert_alpha - smoother image load

# Characters

# Monkey
monkey_frame_1 = pygame.image.load('thegame/characters/monkey_1.png').convert_alpha() # load image of monkey
monkey_frame_2 = pygame.image.load('thegame/characters/monkey_2.png').convert_alpha()
monkey_frames = [monkey_frame_1,monkey_frame_2]
monkey_frame_index = 0
monkey_surface = monkey_frames[monkey_frame_index]

# Banana
banana_frame_1 = pygame.image.load('thegame/characters/banana_1.png').convert_alpha() # load image of banana
banana_frame_2 = pygame.image.load('thegame/characters/banana_2.png').convert_alpha()
banana_frames = [banana_frame_1, banana_frame_2]
banana_frame_index = 0
banana_surface = banana_frames[banana_frame_index]

obstacle_rect_list = [] # monkey and banana movement

# Cowboy
cowboy_surface = pygame.image.load('thegame/characters/cowboy_1.png').convert_alpha() # load image of cowboy
cowboy_rect = cowboy_surface.get_rect(midbottom = (100,370)) # get_rect creates rectangle around cowboy surface
cowboy_gravity = 0 # cowboy default gravity

# Intro screen
cowboy_stand = pygame.image.load('thegame/characters/cowboy_1.png').convert_alpha()
cowboy_stand = pygame.transform.rotozoom(cowboy_stand,70, 2) # rotozoom- resize and rotate surface. 3 arguments- (surface,angle,scale size)
cowboy_stand_rect = cowboy_stand.get_rect(center = (450,250)) # rectangle of cowboy intro screen

game_title = font1.render("Monkey hates cowboy",False,(30,50,100)) # rendering text. 3 arguments (text, anti aliasing, color)
game_title_rect = game_title.get_rect(center = (450,100))

game_message = font1.render("Press space to start",False,(250,60,60)) # renderiing text. 3 arguments (text, anti aliasing, color)
game_message_rect = game_message.get_rect(center = (450, 420))

# Timers
obstacle_timer = pygame.USEREVENT + 1 # USEREVENT + 1 to create timer. + 1 is important to add.
pygame.time.set_timer(obstacle_timer, 1500) # 2 arguments- event you want to trigger, how often you want to trigger in millisecond

monkey_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(monkey_animation_timer, 500)

banana_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(banana_animation_timer,200)

# Event loop

while True: # when exit() is called, while True loop will be gone
    for event in pygame.event.get(): # loop for all possible events in game
        if event.type == pygame.QUIT: # QUIT is common event type
           pygame.quit() # opposite of pygame.init()
           exit()
       
        if game_active:

            if event.type == pygame.MOUSEBUTTONDOWN: # if any key on mouse is pressed down
               if event.key == pygame. and cowboy_rect.bottom >= 370: # if mouse is pressed down and cowboy rectangle is equal to ground y axis
                  cowboy_gravity = -20  
                
            if event.type == pygame.KEYDOWN: # if any key on keyboard is pressed down
               if event.key == pygame.K_SPACE and cowboy_rect.bottom >= 370: # if space is pressed down and cowboy rectangle is equal to ground y axis
                  cowboy_gravity = -20  # player jump mechanics
        
        # Restart game (SPACE)
        else:
           if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # if space is pressed down
              game_active = True # start/restart game
              start_time = int(pygame.time.get_ticks() / 1000) # restart time to 0 

        # Movement
        if game_active:
            if event.type == obstacle_timer and game_active:
                if randint(0,2): # True(1) or False(0)
                 obstacle_group.add(Obstacle(choice(["banana","monkey,","monkey","monkey"]))) # 75% to spawn monkey, 25% to spawn banana
                else:
                   obstacle_group.add(Obstacle("banana"))
             #  if randint(0,2): # True(1) or False(0)
              #    obstacle_rect_list.append(monkey_surface.get_rect(bottomright = (randint(1000,1200),370))) # add new position to obstacle_rect_list. # get_rect creates rectangle around monkey surface
              # else:
              #    obstacle_rect_list.append(banana_surface.get_rect(bottomright = (randint(1000,1200),270)))
                  
            if event.type == monkey_animation_timer:
               if monkey_frame_index == 0: monkey_frame_index = 1
              
               else: monkey_frame_index = 0
               monkey_surface = monkey_frames[monkey_frame_index]
           
            if event.type == banana_animation_timer:
               if banana_frame_index == 0: banana_frame_index = 1
              
               else: banana_frame_index = 0
               banana_surface = banana_frames[banana_frame_index]
                  

    if game_active: # game_active by default is False
            
        # Surfaces on screen
        screen.blit(sky_surface,(0,0)) # .blit - put one surface on another surface. 2 arguments required - surface, position
        screen.blit(ground_surface,(0,370))
        score = display_score() # actual score

        # Enemy(monkey)
       # monkey_rect.x -= 5 # make monkey move to left . move by x axis
       # if monkey_rect.right <= 0: # if monkey rectangle right side is out of left side of screen :
        #  monkey_rect.left = 900  # put monkey rectangle left side out of right side of screen
       # screen.blit(monkey_surface, monkey_rect)
        
        # Player(cowboy)
      #  cowboy_gravity += 1
      #  cowboy_rect.y += cowboy_gravity # player rectangle.y(y axis to fall down)
       # if cowboy_rect.bottom >= 370: # if cowboy rectangle bottom is greater than ground y surface :
        #  cowboy_rect.bottom = 370 #  put it back on ground 
       # screen.blit(cowboy_surface, cowboy_rect)
        
        cowboy.draw(screen) # draw sprite
        cowboy.update() # update sprite
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
      #  obstacle_rect_list = obstacle_movement(obstacle_rect_list) # overwrite 

        # Collision
        game_active = collision_sprite()
      #  game_active = collisions(cowboy_rect, obstacle_rect_list) # if there is collison, return False. so game is not active anymore

    else:
        screen.fill((110,90,140)) # rgb colors # any color name in string works aswell , example "Blue"
        screen.blit(game_title,game_title_rect) # display game name at intro/death menu
        obstacle_rect_list.clear() # clear movement of obstacles
        cowboy_rect.midbottom = (100,370) # restart cowboy position to ground
        cowboy_gravity = 0 # restart gravity
        
        # Intro screen
        if score == 0: # score starts from 0
           screen.blit(game_message,game_message_rect) # display message "Press space to start"
           screen.blit(monkey_surface, (500,220))
           screen.blit(cowboy_surface, (300,200))
        
        # Death/Score screen
        else: # if score greater than 0
           score_message = font1.render(f"Your score: {score}",False,(250,60,60))
           score_message_rect = score_message.get_rect(center = (450,350))
           screen.blit(cowboy_stand,cowboy_stand_rect) # display cowboy at intro/death menu
           screen.blit(score_message, score_message_rect) # display score message

     # Display/FPS
    pygame.display.update() # updates everything in "screen" variable
    clock.tick(60) # tells while True loop that game should not run faster than 60fps
