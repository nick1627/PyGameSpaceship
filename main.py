# created following https://www.youtube.com/watch?v=jO6qQDNa2UY

import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game")

white = (255, 255, 255)
black = (0, 0, 0)
redColour = (255, 0, 0)
yellowColour = (255, 255, 0)
fps = 60
border = pygame.Rect(width//2 - 5, 0, 10, height)

spaceShipHeight = 40
spaceShipWidth = 55

speed = 5
bulletSpeed = 7

maxBullets = 3

redHit = pygame.USEREVENT + 1 #create a new event
yellowHit = pygame.USEREVENT + 2

# redHealth = 10
# yellowHealth = 10

winnerText = ""

healthFont = pygame.font.SysFont("comicsans", 40)
winnerFont = pygame.font.SysFont("comicsans", 100)


bulletHitSound = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
bulletFireSound = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))


yellow_spaceship_image = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png")) #avoids different OS slash direction problems
yellowShip = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceShipWidth, spaceShipHeight)), 270)
red_spaceship_image = pygame.image.load(os.path.join("Assets", "spaceship_red.png")) #avoids different OS slash direction problems
redShip = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceShipWidth, spaceShipHeight)), 90)

space = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (width, height))


def drawWindow(red, yellow, bulletsRed, bulletsYellow, redHealth, yellowHealth):
    win.blit(space, (0, 0))
    pygame.draw.rect(win, black, border)

    redHealthText = healthFont.render("Health: " + str(redHealth), 1, white)
    yellowHealthText = healthFont.render("Health: " + str(yellowHealth), 1, white)
    win.blit(redHealthText, (10, 10))
    win.blit(yellowHealthText, (width - redHealthText.get_width() - 10, 10))


    win.blit(yellowShip, (yellow.x, yellow.y)) #blit draws surface onto screen
    win.blit(redShip, (red.x, red.y))

    for bullet in bulletsRed:
        pygame.draw.rect(win, redColour, bullet)
    for bullet in bulletsYellow:
        pygame.draw.rect(win, yellowColour, bullet)

    pygame.display.update()

def handleRedMovement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - speed > 0: #left
        red.x -= speed
    if keys_pressed[pygame.K_d] and red.x + speed + red.width < border.x: #right
        red.x += speed
    if keys_pressed[pygame.K_w] and red.y - speed > 0: #up
        red.y -= speed
    if keys_pressed[pygame.K_s] and red.y + speed + red.height < height: #down
        red.y += speed

def handleYellowMovement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - speed > border.x + border.width: #left
        yellow.x -= speed
    if keys_pressed[pygame.K_RIGHT] and yellow.x + speed + yellow.width < width: #right
        yellow.x += speed
    if keys_pressed[pygame.K_UP] and yellow.y - speed > 0: #up
        yellow.y -= speed
    if keys_pressed[pygame.K_DOWN] and yellow.y + speed + yellow.height < height: #down
        yellow.y += speed

def handleBullets(bulletsRed, bulletsYellow, red, yellow):
    for bullet in bulletsRed:
        bullet.x += bulletSpeed
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellowHit))
            bulletsRed.remove(bullet)
        elif bullet.x > width:
            bulletsRed.remove(bullet)

    for bullet in bulletsYellow:
        bullet.x -= bulletSpeed
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(redHit))
            bulletsYellow.remove(bullet)
        elif bullet.x < 0:
            bulletsYellow.remove(bullet)

def drawWinner(text):
    drawText = winnerFont.render(text, 1, white)
    win.blit(drawText, (width/2 - drawText.get_width()/2, height/2 - drawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red =  pygame.Rect(100, 300, spaceShipWidth, spaceShipHeight)
    yellow =  pygame.Rect(700, 300, spaceShipWidth, spaceShipHeight)
    winnerText = ""

    redHealth = 10
    yellowHealth = 10

    clock = pygame.time.Clock()
    run = True

    bulletsRed = []
    bulletsYellow = []

    while run:
        clock.tick(fps) #never run loop more than 60 times per second
        for event in pygame.event.get():
            #check for different events
            if event.type == pygame.QUIT:
                #if the user tries to quit game
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bulletsRed) < maxBullets:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2-2, 10, 5)
                    bulletsRed.append(bullet)
                    bulletFireSound.play()
                if event.key == pygame.K_RCTRL and len(bulletsYellow) < maxBullets:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2-2, 10, 5)
                    bulletsYellow.append(bullet)
                    bulletFireSound.play()


            if event.type == redHit:
                redHealth -= 1
                bulletHitSound.play()
            if event.type == yellowHit:
                yellowHealth -= 1
                bulletHitSound.play()


        if redHealth <= 0:
            winnerText = "Yellow Wins!"
        if yellowHealth <= 0:
            winnerText = "Red Wins"

        if winnerText != "":
            drawWinner(winnerText)
            break

        keys_pressed = pygame.key.get_pressed() #to allow continuous pressing
        handleRedMovement(keys_pressed, red)
        handleYellowMovement(keys_pressed, yellow)

        handleBullets(bulletsRed, bulletsYellow, red, yellow)
        drawWindow(red, yellow, bulletsRed, bulletsYellow, redHealth, yellowHealth)



    main()



if __name__ == "__main__":
    #only run if main.py is run directly, not imported
    main()