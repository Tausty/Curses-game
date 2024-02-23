# make global attack functino
# make a new type of enemy
# make the enemy attack more apperent that its an attack
# make win screen r
# make a variable diffuclty maybe? starting menu?
# fix ewnemy can spawn on player
# add bulluts mathew said use a classes
import random
import curses
from time import perf_counter as pf

name = input()
HEIGHT = 24
WIDTH = 70
isdead = False
enemy = []

class swordenemy:
    def __init__(self, ex, ey):
        self.ex = ex
        self.ey = ey
        self.elastmove = " "
        self.death = False
       
   
    def move(self,cx,cy):
        if self.death == False:
            direction = random.randint(0,6)
            if cy == self.ey and direction != 6:
                direction = 0
            if cx == self.ex and direction != 6:
                direction = 3
            if direction == 0 or direction == 1 or direction == 2:
                if abs((self.ex+1)-cx) > abs((self.ex-1)-cx): #the enemy is on the left
                    self.ex -= 1
                    self.elastmove = 'l'
                else:
                    self.ex +=1
                    self.elastmove = 'r'
            if direction == 3 or direction == 4 or direction ==5:
                if abs((self.ey+1)-cy) > abs((self.ey-1)-cy): #the enemy is above
                    self.ey -= 1
                    self.elastmove = 'u'
                else:
                    self.ey += 1 # enemy is below
                    self.elastmove = 'd'
        return self.ex, self.ey, self.elastmove
       

def bordercontrol(x,y):
    x = max(1, x) # stops the cursor from going under the white bar
    x = min(WIDTH-2, x) # stops the cursor from going over the white bar

    y = max(1, y) # stops the cursor from going under the white bar
    y = min(HEIGHT-2, y) # stops the cursor from going over the white bar
    return x,y



def menu(stdscr):
    lastkey = 0
   
    cx = 0
    cy = 0

    #ready sceren for blank canvas
    stdscr.clear()
    stdscr.refresh()
   
    #starting colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN) # cyan text black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # red ttext black background
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE) # black text white backgroudn
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK) # green text balck background
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_WHITE) # yellowtext gray background
   

    lastmove = " "
    isdead = False
    enemy = []
    enemycount = 0
    title = "              "
    subtitle = "(use arrows to move, / to attack)"
    count = 0
    killcount = 0
    enemyleft = 0
    start = pf()
    #since q is exit
    while lastkey != ord('q'): #ord gives the number code of q
        stdscr.clear()
        time = round(pf() - start, 2)
        
       
        killcount = 0
        for i in enemy:
            if i.death == True:
                killcount += 1

        stdscr.attron(curses.color_pair(3)) # making the borders on the side
        for i in range(WIDTH):
            stdscr.addstr(0,i," ")
            stdscr.addstr(HEIGHT-1,i," ")
        for i in range(HEIGHT):
            stdscr.addstr(i,int(WIDTH)-1, " ")
            stdscr.addstr(i,0, " ")
        stdscr.attroff(curses.color_pair(3))
       
        if killcount == len(enemy):
            enemycount += 3
            f = open("scores.txt", "a")
            f.write(f"Stage {enemycount // 3-1} completion time: {time} done by {name}\n")
            f.close()
            for i in range(enemycount):
                if cy < HEIGHT // 2:
                    enemy.append(swordenemy(random.randint(3,WIDTH-3),random.randint(HEIGHT//2, HEIGHT-1)))
                else:
                    enemy.append(swordenemy(random.randint(3,WIDTH-3),random.randint(2, HEIGHT // 2)))
               
        if killcount >= 1:
            enemyleft = 0
            for i in range(enemycount-3, len(enemy)):
                if enemy[i].death == False:
                    enemyleft += 1
            title = f"you are on wave {enemycount // 3}, There are {enemyleft} enemies left."
            subtitle = f"you have killed {killcount} enemies."
        # arrow key movement (using premade functions, can)
        for i in range(len(enemy)):
            stdscr.addstr(enemy[i].ey,enemy[i].ex," ")
           
            if isdead == False:
                if lastkey == curses.KEY_DOWN:
                    if i == 0: cy += 1
                    enemy[i].ex, enemy[i].ey, enemy[i].elastmove = enemy[i].move(cx,cy)
                    lastmove = "d"
                elif lastkey == curses.KEY_UP:
                    if i == 0: cy -= 1
                    enemy[i].ex, enemy[i].ey, enemy[i].elastmove = enemy[i].move(cx,cy)
                    lastmove = "u"
                elif lastkey == curses.KEY_RIGHT:
                    if i == 0: cx += 1
                    enemy[i].ex, enemy[i].ey, enemy[i].elastmove = enemy[i].move(cx,cy)
                    lastmove = "r"
                elif lastkey == curses.KEY_LEFT:
                    if i == 0: cx -= 1
                    enemy[i].ex, enemy[i].ey, enemy[i].elastmove = enemy[i].move(cx,cy)
                    lastmove = "l"

                   
            for j in range(len(enemy)):
                if (enemy[i].ex == enemy[j].ex and enemy[i].ey == enemy[j].ey and i != j and enemy[i].death == False and enemy[j].death == False):
                    if enemy[i].elastmove == "d":
                        enemy[i].ey -= 1
                    elif enemy[i].elastmove == "u":
                        enemy[i].ey += 1
                    elif enemy[i].elastmove == "r":
                        enemy[i].ex -= 1
                    elif enemy[i].elastmove == "l":
                        enemy[i].ex += 1
                   
            if enemy[i].ex == cx and enemy[i].ey == cy and enemy[i].death == False:
                isdead = True
               
               
       
            enemy[i].ex, enemy[i].ey = bordercontrol(enemy[i].ex,enemy[i].ey)
       
        cx, cy = bordercontrol(cx,cy)
        #string decleration
       
        debugline  = f"time :D: {time}"#format puts something into the curly brackets

       
        x_title = (WIDTH//2) - len(title)//2
        x_subtitle = (WIDTH//2) - len(subtitle)//2
        x_debugline = (WIDTH//2) - len(debugline)//2
        y_global = HEIGHT // 2
       
       
        stdscr.addstr(y_global + 1, x_subtitle, subtitle)
        stdscr.addstr(y_global + 5, x_debugline, debugline)
       

        stdscr.addstr(y_global, x_title, title)
       
        # if enemy[i].death == True:
        #     stdscr.attron(curses.color_pair(4))
        #     title = "You WON. Press q to exit"
        #     stdscr.addstr(y_global, (WIDTH//2) - len(title)//2,title)
        #     deathmsg = "you won "
        #     subtitle = ""
        #      # trying to get it to print death message all across the screen
        #     stdscr.attroff(curses.color_pair(4))
       
       
               
        stdscr.attroff(curses.A_BOLD)
       
        stdscr.attron(curses.color_pair(5))
        stdscr.attron(curses.A_STANDOUT)
       
        for i in range(len(enemy)):
            if lastkey == ord('/') and isdead == False:
                if lastmove == "d":
                    if i == 0:
                        stdscr.addstr(cy+1,cx,"#")
                        if cy+2 < HEIGHT: stdscr.addstr(cy+2,cx,"#")
                    if (cy+1 == enemy[i].ey or cy+2 == enemy[i].ey) and enemy[i].ex == cx:
                        enemy[i].death = True
                if lastmove == "u":
                    if i == 0:
                        stdscr.addstr(cy-1,cx,"#")
                        if cy-2 > 0: stdscr.addstr(cy-2,cx,"#")
                    if (cy-1 == enemy[i].ey or cy-2 == enemy[i].ey) and enemy[i].ex == cx:
                        enemy[i].death = True
                if lastmove == "r":
                    if i == 0:
                        stdscr.addstr(cy,cx+1,"#")
                       
                        if cx+2 < WIDTH: stdscr.addstr(cy,cx+2,"#")
                        if cx+3 < WIDTH: stdscr.addstr(cy,cx+3,"#")
                    if (cx+1 == enemy[i].ex or cx+2 == enemy[i].ex or cx+3 == enemy[i].ex) and enemy[i].ey == cy:
                        enemy[i].death = True
                if lastmove == "l":
                    if i == 0:
                        stdscr.addstr(cy,cx-1,"#")
                        if cx-2 > 0: stdscr.addstr(cy,cx-2,"#")
                        if cx-3 > 0: stdscr.addstr(cy,cx-3,"#")
                    if (cx-1 == enemy[i].ex or cx-2 == enemy[i].ex or cx-3 == enemy[i].ex) and enemy[i].ey == cy:
                        enemy[i].death = True
           
            if lastkey == ord('.') and isdead == False:
                for y in range(3):
                    for x in range(3):
                        if i == 0: stdscr.addstr(cy-1+y,cx-1+x,"#")
                        if cy-1+y == enemy[i].ey and cx-1+x == enemy[i].ex:
                            enemy[i].death = True
       
        if lastkey == ord('r'):
            lastmove = " "
            isdead = False
            enemy = []
            title = "              "
            subtitle = "(use arrows to move, / to attack)"
            cy = 1
            cx = 1
            enemycount = 0
            enemyleft = 0
            enemy = []
            killcount = 0
            start += time
            stdscr.clear()
            stdscr.refresh()

        stdscr.attroff(curses.color_pair(5))
        stdscr.attroff(curses.A_STANDOUT)
           
        stdscr.attron(curses.color_pair(1))
        for i in range(len(enemy)):
            if (enemy[i].ex-1 == cx or enemy[i].ex-2 == cx) and enemy[i].elastmove == "l" and enemy[i].death == False:
                stdscr.addstr(enemy[i].ey, enemy[i].ex-1,"#")
                stdscr.addstr(enemy[i].ey, enemy[i].ex-2,"#")
                if (enemy[i].ex-1 == cx or enemy[i].ex-2 == cx) and enemy[i].ey == cy:
                    isdead = True
            if (enemy[i].ex+1 == cx or enemy[i].ex+2 == cx) and enemy[i].elastmove == "r" and enemy[i].death == False:
                stdscr.addstr(enemy[i].ey, enemy[i].ex+1,"#")
                stdscr.addstr(enemy[i].ey, enemy[i].ex+2,"#")
                if (enemy[i].ex+1 == cx or enemy[i].ex+2 == cx) and enemy[i].ey == cy:
                    isdead = True
            if (enemy[i].ey+1 == cy) and enemy[i].elastmove == "d" and enemy[i].death == False:
                stdscr.addstr(enemy[i].ey+1,enemy[i].ex,"#")
                if (enemy[i].ey+1 == cy and enemy[i].ex == cx):
                    isdead = True
            if (enemy[i].ey-1 == cy) and enemy[i].elastmove == "u" and enemy[i].death == False:
                stdscr.addstr(enemy[i].ey-1,enemy[i].ex,"#")
                if (enemy[i].ey-1 == cy and enemy[i].ex == cx):
                    isdead = True
        stdscr.attroff(curses.color_pair(1))
       
        if isdead == True:
            stdscr.refresh()
            title ="You died. Press r to restart"
            subtitle = f"You killed {killcount} enemies!"
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(y_global, (WIDTH//2) - len(title)//2, title)
            stdscr.addstr(y_global+1, (WIDTH//2) - len(subtitle)//2, subtitle)
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
            isdead = True
       
        for i in range(len(enemy)):
            if enemy[i].death == False:
                stdscr.addstr(enemy[i].ey, enemy[i].ex,"X",curses.color_pair(1))
       
        stdscr.move(cy, cx,)
       
        stdscr.refresh()
       
        lastkey = stdscr.getch() # getch is instead of input
       
def main():
    curses.wrapper(menu)
   

if __name__ == "__main__":
    main()