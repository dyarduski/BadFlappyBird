import pygame
import random

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

class IBird:
    def __init__(self):
        self.moving_down = True
        self.Bird_DownFlap = pygame.image.load("sprites\\yellowbird-downflap.png")
        self.Bird_MidFlap = pygame.image.load("sprites\\yellowbird-midflap.png")
        self.Bird_UpFlap = pygame.image.load("sprites\\yellowbird-upflap.png")
        self.Bird_rect = self.Bird_MidFlap.get_rect(center=(370/3-33,570/2))
        self.selected_bird = self.Bird_MidFlap
        self.R = None

def draw_bird(Bird,gravity):
    x = lambda:pygame.transform.rotate(Bird.selected_bird,-gravity * 3.25)
    Bird.R = x()
    gravity += strength
    Bird.Bird_rect.centery += gravity

    if Bird.moving_down:
        Bird.selected_bird = Bird.Bird_DownFlap
    Bird.moving_down = True
    screen.blit(Bird.R,Bird.Bird_rect)
    return gravity

def MovingPipe(Pipe_List):
    global Alive
    for Pipe_rect in Pipe_List:
        Pipe_rect.centerx -= 2.05
    for Pipe_rect in Pipe_List:
        if Pipe_rect.bottom >= 570:
            screen.blit(Pipe,Pipe_rect)
        else:
            screen.blit(flip_pipe,Pipe_rect)
        if Pipe_rect.colliderect(Bird.Bird_rect):
            death_sound.play()
            Alive = False

    return Pipe_List

def MakePipe():
    y = random.randint(415,533)
    new = Pipe.get_rect(center=(385,y))
    down_new = Pipe.get_rect(center=(385,y - 437))
    return new,down_new

def Render():
    if Alive:
        ToRender = Score_font.render(f"Score: {int(score)}",True,(255,255,255))
        screen.blit(ToRender,(Width/2-35,42))
    elif not Alive:
        ToRender1 = Score_font.render(f"Score: {int(score)}",True,(255,255,255))
        screen.blit(ToRender1,(Width/2-35,42))
        ToRender2 = Score_font.render("Press space to play again",True,(255,255,255))
        screen.blit(ToRender2,(30,Height-Floor.get_height()-25))


Width,Height = 370,570
gravity = 0
strength = 0.3
score = 0
Alive = True
Score_font = pygame.font.Font("04B_19.TTF",25)
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width,Height))

death_sound = pygame.mixer.Sound("sound\\die.wav")
wing_sound =  pygame.mixer.Sound("sound\\wing.wav")
score_sound =  pygame.mixer.Sound("sound\\point.wav")
score_timer = 0

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
    if score_timer >= 60*2:
        score_timer = 0
        score_sound.play()
        score += 1
    for event in pygame.event.get():
        if event.type == 12:
            exit()
        if event.type == SPAWNPIPE and Alive:
            Pipe_List.extend(MakePipe())

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and Alive:
                wing_sound.play()
                gravity = 0
                gravity -= 5.26
                Bird.selected_bird = Bird.Bird_UpFlap
                Bird.moving_down = False
            if event.key == pygame.K_SPACE and not Alive:
                Bird.Bird_rect.center = (370/3-33,570/2)
                Pipe_List.clear()
                score_timer = 0
                score = 0
                gravity = 0
                Alive = True


    screen.blit(Background,(0,0))
    if Alive:
        score_timer += 1
        if gravity < 0:
            Bird.moving_down = False
        gravity = draw_bird(Bird,gravity)
        if Bird.Bird_rect.bottom >= Height-Floor.get_height():
            death_sound.play()
            Alive = False
        Pipe_List = MovingPipe(Pipe_List)
    else:
        pass
    Floor_x -= 2.1
    screen.blit(Floor,(Floor_x,Height-112))
    screen.blit(Floor,(Floor_x+Floor.get_width(),Height-112))
    Render()
    if Floor_x <= -Floor.get_width():
        Floor_x = 0
    
    pygame.display.update()