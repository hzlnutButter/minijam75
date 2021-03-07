import time
from random import randint
import curses

head_side = [
    "    _______  ",
    "   /\  /   \ ",
    "  /  \/ o __\\",
    " /       /  |",
    "/       |__/"]
head_speak = [
    "    _______  ",
    "   /\  /   \ ",
    "  /  \/ o __\\",
    " /       //  ",
    "/       |_\_"]
head_front = [
    " ___________ ",
    "|  /     \  |",
    " \/ o___o \/ ",
    " /  /   \ /  ",
    "/   \___//   "]
head_tilt = [
    " / \_____    ",
    "/_/  o   \__ ",
    "  / ___ o \ |",
    " / /   \  /\|",
    "/  \___/ /   "]
body = [
    "|_________",
    "|                 /",
    "|                /",
    "|    /          /",
    "|  _/\_______| |",
    "| |          | |",
    "|_|          |_|"]
tail_normal = [
    "          ",
    "  ___     ",
    " /   \    ",
    "|  \_/    "]
tail_big = [
    "   ____   ",
    " /      \ ",
    "|        |",
    "|     \_/ ",]

width, height = 100, 50
score_box_height, score_box_width = 5, 30
background, pug = [], []
pug_traits = {"facing": "R", "head": head_side, "tail": tail_normal}
pug_location = int(width/2) - 12
mass, highest_mass = 10, 10
distance = 100
loop_delay, mouth_delay = .1, 0

class Bone():
    registry = []
    def __init__(self):
        if randint(1, 5) == 1:
            self.text = "8===8"
            self.mass = 1
        else:
            self.text = "8=8"
            self.mass = .5
        self.location = randint(1, width-3)
        self.row = height
        self.registry.append(self)
    def capture(self):
        global loop_delay, mouth_delay, pug_traits, mass
        mass += self.mass
        pug_traits["head"] = head_speak
        mouth_delay = time.time()
        self.registry.remove(self)
        if mass > 22:
            loop_delay = .05
        elif mass > 17:
            loop_delay = .075
    def miss(self):
        self.registry.remove(self)

def delay_print(output, window, y, x):
    pace = .04
    for z in range(len(output)):
        window.addstr(y, x+z, output[z])
        window.refresh()
        time.sleep(pace)
        if pace > .005:
           pace = pace - .0005

def update_background():
    global background
    if background:
        if background[0] > 0 or background[1] > 0:
            addition = 0
        else:
            addition = randint(2, width-1)
        background.remove(background[0])
        background.append(addition)
    else:
        for y in range(int(height/3)):
            index = randint(2, width-1)
            for addition in [index, 0, 0]:
                background.append(addition)

def update_pug(traits):
    global pug_traits, pug
    if "facing" in traits:
        pug_traits["facing"] = traits["facing"]
    if "head" in traits:
        pug_traits["head"] = traits["head"]
    if "tail" in traits:
        pug_traits["tail"] = traits["tail"]
    pug = []
    for x in range(4):
        pug.append((pug_traits["tail"])[x] + (pug_traits["head"])[x])
    pug.append(body[0] + (pug_traits["head"])[4])
    for line in body[1:]:
        pug.append(line)
    if pug_traits["facing"] == "L":
        for x in range(len(pug)):
            new_line = ""
            for character in pug[x]:
                if character in "\ " and character != " ":
                    character = "/"
                elif character == "/":
                    character = "\ "[0]
                new_line = character + new_line
            pug[x] = new_line

def main():
    curses.wrapper(game)

def game(win):
    # setup
    global pug_location, pug_traits, background, loop_delay, mouth_delay, mass, highest_mass, distance
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak(True)
    window = curses.newwin(height+2, width+2)
    window.nodelay(True)
    # intro = ["Once, a pug was cast from Earth to fly through outer space", "Lost without a way back home, he sought a brand new place", "Small he was - too light to feel the pull of gravity", "Without treats to weigh him down - help find them, rapidly!"]
    # for i in range(len(intro)):
    #     delay_print(intro[i], window, 4+i, 5)
    #     time.sleep(.5)
    # time.sleep(1)
    while True:
        background = []
        pug_traits = {"facing": "R", "head": head_side, "tail": tail_normal}
        pug_location = int(width/2) - 12
        mass = 10
        distance = 100
        loop_delay = .1
        menu_lines = [("Eat as many bones as you can on your way to Mars, " + str(distance) + " million kilometres away."), "You need to be at least 30 kg, or else the planet's gravitational pull will be too weak.", "Big bones (8===8) are twice as heavy as small bones (8=8).", "", "COMMANDS: move left -> A", "          move right -> D", "          pause -> SPACE", "          restart -> RETURN", "", "PRESS RETURN TO BEGIN"]
        for i in range(len(menu_lines)):
            window.addstr(9+i, 5, menu_lines[i])
        window.nodelay(False)
        while window.getch() != 10:
            continue
        window.nodelay(True)
        while distance > 0:
            start_time = time.time()
            key = window.getch()
            if key == 32: # space (pause)
                window.nodelay(False)
                while window.getch() != 32:
                    continue
                window.nodelay(True)
            elif key == 10: # return (restart)
                break
            elif key == 97 or key == 65: # a or A
                pug_location += -5
                pug_traits["facing"] = "L"
                if pug_location < 1:
                    pug_location = 1
            elif key == 100 or key == 68: # d or D
                pug_location += 5
                pug_traits["facing"] = "R"
                if pug_location > (width-23):
                    pug_location = width-23
            update_background()
            update_pug(pug_traits)
            window.clear()
            for y in range(len(background)): # background
                if background[y] > 0:
                    window.addstr(y+1, background[y], "*")
            if randint(1, 20) == 10: # update bones
                new_bone = Bone()
            for bone in Bone.registry:
                if bone.row > 5 and bone.row < 11:
                    if pug_traits["facing"] == "R":
                        if bone.location > pug_location+12 and bone.location < pug_location+24:
                            bone.capture()
                    elif pug_traits["facing"] == "L":
                        if bone.location > pug_location-4 and bone.location < pug_location+10:
                            bone.capture()
            if pug_traits["head"] == head_speak and (time.time() - mouth_delay >= .2): # pug
                pug_traits["head"] = head_side
                mouth_delay = 0        
            if pug_traits["facing"] == "R":
                for y in range(11):
                    window.addstr((y+6), pug_location+1, pug[y])
            elif pug_traits["facing"] == "L":
                for y in range(4):
                    window.addstr(y+6, pug_location+1, pug[y])
                window.addstr(10, pug_location+2, pug[4])
                for y in range(4):
                    window.addstr(y+11, (pug_location+5+y), pug[y+5])
                for y in range(2):
                    window.addstr(y+15, pug_location+8, pug[9+y])
            for bone in Bone.registry: # place bones
                window.addstr(bone.row, bone.location, bone.text, curses.A_BOLD)
                bone.row += -1
                if bone.row < 1:
                    bone.miss()
            distance += -.1 # score
            window.addstr(score_box_height, width-score_box_width, ("_" * (score_box_width+1)))
            for x in range(score_box_height):
                window.addstr(x+1, width-score_box_width, "|")
            window.addstr(2, width-27, ("MASS: " + str(mass) + " kg"), curses.A_BOLD)
            window.addstr(3, width-27, ("DISTANCE: " + str(int(distance)) + " million km"), curses.A_BOLD)
            if highest_mass > 10:
                window.addstr(4, width-27, ("HIGH SCORE: " + str(highest_mass) + " kg"), curses.A_BOLD)
            window.border(0)
            window.refresh()
            while time.time() - start_time < loop_delay:
                continue
        # post-game
        mars = ["   ____", " /      \\", "(  MARS  )", " \ ____ /"]
        for bone in Bone.registry:
            bone.registry.remove(bone)
        if distance > 0: # you didn't make it
            update_pug({"head": head_front})
            for i in range(height):
                start_time = time.time()
                window.clear()
                for y in range(len(background)):
                    window.addstr(y+1, background[y], "*")
                try:
                    if pug_traits["facing"] == "R":
                        for y in range(11):
                            window.addstr((y+5+(int(i*i/2))), pug_location+1, pug[y])
                    elif pug_traits["facing"] == "L":
                        for y in range(5):
                            window.addstr((y+5+(int(i*i/2))), pug_location+1, pug[y])
                        for y in range(3):
                            window.addstr((y+10+(int(i*i/2))), (pug_location+5+y), pug[y+5])
                        for y in range(3):
                            window.addstr((y+13+(int(i*i/2))), (pug_location+8), pug[y+8])
                except Exception:
                    break
                window.border(0)
                window.refresh()
                while time.time() - start_time < .1:
                    continue
            display_text = "YOU LOST: YOU WERE STILL " + str(int(distance)) + " KM AWAY FROM MARS!"
        elif mass < 30: # not heavy enough
            update_pug({"head": head_front})
            xval, yval = 40, height-3
            for i in range(14):
                start_time = time.time()
                window.clear()
                for y in range(len(background)):
                    window.addstr(y+1, background[y], "*")
                if pug_traits["facing"] == "R":
                    for y in range(11):
                        window.addstr((y+6), pug_location+1, pug[y])
                elif pug_traits["facing"] == "L":
                    for y in range(5):
                        window.addstr(y+6, pug_location+1, pug[y])
                    for y in range(4):
                        window.addstr(y+11, (pug_location+5+y), pug[y+5])
                    for y in range(2):
                        window.addstr(y+15, pug_location+8, pug[9+y])
                if i == 0:
                    window.addstr(height, 25, mars[0])
                elif i == 1:
                    window.addstr(height-2, 30, mars[0])
                    window.addstr(height-1, 30, mars[1])
                elif i == 2:
                    window.addstr(height-4, 35, mars[0])
                    window.addstr(height-3, 35, mars[1])
                    window.addstr(height-2, 35, mars[2])
                else:
                    try:
                        window.addstr(yval-3, xval, mars[0])
                        window.addstr(yval-2, xval, mars[1])
                        window.addstr(yval-1, xval, mars[2])
                        window.addstr(yval, xval, mars[3])
                        xval += 5
                        yval += -2
                    except Exception:
                        break
                window.border(0)
                window.refresh()
                while time.time() - start_time < .15:
                    continue
            display_text = "YOU LOST: YOU WERE ONLY " + str(mass) + " KG, AND MARS'S GRAVITATIONAL PULL WAS TOO WEAK."
        else: # win
            update_pug({"head": head_front})
            yval = height-3
            for i in range(int((height-15) / 2)):
                start_time = time.time()
                window.clear()
                for y in range(len(background)):
                    window.addstr(y+1, background[y], "*")
                if pug_traits["facing"] == "R":
                    for y in range(11):
                        window.addstr((y+6), pug_location+1, pug[y])
                elif pug_traits["facing"] == "L":
                    for y in range(5):
                        window.addstr(y+6, pug_location+1, pug[y])
                    for y in range(4):
                        window.addstr(y+11, (pug_location+5+y), pug[y+5])
                    for y in range(2):
                        window.addstr(y+15, pug_location+8, pug[9+y])
                if i == 0:
                    window.addstr(height, pug_location, mars[0])
                elif i == 1:
                    window.addstr(height-2, pug_location, mars[0])
                    window.addstr(height-1, pug_location, mars[1])
                elif i == 2:
                    window.addstr(height-4, pug_location, mars[0])
                    window.addstr(height-3, pug_location, mars[1])
                    window.addstr(height-2, pug_location, mars[2])
                else:
                    window.addstr(yval-3, pug_location, mars[0])
                    window.addstr(yval-2, pug_location, mars[1])
                    window.addstr(yval-1, pug_location, mars[2])
                    window.addstr(yval, pug_location, mars[3])
                    yval += -2
                window.border(0)
                window.refresh()
                while time.time() - start_time < .15:
                    continue
            display_text = "CONGRATULATIONS, YOU MADE IT TO MARS! NOW YOU CAN MAKE A NEW HOME."
        window.clear()
        if mass > highest_mass:
            window.addstr(6, 5, ("NEW HIGH SCORE: " + str(mass)), curses.A_BOLD)
            highest_mass = mass
        window.addstr(5, 5, display_text, curses.A_BOLD)

main()