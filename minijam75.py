from os import system
import time
from random import randint
import curses

head_side = [
    "    _______  ",
    "   /\  /   \ ",
    "  /  \/ o __\\",
    " /       /  |",
    "/       |__/ "]
head_speak = [
    "    _______  ",
    "   /\  /   \ ",
    "  /  \/ o __\\",
    " /       //  ",
    "/       |_\_ "]
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
    "|                / ",
    "|    /          /  ",
    "|  _/\_______| |   ",
    "| |          | |   ",
    "|_|          |_|   "]
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

width = 100 # width and height must be even
height = 50
background = []
pug_traits = {"facing": "R", "head": head_side, "tail": tail_normal}
pug = []
pug_location = int(width/2) - 12
intro = ["Once there was a puppy who was gliding through the sky",
    "Fearless, he did not observe he had not wings to fly",
    "Looking down, he saw below the quickly gaining ground",
    "Still unfazed, along the way, he ate each treat he found..."]
bones_captured = 0
bones_missed = 0
best_accuracy = 0
goal_bones = 20
goal_loop_ms = 100
speak_time = None

class Bone():
    registry = []
    def __init__(self):
        self.text = "8=8"
        self.location = randint(1, width-3)
        self.current_row = height
        self.registry.append(self)
    def capture(self):
        global bones_captured, goal_loop_ms, speak_time, pug_traits
        bones_captured += 1
        pug_traits["head"] = head_speak
        speak_time = time.time()
        if bones_captured == int(goal_bones * .2):
            goal_loop_ms += -30
        elif bones_captured == int(goal_bones * .4):
            goal_loop_ms += -10
        elif bones_captured == int(goal_bones * .65):
            goal_loop_ms += -10
        self.registry.remove(self)
    def miss(self):
        global bones_missed
        bones_missed += 1
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
        if "*" in background[0]:
            new_line = width * " "
        else:
            spaces_before = randint(1, width-1)
            spaces_after = width - 1 - spaces_before
            new_line = (" " * spaces_before) + "*" + (" " * spaces_after)
        background.remove(background[0])
        background.append(new_line)
        for x in range(len(background)):
            if "_" in background[x]:
                background[x] = background[x].replace("_", " ")
                break
    else:
        for x in range(int(height/2)):
            spaces_before = randint(1, width-1)
            spaces_after = width - 1 - spaces_before
            background.append((" " * spaces_before) + "*" + (" " * spaces_after))
            background.append(width * " ")

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
    global pug_location, pug_traits, best_accuracy, background, bones_missed, bones_captured, goal_loop_ms, speak_time
    curses.noecho()
    curses.curs_set(0)
    curses.cbreak(True)
    window = curses.newwin(height+2, width+2)
    window.nodelay(True)
    # intro
    # delay_print(intro[0], window, 4, 5)
    # time.sleep(.5)
    # delay_print(intro[1], window, 5, 5)
    # time.sleep(.5)
    # delay_print(intro[2], window, 6, 5)
    # time.sleep(.5)
    # delay_print(intro[3], window, 7, 5)
    # time.sleep(1.5)
    while True:
        window.addstr(9, 5, "HOW TO PLAY: Eat " + str(goal_bones) + " bones before you hit the ground!", curses.A_BOLD)
        window.addstr(11, 5, "COMMANDS: move left -> A")
        window.addstr(12, 15, "move right -> D")
        window.addstr(13, 15, "pause -> SPACE")
        window.addstr(14, 15, "restart -> RETURN")
        window.addstr(16, 5, "PRESS RETURN TO BEGIN", curses.A_BOLD)
        window.nodelay(False)
        while True:
            key = window.getch()
            if key == 10:
                break
        window.nodelay(True)
        background = []
        pug_traits = {"facing": "R", "head": head_side, "tail": tail_normal}
        pug_location = int(width/2) - 12
        bones_captured = 0
        bones_missed = 0
        goal_loop_ms = 100
        while bones_captured < goal_bones and bones_missed < goal_bones:
            start_time_ms = int(time.time() * 1000)
            key = window.getch()
            if key == 32: # space (pause)
                window.nodelay(False)
                key = window.getch()
                window.nodelay(True)
            elif key == 10: # return (restart)
                break
            if key == 97: # a
                pug_location += -5
                pug_traits["facing"] = "L"
                if pug_location < 1:
                    pug_location = 1
            elif key == 100: # d
                pug_location += 5
                pug_traits["facing"] = "R"
                if pug_location > (width-23):
                    pug_location = width-23
            update_background()
            update_pug(pug_traits)
            window.clear()
            # background
            for y in range(len(background)):
                window.addstr(y+1, 1, background[y])
            # pug
            if pug_traits["facing"] == "R":
                for y in range(11):
                    window.addstr((y+5), pug_location+1, pug[y])
            elif pug_traits["facing"] == "L":
                for y in range(5):
                    window.addstr((y+5), pug_location+1, pug[y])
                for y in range(6):
                    window.addstr((y+10), (pug_location+5), pug[y+5])
            # bone
            if randint(1, 25) == 10:
                bone = Bone()
            for each_bone in Bone.registry:
                if each_bone.current_row > 4 and each_bone.current_row < 11:
                    if pug_traits["facing"] == "R":
                        if each_bone.location > (pug_location + 10) and each_bone.location < (pug_location + 24):
                            each_bone.capture()
                    elif pug_traits["facing"] == "L":
                        if each_bone.location > (pug_location - 4) and each_bone.location < (pug_location + 10):
                            each_bone.capture()
                window.addstr(each_bone.current_row, each_bone.location, each_bone.text, curses.A_BOLD)
                each_bone.current_row += -1
                if each_bone.current_row < 1:
                    each_bone.miss()
            if pug_traits["head"] == head_speak:
                if time.time() - speak_time >= .2:
                    pug_traits["head"] = head_side
                    speak_time = None
            # score
            score_box_height = 6
            score_box_width = 20
            window.addstr(height-score_box_height, width-score_box_width, ("_" * (score_box_width+1)))
            for x in range(score_box_height):
                window.addstr(height-x, width-score_box_width, "|")
            window.addstr(height-4, width-17, ("BONES: " + str(bones_captured)), curses.A_BOLD)
            window.addstr(height-3, width-17, ("MISSED: " + str(bones_missed)), curses.A_BOLD)
            window.addstr(height-2, width-17, ("WEIGHT: " + str(20+bones_captured) + " lbs"), curses.A_BOLD)
            if best_accuracy > 0:
                window.addstr(height-1, width-17, ("HIGH SCORE: " + str(best_accuracy) + "%"), curses.A_BOLD)
            window.border(0)
            window.refresh()
            # time stuff
            while True:
                end_time_ms = int(time.time() * 1000)
                time_elapsed_ms = end_time_ms - start_time_ms
                if time_elapsed_ms >= goal_loop_ms:
                    break
        # post-game
        for each_bone in Bone.registry:
            each_bone.registry.remove(each_bone)
        if bones_captured >= goal_bones:
            window.clear()
            try:
                accuracy_rate = int(bones_captured / (bones_captured + bones_missed) * 100)
            except ZeroDivisionError:
                accuracy_rate = 0
            if accuracy_rate > best_accuracy:
                window.addstr(4, 5, "NEW HIGH SCORE!", curses.A_BOLD)
                best_accuracy = accuracy_rate
            window.addstr(5, 5, ("You got " + str(bones_captured) + " bones, and you missed " + str(bones_missed) + ". Your accuracy rate was " + str(accuracy_rate) + "%."))
        else: # you lose
            update_pug({"head": head_front})
            time.sleep(.5)
            for i in range(height-18):
                window.clear()
                # background
                for y in range(len(background)):
                    window.addstr(y+1, 1, background[y])
                # pug
                try:
                    if pug_traits["facing"] == "R":
                        for y in range(11):
                            window.addstr((y+5+(int(i*i/2))), pug_location+1, pug[y])
                    elif pug_traits["facing"] == "L":
                        for y in range(5):
                            window.addstr((y+5+(int(i*i/2))), pug_location+1, pug[y])
                        for y in range(6):
                            window.addstr((y+10+(int(i*i/2))), (pug_location+5), pug[y+5])
                except Exception:
                    break
                # score
                score_box_height = 5
                score_box_width = 20
                window.addstr(height-score_box_height, width-score_box_width, ("_" * (score_box_width+1)))
                for x in range(score_box_height):
                    window.addstr(height-x, width-score_box_width, "|")
                window.addstr(height-3, width-17, ("BONES: " + str(bones_captured)), curses.A_BOLD)
                window.addstr(height-2, width-17, ("MISSED: " + str(bones_missed)), curses.A_BOLD)
                if best_accuracy > 0:
                    window.addstr(height-1, width-17, ("HIGH SCORE: " + str(best_accuracy) + "%"), curses.A_BOLD)
                window.border(0)
                window.refresh()
                time.sleep(.1)
            window.clear()
            window.addstr(4, 5, "You only got " + str(bones_captured) + " bones before you crashed :(")

main()