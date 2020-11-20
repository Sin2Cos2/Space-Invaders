import pygame, sys, random, time, pickle
from player import SpaceShip, Lazer, Shelter, Enemy

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
HIGHSCORE = 0

class SpaceInvaders:
    FPS = 80
    HEIGHT = 600
    WIDTH = 800
    SCORE = 0
    FLAG = 0

    def __init__(self):

        self.playerShip = SpaceShip()
        self.lazer = Lazer(-5, -5, color=BLACK)
        self.enemy_lazer = Lazer(-5, -5, color=BLACK, speed=-5)
        self.enemies = []
        self.shelters = []

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = None

    def start(self):

        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background = self.background.convert()
        self.background.fill(BLACK)
        self.font = pygame.font.SysFont(None, 28)
        self.FONT = pygame.font.SysFont(None, 60)

        self.screen.blit(self.background, (0, 0))

        pygame.display.flip()
        
        #Create shelters
        for i in range(50,800,200):
            self.create_shelters(i, 400)

        #Create enemies
        enemy_x = 100
        enemy_y = 50
        for i in range(5):
            for j in range(10):
                self.enemies.append(Enemy(enemy_x, enemy_y))
                enemy_x += 30
            enemy_x = 100
            enemy_y += 30


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.playerShip.moveLeft()
            if keys[pygame.K_RIGHT]:
                self.playerShip.moveRight()
            if keys[pygame.K_SPACE] and self.lazer.kd == 0:
                self.lazer.x = self.playerShip.x + (self.playerShip.width//2)
                self.lazer.y = self.playerShip.y
                self.lazer.color = (0, 255, 0)
                self.lazer.kd = 1

            self.update()

            self.draw()
    
    def create_shelters(self, x, y):
        for i in range(0, 60, 20):
            for j in range(0, 75, 15):
                self.shelters.append(Shelter(x+j, y+i, 15, 20))


    def update(self):
            
        self.clock.tick(SpaceInvaders.FPS)
        
        for i, shelter in enumerate(self.shelters):
            if shelter.colliderect(self.lazer):
                self.lazer.y = -15
                self.shelters.pop(i)
            if shelter.colliderect(self.enemy_lazer):
                self.enemy_lazer.y = 615
                self.shelters.pop(i)
    
        self.update_enemies()

        if self.enemy_lazer.colliderect(self.playerShip):
            self.enemy_lazer.y = 615
            self.playerShip.health -= 1

        if self.playerShip.health == 0:
            self.exit_game()


        #cooldown for lazer
        self.lazer.update()
        if self.lazer.y + self.lazer.height < 0:
            self.lazer.kd = 0
    
    def update_enemies(self):
        enemies_pos = {}
        enemies_attack = []
        for i, enemy in enumerate(self.enemies):
            enemies_pos[i] = enemy.x
            enemies_attack.append(enemy.y)
        
        if self.enemy_lazer.y >= 610:
            self.enemy_lazer.kd = 0

        max_x = max(enemies_pos, key=enemies_pos.get) 
        min_x = min(enemies_pos, key=enemies_pos.get)

        for i, enemy in enumerate(self.enemies):
            
            if (i == max_x and enemy.x+enemy.width>=self.WIDTH) or (i == min_x and enemy.x<=0):
                Enemy.y_direction -= 5
                Enemy.direction *= -1
            enemy.move_ip(Enemy.direction, 0)

            enemy.y -= 55
            if not enemy.y in enemies_attack:
                rand_numb = random.randint(0, 2500)
                if self.enemy_lazer.kd == 0 and rand_numb == 5:
                    self.enemy_lazer.color = WHITE
                    self.enemy_lazer.x = enemy.x + 12
                    self.enemy_lazer.y = enemy.y - Enemy.y_direction + 55
                    self.enemy_lazer.kd = 1
            enemy.y += 55

            if enemy.colliderect(self.lazer):
                self.lazer.y = -30
                self.enemies.pop(i)
                self.SCORE += 15
        
        if not self.enemies:
            self.win_game()
        
        self.enemy_lazer.update()
    
        
    def draw(self):
    
        self.background.fill(BLACK)

        self.playerShip.draw(self.background)
        self.lazer.draw(self.background)
        self.enemy_lazer.draw(self.background)

        for enemy in self.enemies:
            enemy.draw(self.background)
            
        for shelter in self.shelters:
            shelter.draw(self.background)
        
        score = "score: " + str(self.SCORE)
        scoreWin = self.font.render(score, 1, WHITE)
        lives = 'lives: ' + str(self.playerShip.health)
        livesWin = self.font.render(lives, 1, GREEN)
        

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(scoreWin, (5, 5))
        self.screen.blit(livesWin, (5, 560))
        pygame.display.flip()

    def exit_game(self):

        self.background.fill(BLACK)
        game = self.FONT.render("GAME", 1, WHITE)
        over = self.FONT.render(" OVER", 1, WHITE)
        score = "score: " + str(self.SCORE)
        scoreWin = self.font.render(score, 1, WHITE)
        highscore = "highscore: " + str(HIGHSCORE)
        highscoreWin = self.font.render(highscore, 1, WHITE)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(game, (350, 250))
        self.screen.blit(over, (350, 300))
        self.screen.blit(scoreWin, (300, 350))
        self.screen.blit(highscoreWin, (420, 350))
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    
    def win_game(self):
        
        global HIGHSCORE
        self.background.fill(BLACK)
        if self.SCORE > HIGHSCORE:
            HIGHSCORE = self.SCORE
            with open('HIGHSCORE', 'wb') as f:
                pickle.dump(HIGHSCORE, f)
        #You win, your score, highscore
        you = self.FONT.render("YOU", 1, WHITE)
        win = self.FONT.render("WIN", 1, WHITE)
        score = "score: " + str(self.SCORE)
        scoreWin = self.font.render(score, 1, WHITE)
        highscore = "highscore: " + str(HIGHSCORE)
        highscoreWin = self.font.render(highscore, 1, WHITE)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(you, (350, 250))
        self.screen.blit(win, (350, 300))
        self.screen.blit(scoreWin, (270, 350))
        self.screen.blit(highscoreWin, (390, 350))
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()



def main():

    pygame.init()
    pygame.display.set_caption("Space Invaders")
    
    game = SpaceInvaders()
    with open('HIGHSCORE', 'rb') as f:
        HIGHSCORE = pickle.load(f)
    game.start()

if __name__ == "__main__":
    main()