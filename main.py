import pygame
import math
import random

# display setup
pygame.init()
WIDTH, HEIGHT = 800, 550
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# music
pygame.mixer.init(44100, -16,2,2048)

win_sound= pygame.mixer.Sound("won.wav")
lost_sound= pygame.mixer.Sound("lost.wav")

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

# buttons
RADIUS= 20
GAP= 15
letters= []
startx= round((WIDTH - (RADIUS*2 + GAP)*13) / 2)
starty= 400
A= 65
for i in range(26):
    x= startx + GAP*2 + ((RADIUS*2 + GAP)*(i%13))
    y= starty + ((i//13)*(GAP + RADIUS*2))
    letters.append([x,y,chr(A+i),True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans',40)
WORD_FONT = pygame.font.SysFont('comicsans',60)
TITLE_FONT = pygame.font.SysFont('comicsans',70)
HINT_FONT = pygame.font.SysFont('comicsans',30)

# images
images= []
for i in range(7):
    images.append(pygame.image.load("img/hangman"+str(i)+".png"))

# game variables
hangman_status= 0
obj = open("words.txt","r")
w= obj.read()  # reading words from file
words= list(w.split("\n"))
obj.close()
word,hint= random.choice(words).split("-")
guessed= []

# colors
GREEN= (41,110,1)
SILVER= (108,122,134)
GOLD= (212,175,55)
MAROON= (128,0,0)

def draw():
    win.fill(GREEN)

    # title
    text= TITLE_FONT.render("GUESS THE ANIMAL!",1,GOLD)
    win.blit(text, (WIDTH/2-text.get_width()/2,20))

    # word
    display_word= ""
    for letter in word:
        if letter in guessed:
            display_word+= letter+" "
        else:
            display_word+= "_ "
    text= WORD_FONT.render(display_word,1,MAROON)
    win.blit(text,(400,200))

    # hint
    text= HINT_FONT.render(f"Hint: {hint}",1,SILVER)
    win.blit(text,(400,260))

    # letters button 
    for letter in letters:
        x,y,ltr,visible = letter
        if visible:
            pygame.draw.circle(win,(102,0,51),(x,y),RADIUS,3)
            text= LETTER_FONT.render(ltr,1,(102,0,51))
            win.blit(text, (x-text.get_width()/2,y-text.get_height()/2))

    win.blit(images[hangman_status], (150,100))
    pygame.display.update()

def display_message(msg,s=-1):
    pygame.time.delay(2000)
    win.fill(GREEN)
    text= WORD_FONT.render(msg,1,GOLD)
    win.blit(text,(WIDTH/2-text.get_width()/2, HEIGHT/2-text.get_height()/2))
    pygame.display.update()
    if s==1:
    	win_sound.play()
    elif s==0:
    	lost_sound.play()
    pygame.time.delay(2000)

def main():
    global hangman_status
    FPS= 60
    clock= pygame.time.Clock()
    run= True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y= pygame.mouse.get_pos()
                for letter in letters:
                    x,y,ltr,visible= letter
                    if visible:
                        dis= math.sqrt((x-m_x)**2 + (y-m_y)**2)
                        if dis<RADIUS:
                            letter[3]= False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status+=1

        draw()

        won= True
        
        for letter in word:
            if letter not in guessed:
                won= False
                break

        if won:
        	display_message("YOU WON!",1)
        	break

        if hangman_status==6:
        	display_message(f"YOU LOST! The word was {word}!",0)
        	break

def main_menu():
    global hangman_status
    global guessed
    global word
    global hint
    global letters
    run= True
    while run:
        display_message("Press the mouse to play...")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                hangman_status= 0
                guessed= []
                word,hint= random.choice(words).split("-")
                for l in letters:
                    l[3]= True
                pygame.time.delay(1000)
    pygame.quit()

main_menu()