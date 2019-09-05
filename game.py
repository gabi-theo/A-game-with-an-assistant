import pygame
import random
import os
import time
import playsound
import speech_recognition as sr
import pyttsx3

#Initializing the window game and choosing random coordinates for the two points 
window = pygame.display.set_mode((500,650))
background = pygame.image.load('grid.png')
minx = 73 
miny = 147
radius = 25
vel = 85
x = minx+vel*random.randint(0,4)
y = miny+vel*random.randint(0,4)
initial_posX = x    #storing the initial positions so we can reuse them when the computer will play the game by himsel
initial_posY = y
targetX  = minx+vel*random.randint(0,4)
targetY = miny+vel*random.randint(0,4)
#choosing the coordinates of the target point different from those of the starting point
while targetX == x and targetY == y:
    targetX  = minx+vel*random.randint(0,4)
    targetY = miny+vel*random.randint(0,4)

#function for redrawing the window when we teach the computer  what moves should do
def redrawWindow():
    window.fill((255,255,255))
    window.blit(background,(0,0))
    pygame.draw.circle(window, (0,0,0), (x,y),radius)
    pygame.draw.circle(window, (0,255,0),(targetX,targetY), radius)
    pygame.display.update()

#function for redrawing the window after the computer makes a move when playing alone
def redrawNewWindow():
    window.fill((255,255,255))
    window.blit(background,(0,0))
    pygame.draw.circle(window, (0,0,0), (initial_posX,initial_posY),radius)
    pygame.draw.circle(window, (0,255,0),(targetX,targetY), radius)
    pygame.display.update()

#function for recognizing our voice
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
            print(said)

        except Exception as e:
            print('Exception ' +str(e))

    return said

#function so the computer can talk
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
 
move_list = [] #here we will store the moves so the computer can remember what it should do
run = True

#so we start the game
while run:
    pygame.time.delay(70)
    text = get_audio()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # if computer detects that we said the word "left" he will move to the left
    # same with the other commands
    # it will also store our command to move_list
    if ('left' in text) and x>73:
        x-=vel
        time.sleep(0.5)
        move_list.append('left')
    if ('right' in text) and x<147+vel*3:
        x+=vel
        time.sleep(0.5)
        move_list.append('right')
    if ('up' in text) and y> 147:
        y-=vel
        time.sleep(0.5)
        move_list.append('up')
    if ('down' in text) and y<147+vel*4:
        y+=vel
        time.sleep(0.5)
        move_list.append('down')
        
    # we will redraw the window so we can see the new position of the circle
    redrawWindow()

    #if the computer reaches the target he will say that the game is done
    #otherwise he will ask for new instructions
    if targetX == x and targetY == y:
        run = False
        speak('I finished the game')
        
    else:
        speak('What should I do next?')
time.sleep(1)
# based on the commands from the list, he will play the game alone now
# but only if say that we want to do that :)
speak('I think I know how to solve the game alone')
speak('Do you want me to solve the game by myself now?')
text = get_audio()
if 'yes' or 'sure' in text:
    newrun = True
    while newrun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                newrun = False
        redrawNewWindow()
        time.sleep(0.5)
        for word in move_list:
            pygame.time.delay(70)
            if word=='right':
                initial_posX += vel
            if word == 'left':
                initial_posX -=vel
            if word == 'up':
                initial_posY-=vel
            if word == 'down':
                initial_posY+=vel
                    
            redrawNewWindow()
            time.sleep(0.5)
        newrun = False

else:
    speak('ok')
speak('I am done')
speak('It was a pleasure playing with you. See you soon')
                    
    
pygame.quit()
