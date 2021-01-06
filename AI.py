import pygame
import random
import neat

pygame.init()

class Bird:
    def __init__(self):
        self.moving_down = True
        self.sprite_bird = [pygame.image.load("sprites\\yellowbird-downflap.png"),pygame.image.load("sprites\\yellowbird-midflap.png"),pygame.image.load("sprites\\yellowbird-upflap.png")]
        self.Bird_rect = self.sprite_bird[1].get_rect(center=(370/3-33,570/2))
        self.selected_bird = self.sprite_bird[1]
        self.rotated_bird = None
        self.gravity = 0
        self.score = 0
    def move(self):
        x = lambda:pygame.transform.rotate(self.selected_bird,-self.gravity * 3.25)
        self.rotated_bird = x()
        self.gravity += 0.3
        self.Bird_rect.centery +=self.gravity
        screen.blit(self.rotated_bird,self.Bird_rect)
    def jump(self):
        self.gravity = -4.5
        self.Bird_rect.centery +=self.gravity

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


def draw_bird(ge,nets,pipe_ind):
    for Pipe in Pipe_List:
        for x,ai in enumerate(Birds):

            if ai.Bird_rect.colliderect(Pipe.top_rect) or ai.Bird_rect.colliderect(Pipe.bottom_rect) or ai.Bird_rect.bottom >= abs(Height-Floor.get_height()) or ai.Bird_rect.top < 0:
                ge[x].fitness -= 2
                Birds.pop(x)
                ge.pop(x)
                nets.pop(x)
                continue
            if ai.Bird_rect.centerx > Pipe.top_rect.right and Pipe.passed==False:
                Pipe.passed = True
                ge[x].fitness += 5
                ai.score += 1
    for ai in Birds:
        ge[Birds.index(ai)].fitness += 0.1
        ai.move()
        try:
            output = nets[Birds.index(ai)].activate((ai.Bird_rect.centery, abs(ai.Bird_rect.centery - Pipe_List[pipe_ind].top_rect.bottom), abs(ai.Bird_rect.centery - (Pipe_List[pipe_ind].bottom_rect.top-2))))
        except:
            print(pipe_ind)
            exit()
        if output[0] > 0.3:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            ai.jump()
    return ge,nets

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

Width,Height = 370,570
Clock = pygame.time.Clock()
Score_font = pygame.font.Font("04B_19.TTF",25)
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
pygame.time.set_timer(SPAWNPIPE,1300)

Birds = []
def eval_genome(genomes,config):
    global Floor_x,Pipe_List
    nets = []
    ge = []
    rects = MakePipe()
    Pipe_List.append(pipe(rects[1],rects[0]))
    for _, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        Birds.append(Bird())
        ge.append(genome)
    while True:
        Clock.tick(60)
        pipe_ind = 0
        for event in pygame.event.get():
            if event.type == 12:
                exit()
            if event.type == SPAWNPIPE:
                rects = MakePipe()
                Pipe_List.append(pipe(rects[1],rects[0]))

        screen.blit(Background,(0,0))
        MovingPipe()
        if len(Birds) > 0:
            if len(Pipe_List) > 1 and Pipe_List[0].passed:
                pipe_ind = 1
        else:
            Pipe_List.clear()
            break
        ToRender1 = Score_font.render(f"Score: {int(Birds[0].score)}",True,(255,255,255))
        screen.blit(ToRender1,(Width/2-35,42))

        Floor_x -= 2.1
        screen.blit(Floor,(Floor_x,Height-112))
        screen.blit(Floor,(Floor_x+Floor.get_width(),Height-112))
        ge,nets = draw_bird(ge,nets,pipe_ind)
        if Floor_x <= -Floor.get_width():
            Floor_x = 0
        
        pygame.display.update()

if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,"config.txt")  
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    winner = p.run(eval_genome,50)
