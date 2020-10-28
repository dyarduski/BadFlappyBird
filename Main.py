import pygame
import random
pygame.init()

class IBird:
    def __init__(self):
        self.moving_down = True
        self.Bird_DownFlap = pygame.image.load("sprites\\yellowbird-downflap.png").convert()
        self.Bird_MidFlap = pygame.image.load("sprites\\yellowbird-midflap.png").convert()
        self.Bird_UpFlap = pygame.image.load("sprites\\yellowbird-upflap.png").convert()
        self.Bird_rect = self.Bird_MidFlap.get_rect(center=(370/3-33,570/2))
        self.selected_bird = self.Bird_MidFlap

def draw_bird(Bird,gravity):
    gravity += strength
    Bird.Bird_rect.centery += gravity

    if Bird.moving_down:
        Bird.selected_bird = Bird.Bird_DownFlap
    Bird.moving_down = True
    screen.blit(Bird.selected_bird,Bird.Bird_rect)
    return gravity

def MovingPipe(Pipe_List):
    for Pipe_rect in Pipe_List:
        Pipe_rect.centerx -= 2.05

    for Pipe_rect in Pipe_List:
        if Pipe_rect.bottom >= 570:
            screen.blit(Pipe,Pipe_rect)
        else:
            screen.blit(flip_pipe,Pipe_rect)
        if Pipe_rect.colliderect(Bird.Bird_rect):
            print("Trash die")
            exit()
    return Pipe_List

def MakePipe():
    y = random.randint(415,533)
    new = Pipe.get_rect(center=(385,y))
    down_new = Pipe.get_rect(center=(385,y - 437))
    return new,down_new



Width,Height = 370,570
gravity = 0
strength = 0.3
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

Background = pygame.image.load("sprites\\background-day.png").convert()
Background = pygame.transform.scale(Background, (Width, Height))

Floor = pygame.image.load("sprites\\base.png").convert()
Floor = pygame.transform.scale(Floor, (Width, Floor.get_height()))
Floor_x = 0

Pipe = pygame.image.load("sprites\\pipe-green.png").convert()
flip_pipe = pygame.transform.flip(Pipe,False,True)
Pipe_List = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1250)

Bird = IBird()


while True:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == 12:
            exit()
        if event.type == SPAWNPIPE:
            Pipe_List.extend(MakePipe())
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                gravity = 0
                gravity -= 5.26
                Bird.selected_bird = Bird.Bird_UpFlap
                Bird.moving_down = False
    if gravity < 0:
        Bird.moving_down = False

    screen.blit(Background,(0,0))
    gravity = draw_bird(Bird,gravity)
    Pipe_List = MovingPipe(Pipe_List)
    Floor_x -= 2.1
    screen.blit(Floor,(Floor_x,Height-112))
    screen.blit(Floor,(Floor_x+Floor.get_width(),Height-112))
    if Floor_x <= -Floor.get_width():
        Floor_x = 0
   

    pygame.display.update()