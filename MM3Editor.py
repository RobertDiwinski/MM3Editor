#!/usr/bin/python3

import curses
import sys

NAME_LENGTH = 0xA

GOLD_BANK = 0x2E85
GEMS_BANK = 0x2E89
FOOD = 0x2E7D
GOLD = 0x2E8D
GEMS = 0x2E91
CHARACTER1 = 0x07A1
CHARACTER2 = 0x1833
CHARACTER3 = 0x1CEF
CHARACTER4 = 0x1119
CHARACTER5 = 0x14A6
CHARACTER6 = 0x0EBB
STRENGTH = 0x14
INTELLIGENCE = 0x16
PERSONALITY = 0x18
STAMINA = 0x1A
SPEED = 0x1C
ACCURACY = 0x1E
LUCK = 0x20
LEVEL = 0x23
HITPOINTS = 0x125
SPELLPOINTS = 0x127

class TextBox():
    def __init__(self, y, x, text, max_length, is_numeric):
        if (is_numeric): self.text = str(text)
        else: self.text = text
        
        self.pos = len(self.text)
        self.max_length = max_length
        self.y = y
        self.x = x
        self.is_numeric = is_numeric
        
        if (is_numeric): scr.addstr(y, x, self.text)
        else: scr.addstr(y, x, text)
    
    def handle_char(self, c):
        if (self.is_numeric and c >= 48 and c <= 57):
            self.text += chr(c)
            self.pos += 1
            
            if (int(self.text) > self.max_length):
                self.text = str(self.max_length)
                self.pos = len(self.text)
            
            scr.addstr(self.y, self.x, self.text)
        elif (not self.is_numeric and (((c >= 48 and c <= 57) or (c >= 65 and c <= 90) or (c >= 97 and c <= 122) or c == 32) and self.pos < self.max_length)):
            self.text += chr(c)
            self.pos += 1
            scr.addstr(self.y, self.x, self.text)
        elif (c == curses.KEY_BACKSPACE and self.pos > 0):
            self.text = self.text[:-1]
            scr.addstr(self.y, self.x + self.pos - 1, " ")
            self.pos -= 1
            scr.addstr(self.y, self.x, self.text)

def read_file(file):
    f = open(file, "rb")
    ret = f.read()
    f.close()
    
    return bytearray(ret)

def write_file(file, buf):
    f = open(file, "wb");
    f.write(buf)
    f.close()
    
def read_uint32(buf, offset):
    return int.from_bytes([buf[offset], buf[offset + 1], buf[offset + 2], buf[offset + 3]], "little", signed=False)

def read_uint16(buf, offset):
    return int.from_bytes([buf[offset], buf[offset + 1]], "little", signed=False)

def read_string(buf, offset, length):
    bb = buf[offset:offset + length]
    
    for x in range(0, length):
        if (bb[x] == 0):
            bb[x] = 0x20
    
    return bb.decode("ascii")

def write_uint32(buf, offset, value):
    bb = value.to_bytes(4, "little", signed=False)
    buf[offset] = bb[0]
    buf[offset + 1] = bb[1]
    buf[offset + 2] = bb[2]
    buf[offset + 3] = bb[3]
    
def write_uint16(buf, offset, value):
    bb = value.to_bytes(2, "little", signed=False)
    buf[offset] = bb[0]
    buf[offset + 1] = bb[1]

def write_string(buf, offset, text, max_length):
    bb = text.encode("ascii")
    
    for x in range(offset, offset + max_length):
        if (x - offset < len(bb)): buf[x] = bb[x - offset]
        else: buf[x] = 0

def draw_main_window(buf, highlight):
    c1 = read_string(buf, CHARACTER1, NAME_LENGTH)
    c2 = read_string(buf, CHARACTER2, NAME_LENGTH)
    c3 = read_string(buf, CHARACTER3, NAME_LENGTH)
    c4 = read_string(buf, CHARACTER4, NAME_LENGTH)
    c5 = read_string(buf, CHARACTER5, NAME_LENGTH)
    c6 = read_string(buf, CHARACTER6, NAME_LENGTH)
    
    scr.addstr(0, 0,  "                            ┌───────────────────────────────────┐            ")
    scr.addstr(1, 0,  "                            │ Might And Magic 3 Savegame Editor │            ")
    scr.addstr(2, 0,  "┌──┬────────────┬───────────┴───────────────────────────────────┴───────────┐")
    scr.addstr(3, 0,  "│F1│ " + c1 + " │                                                           │")
    scr.addstr(4, 0,  "├──┼────────────┤                                                           │")
    scr.addstr(5, 0,  "│F2│ " + c2 + " │                                                           │")
    scr.addstr(6, 0,  "├──┼────────────┤                                                           │")
    scr.addstr(7, 0,  "│F3│ " + c3 + " │                                                           │")
    scr.addstr(8, 0,  "├──┼────────────┤                                                           │")
    scr.addstr(9, 0,  "│F4│ " + c4 + " │                                                           │")
    scr.addstr(10, 0, "├──┼────────────┤                                                           │")
    scr.addstr(11, 0, "│F5│ " + c5 + " │                                                           │")
    scr.addstr(12, 0, "├──┼────────────┤                                                           │")
    scr.addstr(13, 0, "│F6│ " + c6 + " │                                                           │")
    scr.addstr(14, 0, "├──┼────────────┤                                                           │")
    scr.addstr(15, 0, "│F7│ Party      │                                                           │")
    scr.addstr(16, 0, "├──┼────────────┤                                                           │")
    scr.addstr(17, 0, "│F8│ Save       │                                                           │")
    scr.addstr(18, 0, "├──┼────────────┤                                                           │")
    scr.addstr(19, 0, "│F9│ Quit       │                                                           │")
    scr.addstr(20, 0, "└──┴────────────┤                                                           │")
    scr.addstr(21, 0, "                │                                                           │")
    scr.addstr(22, 0, "                └───────────────────────────────────────────────────────────┘")
    
    if (highlight == 0): scr.addstr(3, 5, c1, curses.color_pair(1))
    elif (highlight == 1): scr.addstr(5, 5, c2, curses.color_pair(1))
    elif (highlight == 2): scr.addstr(7, 5, c3, curses.color_pair(1))
    elif (highlight == 3): scr.addstr(9, 5, c4, curses.color_pair(1))
    elif (highlight == 4): scr.addstr(11, 5, c5, curses.color_pair(1))
    elif (highlight == 5): scr.addstr(13, 5, c6, curses.color_pair(1))
    elif (highlight == 6): scr.addstr(15, 5, "Party", curses.color_pair(1))

def draw_character_props(buf, offset, textbox):
    global current_offset
    global current_textbox
    
    name = read_string(buf, offset, NAME_LENGTH).strip()
    strength = read_uint16(buf, offset + STRENGTH);
    intelligence = read_uint16(buf, offset + INTELLIGENCE);
    personality = read_uint16(buf, offset + PERSONALITY);
    stamina = read_uint16(buf, offset + STAMINA);
    speed = read_uint16(buf, offset + SPEED);
    accuracy = read_uint16(buf, offset + ACCURACY);
    luck = read_uint16(buf, offset + LUCK);
    level = read_uint16(buf, offset + LEVEL);
    hitpoints = read_uint16(buf, offset + HITPOINTS);
    spellpoints = read_uint16(buf, offset + SPELLPOINTS);
    
    if (offset == CHARACTER1): draw_main_window(buf, 0)
    elif (offset == CHARACTER2): draw_main_window(buf, 1)
    elif (offset == CHARACTER3): draw_main_window(buf, 2)
    elif (offset == CHARACTER4): draw_main_window(buf, 3)
    elif (offset == CHARACTER5): draw_main_window(buf, 4)
    elif (offset == CHARACTER6): draw_main_window(buf, 5)
    
    scr.addstr(3, 18,  "Name:         " + name)
    scr.addstr(5, 18,  "Strength:     " + str(strength))
    scr.addstr(7, 18,  "Intelligence: " + str(intelligence))
    scr.addstr(9, 18,  "Personality:  " + str(personality))
    scr.addstr(11, 18, "Stamina:      " + str(stamina))
    scr.addstr(13, 18, "Speed:        " + str(speed))
    scr.addstr(15, 18, "Accuracy:     " + str(accuracy))
    scr.addstr(17, 18, "Luck:         " + str(luck))
    scr.addstr(19, 18, "Level:        " + str(level))
    scr.addstr(21, 18, "Hitpoints:    " + str(hitpoints))
    scr.addstr(3, 48,  "Spellpoints:  " + str(spellpoints))
    
    if (textbox == 0): create_textbox(3, 32, name, 10, False)
    elif (textbox == 1): create_textbox(5, 32, strength, 2**16 - 1, True)
    elif (textbox == 2): create_textbox(7, 32, intelligence, 2**16- 1, True)
    elif (textbox == 3): create_textbox(9, 32, personality, 2**16 - 1, True)
    elif (textbox == 4): create_textbox(11, 32, stamina, 2**16 - 1, True)
    elif (textbox == 5): create_textbox(13, 32, speed, 2**16 - 1, True)
    elif (textbox == 6): create_textbox(15, 32, accuracy, 2**16 - 1, True)
    elif (textbox == 7): create_textbox(17, 32, luck, 2**16 - 1, True)
    elif (textbox == 8): create_textbox(19, 32, level, 2**16 - 1, True)
    elif (textbox == 9): create_textbox(21, 32, hitpoints, 2**16 - 1, True)
    elif (textbox == 10): create_textbox(3, 62, spellpoints, 2**16 - 1, True)
    
    current_textbox = textbox
    current_offset = offset
    
def draw_party_props(buf, textbox):
    global current_offset
    global current_textbox
    
    gold = read_uint32(buf, GOLD)
    gems = read_uint32(buf, GEMS)
    food = read_uint16(buf, FOOD)
    gold_bank = read_uint32(buf, GOLD_BANK)
    gems_bank = read_uint32(buf, GEMS_BANK)
    
    draw_main_window(buf, 6)
    
    scr.addstr(3, 18,  "Food:       " + str(food))
    scr.addstr(5, 18,  "Gold Party: " + str(gold))
    scr.addstr(7, 18,  "Gems Party: " + str(gems))
    scr.addstr(9, 18,  "Gold Bank:  " + str(gold_bank))
    scr.addstr(11, 18, "Gems Bank:  " + str(gems_bank))
    
    current_offset = -1
    current_textbox = textbox
    
    if (textbox == 0): create_textbox(3, 30, food, 2**16 - 1, True)
    elif (textbox == 1): create_textbox(5, 30, gold, 2**32 - 1, True)
    elif (textbox == 2): create_textbox(7, 30, gems, 2**32 - 1, True)
    elif (textbox == 3): create_textbox(9, 30, gold_bank, 2**32 - 1, True)
    elif (textbox == 4): create_textbox(11, 30, gems_bank, 2**32 - 1, True)
    
def create_textbox(y, x, text, max_length, is_numeric):
    global tb
    tb = TextBox(y, x, text, max_length, is_numeric)

def next_textbox():
    write_value()
    
    global current_offset
    global current_textbox
    
    if ((current_offset == -1 and current_textbox == 4) or current_textbox == 10): current_textbox = 0
    else: current_textbox += 1
    
    if (current_offset == -1): draw_party_props(buf, current_textbox)
    else: draw_character_props(buf, current_offset, current_textbox)
    
def prev_textbox():
    write_value()
        
    global current_offset
    global current_textbox
    
    if (current_textbox == 0):
        if (current_offset == -1): current_textbox = 4
        else: current_textbox = 10
    else: current_textbox -= 1
    
    if (current_offset == -1): draw_party_props(buf, current_textbox)
    else: draw_character_props(buf, current_offset, current_textbox)
    
def string_to_int(text):
    if (len(text) == 0): return 0
    return int(text)
    
def write_value():
    global current_offset
    global current_textbox
    global tb
    
    if (current_offset == -1):
        if (current_textbox == 0): write_uint16(buf, FOOD, string_to_int(tb.text))
        elif (current_textbox == 1): write_uint32(buf, GOLD, string_to_int(tb.text))
        elif (current_textbox == 2): write_uint32(buf, GEMS, string_to_int(tb.text))
        elif (current_textbox == 3): write_uint32(buf, GOLD_BANK, string_to_int(tb.text))
        elif (current_textbox == 4): write_uint32(buf, GEMS_BANK, string_to_int(tb.text))
    elif (current_offset > 0):
        if (current_textbox == 0): write_string(buf, current_offset, tb.text, 10)
        elif (current_textbox == 1): write_uint16(buf, current_offset + STRENGTH, string_to_int(tb.text))
        elif (current_textbox == 2): write_uint16(buf, current_offset + INTELLIGENCE, string_to_int(tb.text))
        elif (current_textbox == 3): write_uint16(buf, current_offset + PERSONALITY, string_to_int(tb.text))
        elif (current_textbox == 4): write_uint16(buf, current_offset + STAMINA, string_to_int(tb.text))
        elif (current_textbox == 5): write_uint16(buf, current_offset + SPEED, string_to_int(tb.text))
        elif (current_textbox == 6): write_uint16(buf, current_offset + ACCURACY, string_to_int(tb.text))
        elif (current_textbox == 7): write_uint16(buf, current_offset + LUCK, string_to_int(tb.text))
        elif (current_textbox == 8): write_uint16(buf, current_offset + LEVEL, string_to_int(tb.text))
        elif (current_textbox == 9): write_uint16(buf, current_offset + HITPOINTS, string_to_int(tb.text))
        elif (current_textbox == 10): write_uint16(buf, current_offset + SPELLPOINTS, string_to_int(tb.text))

file = sys.argv[1]
buf = read_file(file)

scr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
scr.keypad(True)
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

current_offset = -2
current_textbox = -1
draw_character_props(buf, CHARACTER1, 0)

while True:
    c = scr.getch()
  
    if (c == curses.KEY_F1): 
        write_value()
        draw_character_props(buf, CHARACTER1, 0)
    elif (c == curses.KEY_F2): 
        write_value()
        draw_character_props(buf, CHARACTER2, 0)
    elif (c == curses.KEY_F3): 
        write_value()
        draw_character_props(buf, CHARACTER3, 0)
    elif (c == curses.KEY_F4): 
        write_value()
        draw_character_props(buf, CHARACTER4, 0)
    elif (c == curses.KEY_F5): 
        write_value()
        draw_character_props(buf, CHARACTER5, 0)
    elif (c == curses.KEY_F6): 
        write_value()
        draw_character_props(buf, CHARACTER6, 0)
    elif (c == curses.KEY_F7): 
        write_value()
        draw_party_props(buf, 0)
    elif (c == curses.KEY_F8): 
        write_value()
        write_file(file, buf)
    elif (c == curses.KEY_F9): break
    elif (c == curses.KEY_UP): prev_textbox()
    elif (c == curses.KEY_DOWN): next_textbox()
    else: tb.handle_char(c)

curses.nocbreak()
scr.keypad(False)
curses.echo()
curses.endwin()
