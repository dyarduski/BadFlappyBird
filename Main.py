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
        self.Bird_rect = self.Bird_MidFlap.get_rect(center=(370*0.25,570/2))
        self.selected_bird = self.Bird_MidFlap
        self.R = None

class pipe():
    def __init__(self,bottom_rect,top_rect):
        self.bottom_rect = bottom_rect
        self.top_rect = top_rect
        self.vel = 2.05
        self.passed = False
    def move(self):
        self.bottom_rect.centerx -= self.vel
        self.top_rect.centerx -= self.vel
        screen.blit(Pipe,self.top_rect)
        screen.blit(flip_pipe,self.bottom_rect)


def draw_bird(Bird,gravity):
    global score,Alive
    x = lambda:pygame.transform.rotate(Bird.selected_bird,-gravity * 3.25)
    Bird.R = x()
    gravity += strength
    Bird.Bird_rect.centery += gravity
    for Pipe in Pipe_List:
        if Bird.Bird_rect.centerx > Pipe.top_rect.centerx and Pipe.passed == False:
            score += 1
            score_sound.play()
            Pipe.passed = True
        if Bird.Bird_rect.colliderect(Pipe.top_rect) or Bird.Bird_rect.colliderect(Pipe.bottom_rect):
            death_sound.play()
            Alive = False
    if Bird.moving_down:
        Bird.selected_bird = Bird.Bird_DownFlap
    Bird.moving_down = True
    screen.blit(Bird.R,Bird.Bird_rect)
    return gravity

def MovingPipe():
    for x,Pipe in enumerate(Pipe_List):
        if Pipe.top_rect.right <= 0 and Pipe.bottom_rect.right <= 0:
            Pipe_List.pop(x)
    for Pipe in Pipe_List:
        Pipe.move()

def MakePipe():
    y = random.randint(415,533)
    new = Pipe.get_rect(center=(385,y))
    down_new = Pipe.get_rect(center=(385,y - 437))
    return new,down_new

def Render():
    ToRender1 = Score_font.render(f"Score: {int(score)}",True,(255,255,255))
    screen.blit(ToRender1,(Width/2-35,42))
    if not Alive:
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
        if event.type == SPAWNPIPE and Alive:
            rects = MakePipe()
            Pipe_List.append(pipe(rects[1],rects[0]))

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
        if gravity < 0:
            Bird.moving_down = False
        gravity = draw_bird(Bird,gravity)
        if Bird.Bird_rect.bottom >= Height-Floor.get_height():
            death_sound.play()
            Alive = False
        MovingPipe()
    else:
        pass
    Floor_x -= 2.1
    screen.blit(Floor,(Floor_x,Height-112))
    screen.blit(Floor,(Floor_x+Floor.get_width(),Height-112))
    Render()
    if Floor_x <= -Floor.get_width():
        Floor_x = 0
    
    pygame.display.update()