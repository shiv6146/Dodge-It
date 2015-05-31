import pygame
import time
import random


pygame.init()

crash_sound = pygame.mixer.Sound('Your music file for crash') #suitable music file is .wav 

display_width = 800
display_height = 600
car_width = 73

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Dodge It!!!")

black = (0,0,0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

clock = pygame.time.Clock()
carImg = pygame.image.load('racecar.png')
pause = False

def unpause():
        global pause
        pause = False
        pygame.mixer.music.unpause()

def paused():
        pygame.mixer.music.pause()
        
        lg_txt = pygame.font.SysFont('freesansbold', 115)
        txt_surf, txt_rect = text_objects("Paused", lg_txt)
        txt_rect.center = ((display_width/2),(display_height/2))
        screen.blit(txt_surf, txt_rect)

        while pause:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_game()

                button("Continue",150,450,100,50,green,bright_green,unpause)
                button("Quit",550,450,100,50,red,bright_red,quit_game)

                pygame.display.update()
                clock.tick(15)

def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
                pygame.draw.rect(screen, ac, (x,y,w,h))
                if click[0] == 1 and action != None:
                        action()
        else:
                pygame.draw.rect(screen, ic, (x,y,w,h))

        sm_txt = pygame.font.Font('freesansbold.ttf', 20)
        txt_surf, txt_rect = text_objects(msg, sm_txt)
        txt_rect.center = ((x+(w/2)), (y+(h/2)))
        screen.blit(txt_surf, txt_rect)

def things_dodged(count):
        font = pygame.font.SysFont(None, 25)
        txt = font.render("Dodged: "+str(count), True, black)
        screen.blit(txt, (0,0))

def things(thing_x, thing_y, thing_w, thing_h, color):
        pygame.draw.rect(screen, color, [thing_x, thing_y, thing_w, thing_h])


def car(x,y):
        screen.blit(carImg, (x,y))

def crash():
        pygame.mixer.Sound.play(crash_sound)
        pygame.mixer.music.stop()
        
        message_display('You crashed')

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit_game()

                button("Play",150,450,100,50,green,bright_green,game_loop)
                button("Quit",550,450,100,50,red,bright_red,quit_game)

                pygame.display.update()
                clock.tick(15)

def message_display(text):
        lg_txt = pygame.font.Font('freesansbold.ttf',115)
        txt_surf, txt_rect = text_objects(text, lg_txt)
        txt_rect.center = ((display_width/2), (display_height/2))
        screen.blit(txt_surf, txt_rect)
        pygame.display.update()
        time.sleep(2)

def text_objects(text, font):
        txt_surf = font.render(text, True, black)
        return txt_surf, txt_surf.get_rect()

def game_intro():
        intro = True

        while intro:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                screen.fill(white)
                lg_txt = pygame.font.Font('freesansbold.ttf', 115)
                txt_surf, txt_rect = text_objects("Dodge It!!!", lg_txt)
                txt_rect.center = ((display_width/2), (display_height/2))
                screen.blit(txt_surf, txt_rect)

                button("GO!",150,450,100,50,green,bright_green,game_loop)
                button("QUIT!",550,450,100,50,red,bright_red,quit_game)

                pygame.display.update()
                clock.tick(15)

def game_loop():
        pygame.mixer.music.load('Your music file for game theme') #suitable music file type .wav
        pygame.mixer.music.play(-1)
        
        x = (display_width*0.45)
        y = (display_height*0.8)

        x_chng = 0

        thing_strt_x =  random.randrange(0, display_width)
        thing_strt_y = -600
        thing_speed = 4
        thing_width = 100
        thing_height = 100
        thing_count = 1
        dodged = 0

        crashed = False

        while not crashed:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        x_chng = -5
                                if event.key == pygame.K_RIGHT:
                                        x_chng = 5
                                if event.key == pygame.K_p:
                                        global pause
                                        pause = True
                                        paused()
                        
                        if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                        x_chng = 0
                x += x_chng
                
                screen.fill(white)

                things(thing_strt_x, thing_strt_y, thing_width, thing_height, red)
                thing_strt_y += thing_speed
                car(x,y)
                things_dodged(dodged)

                if x > display_width-car_width or x < 0:
                        crash()

                if thing_strt_y > display_height:
                        thing_strt_y = 0 - thing_height
                        thing_strt_x = random.randrange(0, display_width)
                        dodged += 1
                        thing_speed += 1
                        #thing_width += (dodged * 1.2)

                if y < thing_strt_y+thing_height:
                        #print 'y crossover'

                        if x > thing_strt_x and x < thing_strt_x+thing_width or x+car_width > thing_strt_x and x+car_width < thing_strt_x+thing_width:
                                #print 'x crossover'
                                crash()
                        
                pygame.display.update()
                clock.tick(60)

def quit_game():
        pygame.quit()
        quit()

game_intro()
game_loop()
pygame.quit()
quit()
