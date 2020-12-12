import pygame
import random
import math
import sys
import matplotlib.pyplot as plt
import Statistics


# other = variables
# F,A = move n forward
# G = move n forward without drawing a line
# B = move n backwards
# - = turn left by angle
# + = turn right by angle
# [ = push position and angle
# ] = pop position and angle
# a,b,c,d = color 1,2,3,4
# 1-4 line size (std = 1)

rules = {}

rules['F'] = 'FF'
rules['X'] = 'b2F[+c3XF-[X]--b2X][---b2X]'
axiom = 'X'
angle = 22.9

iterations = 7
step = 3

color1 = (105, 46, 26)  # brown 1
color2 = (190, 114, 60)  # brown 2
color3 = (101, 250, 52)  # green
color4 = (255, 255, 255)  # white

angleoffset = 270

size = width, height = 1920, 1080  # display with/height
pygame.init()  # init display
screen = pygame.display.set_mode(size)  # open screen
startpos = width / 2 - 100, height - 75


def applyRule(input):
    output = ""
    for rule, result in rules.items():  # applying the rule by checking the current char against it
        if (input == rule):
            output = result  # Rule 1
            break
        else:
            output = input  # else ( no rule set ) output = the current char -> no rule was applied
    return output


def processString(oldStr):
    newstr = ""
    for character in oldStr:
        newstr = newstr + applyRule(character)  # build the new string
    return newstr


def createSystem(numIters, axiom):
    startString = axiom
    endString = ""
    leavesNum = {}
    for i in range(numIters):  # iterate with appling the rules
        print "Iteration: {0}".format(i)
        endString = processString(startString)
        leavesNum[i+1] = endString.count('c')
        startString = endString
    return endString, leavesNum


def polar_to_cart(theta, r, (offx, offy)):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return tuple([x + y for x, y in zip((int(x), int(y)), (offx, offy))])


def cart_to_polar((x, y)):
    return (math.degrees(math.atan(y / x)), math.sqrt(math.pow(x, 2) + math.pow(y, 2)))


def drawTree(input, oldpos):
    a = 0  # angle
    i = 0  # counter for process calculation
    processOld = 0  # old process
    newpos = oldpos
    num = []  # stack for the brackets
    color = (255, 255, 255)
    linesize = 1
    counter = 0
    for character in input:  # process for drawing the l-system by writing the string to the screen
        i += 1  # print process in percent
        process = i * 100 / len(input)
        if not process == processOld:
            print process, "%"
            processOld = process

        if character == 'A':  # magic happens here
            newpos = polar_to_cart(a + angleoffset, step, oldpos)
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == 'F':
            newpos = polar_to_cart(a + angleoffset, step, oldpos)
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == 'B':
            newpos = polar_to_cart(-a + angleoffset, -step, oldpos)
            pygame.draw.line(screen, color, oldpos, newpos, linesize)
            oldpos = newpos
        elif character == 'G':
            newpos = polar_to_cart(a + angleoffset, step, oldpos)
            oldpos = newpos
        elif character == 'a':
            color = color1
        elif character == 'b':
            color = color2
        elif character == 'c':
            color = color3
        elif character == 'd':
            color = color4
        elif character == '1':
            linesize = 1
        elif character == '2':
            linesize = 2
        elif character == '3':
            linesize = 3
        elif character == '4':
            linesize = 4
        elif character == '+':
            a += angle
        elif character == '-':
            a -= angle
        elif character == '[':
            num.append((oldpos, a))
        elif character == ']':
            oldpos, a = num.pop()
        if counter == 100:
            pygame.display.flip()
            counter = 0
        counter+=1

def numberOfleaves(numOfLeaves):
    print(numOfLeaves)
    plt.xlabel("Iterations")
    plt.ylabel("Number of leaves")
    plt.plot(numOfLeaves.keys(), numOfLeaves.values())
    plt.scatter(numOfLeaves.keys(), numOfLeaves.values(), s = 25, c="red")
    #plt.show()



if __name__ == '__main__':
    # drawTree(createSystem(iterations, axiom), startpos)
    tree, leavesNumber = (createSystem(iterations, axiom))
    print tree
    drawTree(tree, startpos)
    #pygame.display.flip()
    pygame.image.save(screen, "screenshot.png")
    print "Finished"
    numberOfleaves(leavesNumber)
    Statistics.show()
    plt.show()
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 sys.exit()
