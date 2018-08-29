import pygame,sys,random
from pygame.locals import *
class Snake:

    #'speed' is the speed of the snake
    # 'size' is the size of the snake
    #'offset' is the offset between two snake body blocks and it is given by size-speed
    # 'deltaX' and 'deltaY' represent the change in X and Y coordinates of head of snake
    def  __init__(self, startx, starty,  speed, deltaX, deltaY,color,size):
        self.x = [startx, startx - speed, startx - 2*speed]
        self.y = [starty, starty, starty]
        self.offset=speed-size
        self.speed=speed
        self.deltaX=deltaX
        self.deltaY=deltaY
        self.color=color
        self.size=size

    def move_snake(self,ds):
        #Move snake head by delta and move other body blocks to its previous block's location
        if self.deltaX != 0 or self.deltaY != 0:
            for i in range(len(self.x) - 1, 0, -1):
                self.x[i] = self.x[i - 1]
            for i in range(len(self.y) - 1, 0, -1):
                self.y[i] = self.y[i - 1]
            self.x[0] += self.deltaX
            self.y[0] += self.deltaY
        for a, b in list(zip(self.x, self.y)):
            pygame.draw.rect(ds, self.color, (a, b, self.size, self.size))

    def inc_snake_length(self):
        tx = abs(self.x[len(self.x) - 1]-self.x[len(self.x)-2])
        ty = abs(self.y[len(self.y) - 1]-self.y[len(self.y)-2])

        #Determine the direction of snake and increment snake's body

        #If abs of x's of last two blocks of snake is 0,then snake moves in y direction.Find y direction.
        if tx == 0:
            self.x.append(self.x[len(self.x) - 1])
            if self.y[len(self.y)-2] > self.y[len(self.y)-1]:
                self.y.append(self.y[len(self.y) - 1]-self.offset)
            else :
                self.y.append(self.y[len(self.y) - 1] + self.offset)
        # If abs of y's of last two blocks of snake is 0,then snake moves in x direction.Find y direction.
        elif ty==0:
            self.y.append(self.y[len(self.y) - 1])
            if self.x[len(self.x) - 2] > self.x[len(self.x) - 1]:
                self.x.append(self.x[len(self.x) - 1] - self.offset)
            else:
                self.x.append(self.x[len(self.x) - 1] + self.offset)

    def collides(self,length,width):
        #collision of snake head with window boundary
        if self.x[0] > length-self.size or self.x[0] < -1 or self.y[0] > width-self.size or self.y[0] < 0:
            return True
        # collision of snake head with its body
        for i in range(1,len(self.x)):
            if (self.x[i]+self.size) > self.x[0] > (self.x[i]-self.size) and (self.y[i]+self.size) > self.y[0] > (self.y[i]-self.size):
                return True
        return False

    def eats_blob(self,blob):
        centerx=self.x[0]+self.size/2.0
        centery=self.y[0]+self.size/2.0
        circlex = abs(blob.x - centerx)
        circley = abs(blob.y - centery)
        if circlex > self.size / 2.0 + blob.size or circley > self.size / 2.0 + blob.size:
            return False
        if circlex <= self.size / 2.0 or circley <=self.size / 2.0:
            return True
        cornerx = circlex - self.size / 2.0
        cornery = circley - self.size / 2.0
        cornersq = cornerx ** 2.0 + cornery ** 2.0
        return cornersq <= blob.size ** 2.0

class Blob:

    def __init__(self,color,size,length,width):
        self.color=color
        self.size=size
        self.eaten=False
        self.x=0
        self.y=0
        self.length=length
        self.width=width

    def create_blob(self,ds):
        self.x = random.randint(self.size, self.length-self.size)
        self.y = random.randint(self.size, self.width-self.size)
        pygame.draw.circle(ds, self.color, (self.x, self.y), self.size)

    def redraw_blob(self,ds):
        pygame.draw.circle(ds, self.color, (self.x, self.y), self.size)

class Game:


    def __init__(self,FPS,length,width,bg_color,title):
        self.game_on=True
        self.FPS=FPS
        self.length=length
        self.width=width
        self.bg_color=bg_color
        self.snake=None
        self.blob=None
        self.ds=None
        self.title=title
        self.clock=pygame.time.Clock()
        self.score=0
        self.initialize()

    def initialize(self):
        pygame.init()
        self.ds=pygame.display.set_mode((self.length,self.width))
        pygame.display.set_caption(self.title)
        self.ds.fill(self.bg_color)
        self.snake=Snake(self.length//2+10,self.width//2+50,20,0,0,(103, 58, 183),15)
        self.blob=Blob((0, 150, 136),7,self.length,self.width)
        self.blob.create_blob(self.ds)

    #Set screen for starting-play envirnoment
    def set_play_screen(self):
        startx=self.length//2+10
        starty=self.width//2+50
        self.snake.x = [startx, startx - self.snake.speed,
                  startx - 2 * self.snake.speed]
        self.snake.y = [starty, starty, starty]
        self.snake.deltaX=0
        self.snake.deltaY=0
        self.score=0
        self.game_on=True

    def quit(self):
        pygame.quit()
        sys.exit()

    def display_score(self):
        self.display_text(str(self.score),self.length // 2, self.width // 2,(158, 158, 158),"helvetica",85)


    def display_text(self,text,centerx,centery,color,font,font_size):
        font_obj = pygame.font.SysFont(font, font_size)
        text_surface_obj = font_obj.render(text, True, color)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (centerx, centery)
        self.ds.blit(text_surface_obj, text_rect_obj)
        return text_rect_obj

    def display_menu(self):
        self.game_on=False
        gray_color=(158, 158, 158)
        font_1 = "monospace"
        font_2 = "lato"
        font_3 = "comicsans"
        font_4 = "monospace"
        credits="@adzo261-Aditya Zope"
        self.ds.fill(gray_color)


        self.display_text("Classic Snake",self.length//2,self.width//6,(255,255,255),font_1,85)

        play_rect_obj=self.display_text("Play", 3*self.length // 4, self.width // 2,(255,255,255), font_3, 60)

        quit_rect_obj=self.display_text("Quit", 3*self.length // 4, self.width // 1.5,(255,255,255), font_3, 60)

        self.display_text("Score ", self.length // 4, self.width // 2,(255,255,255), font_4, 45)

        self.display_text(str(self.score), self.length // 2.5, self.width // 2, (255, 255, 255), font_4, 45)

        self.display_text(credits, self.length // 2, self.width-30 , (255, 255, 255), font_4, 25)

        if play_rect_obj.collidepoint(pygame.mouse.get_pos()):
            self.ds.fill(gray_color)
            self.display_text("Classic Snake", self.length // 2, self.width // 6, (255, 255, 255), font_1, 85)
            self.display_text("Play", 3 * self.length // 4, self.width // 2, (138, 138, 138), font_3, 60)
            self.display_text("Quit", 3 * self.length // 4, self.width // 1.5, (255, 255, 255), font_3, 60)
            self.display_text("Score ", self.length // 4, self.width // 2, (255, 255, 255),font_4, 45)
            self.display_text(str(self.score), self.length // 2.5, self.width // 2, (255, 255, 255), font_4, 45)
            self.display_text(credits, self.length // 2, self.width - 30, (255, 255, 255), font_4, 25)
            if pygame.mouse.get_pressed()[0]:
                self.set_play_screen()

        elif quit_rect_obj.collidepoint(pygame.mouse.get_pos()):
            self.ds.fill(gray_color)
            self.display_text("Classic Snake", self.length // 2, self.width // 6, (255, 255, 255),font_1, 85)
            self.display_text("Play", 3 * self.length // 4, self.width // 2, (255, 255, 255), font_3, 60)
            self.display_text("Quit", 3 * self.length // 4, self.width // 1.5, (138, 138, 138), font_3, 60)
            self.display_text("Score ", self.length // 4, self.width // 2, (255, 255, 255), font_4, 45)
            self.display_text(str(self.score), self.length // 2.5, self.width // 2, (255, 255, 255), font_4, 45)
            self.display_text(credits, self.length // 2, self.width - 30, (255, 255, 255), font_4, 25)
            if pygame.mouse.get_pressed()[0]:
                self.quit()

    def update(self):
        if self.game_on:
            self.ds.fill(self.bg_color)
            self.display_score()
            if self.snake.eats_blob(self.blob) :
                self.blob.create_blob(self.ds)
                self.snake.inc_snake_length()
                self.score+=1
            else :
                self.blob.redraw_blob(self.ds)

            self.snake.move_snake(self.ds)
            if self.snake.collides(self.length,self.width):
                self.display_menu()

        else :
            self.display_menu()

        pygame.display.update()
        # To control the FPS ,i.e run game at same speed on varying speed processors
        self.clock.tick(self.FPS)


    #Handles main game loop
    def gameLoop(self):
        dir=""
        while True:

            for e in pygame.event.get():
                if e.type == QUIT:
                    self.quit()
                if self.game_on :
                    if e.type == KEYDOWN:
                        if e.key == K_LEFT and dir!="right" and dir!="":
                            self.snake.deltaX = -self.snake.speed
                            self.snake.deltaY = 0
                            dir = "left"
                        elif e.key == K_RIGHT and dir!="left":
                            self.snake.deltaX = self.snake.speed
                            self.snake.deltaY = 0
                            dir = "right"
                        elif e.key == K_UP and dir!="down":
                            self.snake.deltaY = - self.snake.speed
                            self.snake.deltaX = 0
                            dir = "up"
                        elif e.key == K_DOWN and dir!="up":
                            self.snake.deltaY = self.snake.speed
                            self.snake.deltaX = 0
                            dir = "down"

            self.update()



if __name__ == "__main__":
    game=Game(20,840,640,(255,255,255),"Classic Snake")
    game.gameLoop()



