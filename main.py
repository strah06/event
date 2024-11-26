import keyboard
import time
import pyautogui as pag
import autoit
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
import regex as re
import requests
import os

discord_webhook = "https://discord.com/api/webhooks/1310981065518743583/m4hon93xL7Dt2SedL8smswz3bT7s_Wo4x_6OKrQ3ZO5_cEV4rAFCgaMD5jFDmoA8ccFf"

#kartice sa pocetka
renge_dmg = 254, 126, 34
talisman_buff = 194, 194, 254
no_traits = 150, 196, 172
monrach_buff = 254, 34, 34
money_surge = 254, 221, 34

#kartice za buffovanje
strong_or_dmg = 254, 62, 65
slayer = 154, 71, 254
speed = 0, 115, 254
press = 90, 254, 112
cooldown = 43, 173, 254
dodge = 203, 237, 254
rangee = 255, 254, 124
harvest = 114, 207, 254
mini_boss = 254, 0, 42

#unit koordinate
takorada = (1513, 666)
toji1 = (881, 521)
sukuna1 = (429, 968)
alucard = (902, 394)
gojo = (944, 381)
julius = (916, 349)
sukuna2 = (994, 380)
toji2 = (954, 516)

#unit stanje
takorada_upgrade = 0

takorada_placed = False
alucard_placed = False
gojo_placed = False
julius_placed = False
toji_placed = False
sukuna_placed = False

#uzete kartice
dodge_amount = 0
strong_amount = 0
press_amount = 0
speed_amount = 0

#bossevi
boss_pos = 648, 193

normal_boss = 160,13,16
shielded_boss = 181,181,0
talisman_boss = 122,23,181
no_boss = 115, 102, 84

#stage
uradeni_stage = 0

def screenshot():
    image = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    image.save(screenshot_path)
    return screenshot_path

def send_to_discord(file_path):
    requests.post(discord_webhook, files={"file": open(file_path, "rb")})
    os.remove(file_path)

def mouse_click_at(x,y):
    autoit.mouse_move(x,y)
    autoit.mouse_click("left")

def choose_buff():
    x = [702,942,1182]
    y = [368,368,368]

    buffs = {}

    for i in range(3):
        buffs[i] = pag.pixel(x[i], y[i])

    talisman_buff_position = find_talisman_buff(buffs)

    if talisman_buff_position != None:
        mouse_click_at(x[talisman_buff_position], y[talisman_buff_position]+10)
        return True
    return False


def find_talisman_buff(buffs):
    for i in range(3):
        if  buffs[i][0] <= talisman_buff[0]+2 and buffs[i][0] >= talisman_buff[0]-2 and buffs[i][1] <= talisman_buff[1]+2 and buffs[i][1] >= talisman_buff[1]-2:
            return i
    return None

def restart_game():
    mouse_click_at(973, 541)
    time.sleep(0.5)
    mouse_click_at(886, 199)
    time.sleep(6)
    mouse_click_at(30, 1009)
    time.sleep(0.5)
    mouse_click_at(1202, 498)
    time.sleep(0.5)
    mouse_click_at(849, 557)
    time.sleep(0.5)
    mouse_click_at(968, 567)
    time.sleep(0.5)
    mouse_click_at(1316, 182)
    time.sleep(0.5)

#gpt goat
def preprocess_image_advanced(image_path):
    """Napredna obrada slike za stilizovan tekst."""
    # Učitavanje slike
    img = cv2.imread(image_path)

    # Pretvaranje slike u sivu skalu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Povećavanje kontrasta i uklanjanje šuma
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Erozija i dilatacija (poboljšanje oblika teksta)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Spasavanje obrađene slike za vizuelnu proveru (opciono)
    cv2.imwrite("advanced_processed_image.png", processed)

    return processed

def current_money():
    region = (903,881,1013,906)
    screen = ImageGrab.grab(bbox=region)
    screen.save("test.png")
    processed_screen = preprocess_image_advanced("test.png")
    money = pytesseract.image_to_string(processed_screen, lang="eng", config="--psm 7")
    numbers = re.findall(r"\d+", money)
    if not numbers:
        return None
    money = ''.join(numbers)
    return int(money)

def place_unit(unit, unitpos):
    keyboard.press_and_release(str(unitpos))
    time.sleep(0.5)
    mouse_click_at(unit[0],unit[1])

def boss_spawned():
    pixel = pag.pixel(boss_pos[0], boss_pos[1])

    if pixel[0] <= normal_boss[0]+10 and pixel[0] >= normal_boss[0]-10 and pixel[1] <= normal_boss[1]+10 and pixel[1] >= normal_boss[1]-10 and pixel[2] <= normal_boss[2]+10 and pixel[2] >= normal_boss[2]-10:
        return 0
    if pixel[0] <= shielded_boss[0]+10 and pixel[0] >= shielded_boss[0]-10 and pixel[1] <= shielded_boss[1]+10 and pixel[1] >= shielded_boss[1]-10 and pixel[2] <= shielded_boss[2]+10 and pixel[2] >= shielded_boss[2]-10:
        return 1
    if pixel[0] <= talisman_boss[0]+10 and pixel[0] >= talisman_boss[0]-10 and pixel[1] <= talisman_boss[1]+10 and pixel[1] >= talisman_boss[1]-10 and pixel[2] <= talisman_boss[2]+10 and pixel[2] >= talisman_boss[2]-10:
        return 2
    if pixel[0] <= no_boss[0]+10 and pixel[0] >= no_boss[0]-10 and pixel[1] <= no_boss[1]+10 and pixel[1] >= no_boss[1]-10 and pixel[2] <= no_boss[2]+10 and pixel[2] >= no_boss[2]-10:
        return -1
    return 3

def upgrade_unit(unit):
    failed = (164, 75, 77)
    mouse_click_at(unit[0]+5,unit[1])
    time.sleep(0.7)
    if is_unit_really_placed() == False:
        print("Upgrade nije uspeo")
        return False
    pixel = pag.pixel(unit_placed_pos[0],unit_placed_pos[1])
    print(pag.pixel(unit_placed_pos[0],unit_placed_pos[1]))
    if pixel[0] <= unit_placed2[0]+10 and pixel[0] >= unit_placed2[0]-10 and pixel[1] <= unit_placed2[1]+10 and pixel[1] >= unit_placed2[1]-10:
        print("Nema se dovoljno novca")
        return False
    before = is_upgrade_really_upgraded()
    time.sleep(0.2)
    keyboard.press_and_release('t')
    time.sleep(0.2)
    pixel = pag.pixel(832, 823)
    print(pixel)
    time.sleep(0.2)
    after = is_upgrade_really_upgraded()
    print(before, after)
    if before == None or after == None:
        before = 0
        after = 1
    
    
    
    if pixel[0] <= failed[0]+20 and pixel[0] >= failed[0]-20 and pixel[1] <= failed[1]+20 and pixel[1] >= failed[1]-20:
        print("Nije uspeo upgrade")
        return False
    print("Upgrade je uspeo")
    return True

def sell_unit(unit):
    mouse_click_at(unit[0]-5, unit[1])
    time.sleep(0.5)
    keyboard.press_and_release('x')
    time.sleep(0.7)
    if is_unit_really_placed() == False:
        print("nije prodat")
        return True
    print("prodat")
    return False

def auto_ability(unit):
    mouse_click_at(unit[0],unit[1]-5)
    time.sleep(0.5)
    mouse_click_at(598,382)
    time.sleep(0.2)
    mouse_click_at(1791, 935)

def choose_card():
    global dodge_amount,strong_amount,press_amount,speed_amount
    x = [657,885,1117]
    y = [368,368,368]

    buffs = {}

    for i in range(3):
        buffs[i] = pag.pixel(x[i], y[i])


    #harvest
    for i in range(3):
        if buffs[i][0] <= harvest[0]+2 and buffs[i][0] >= harvest[0]-2 and buffs[i][1] <= harvest[1]+2 and buffs[i][1] >= harvest[1]-2:
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #press
    for i in range(3):
        if  press_amount < 3 and buffs[i][0] <= press[0]+2 and buffs[i][0] >= press[0]-2 and buffs[i][1] <= press[1]+2 and buffs[i][1] >= press[1]-2:
            press_amount+=1
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #boss
    for i in range(3):
        if buffs[i][0] <= mini_boss[0]+2 and buffs[i][0] >= mini_boss[0]-2 and buffs[i][1] <= mini_boss[1]+2 and buffs[i][1] >= mini_boss[1]-2:
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #speed
    for i in range(3):
        if speed_amount < 4 and buffs[i][0] <= speed[0]+2 and buffs[i][0] >= speed[0]-2 and buffs[i][1] <= speed[1]+2 and buffs[i][1] >= speed[1]-2:
            speed_amount+=1
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #strong
    for i in range(3):
        if strong_amount < 4 and buffs[i][0] <= strong_or_dmg[0]+2 and buffs[i][0] >= strong_or_dmg[0]-2 and buffs[i][1] <= strong_or_dmg[1]+2 and buffs[i][1] >= strong_or_dmg[1]-2:
            strong_amount+=1
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #dodge
    for i in range(3):
        if  dodge_amount < 3 and buffs[i][0] <= dodge[0]+2 and buffs[i][0] >= dodge[0]-2 and buffs[i][1] <= dodge[1]+2 and buffs[i][1] >= dodge[1]-2:
            dodge_amount+=1
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #slayer
    for i in range(3):
        if buffs[i][0] <= slayer[0]+2 and buffs[i][0] >= slayer[0]-2 and buffs[i][1] <= slayer[1]+2 and buffs[i][1] >= slayer[1]-2:
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #range
    for i in range(3):
        if buffs[i][0] <= rangee[0]+2 and buffs[i][0] >= rangee[0]-2 and buffs[i][1] <= rangee[1]+2 and buffs[i][1] >= rangee[1]-2:
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True
    #cooldown
    for i in range(3):
        if buffs[i][0] <= cooldown[0]+2 and buffs[i][0] >= cooldown[0]-2 and buffs[i][1] <= cooldown[1]+2 and buffs[i][1] >= cooldown[1]-2:
            mouse_click_at(x[i], y[i]+10)
            time.sleep(0.7)
            return True


game_started = False

def init_game():
    global takorada_placed, takorada_upgrade, toji_placed, sukuna_placed, game_started
    while(True):
        money = current_money()
        time.sleep(0.1)
        print("current money: ", money)
        choose_card()
        if money is None:
            continue
        if money > 800 and takorada_placed == False:
            place_unit(takorada, 4)
            takorada_placed = True
            money = 0
        if money > 1500 and takorada_placed and takorada_upgrade == 0:
            upgrade_unit(takorada)
            takorada_upgrade += 1
            time.sleep(3.5)
            money = 0
        if money > 1500 and toji_placed == False and takorada_upgrade == 1:
            place_unit(toji1, 5)
            toji_placed = True
            money = 0
            time.sleep(0.2)
        if money > 2000 and toji_placed == True and takorada_upgrade == 1 and sukuna_placed == False:
            place_unit(sukuna1, 6)
            if is_unit_really_placed() == False:
                continue
            sukuna_placed = True
            game_started = True
            time.sleep(7)
            break

def game_did_fail():
    pixel = pag.pixel(game_failed_pos[0], game_failed_pos[1])
    print(pixel)
    print(game_failed)
    if pixel[0] <= game_failed[0]+10 and pixel[0] >= game_failed[0]-10 and pixel[1] <= game_failed[1]+10 and pixel[1] >= game_failed[1]-10 and pixel[2] <= game_failed[2]+10 and pixel[2] >= game_failed[2]-10:
        print("Gotovo")
        return True
    if pixel[0] <= game_failed2[0]+10 and pixel[0] >= game_failed2[0]-10 and pixel[1] <= game_failed2[1]+10 and pixel[1] >= game_failed2[1]-10 and pixel[2] <= game_failed2[2]+10 and pixel[2] >= game_failed2[2]-10:
        print("Gotovo")
        return True
    print("Nije gotovo")
    return False

def toji_spear_on_cooldown():
    color = 72, 43, 255
    x,y = 651, 499
    pixel = pag.pixel(x,y)
    if pixel[0] <= color[0]+2 and pixel[0] >= color[0]-2 and pixel[1] <= color[1]+2 and pixel[1] >= color[1]-2:
        return False
    return True

unit_placed = 96, 222, 91
unit_placed2 = 36, 83, 34
unit_placed_pos = 406, 628

def is_upgrade_really_upgraded():
    region = (392, 383, 425, 412)
    screen = ImageGrab.grab(bbox=region)
    screen.save("test1.png")
    processed_screen = preprocess_image_advanced("test1.png")
    level = pytesseract.image_to_string(processed_screen, lang="eng", config="--psm 7")
    numbers = re.findall(r"\d+", level)
    if not numbers:
        return None
    level = ''.join(numbers)
    return int(level)

def is_unit_really_placed():
    pixel = pag.pixel(unit_placed_pos[0],unit_placed_pos[1])
    print(pag.pixel(unit_placed_pos[0],unit_placed_pos[1]))
    if pixel[0] <= unit_placed[0]+10 and pixel[0] >= unit_placed[0]-10 and pixel[1] <= unit_placed[1]+10 and pixel[1] >= unit_placed[1]-10 or pixel[0] <= unit_placed2[0]+10 and pixel[0] >= unit_placed2[0]-10 and pixel[1] <= unit_placed2[1]+10 and pixel[1] >= unit_placed2[1]-10:
        return True
    return False

global_ability_cd = 190, 190, 190
    
def global_ability():
    pixel = pag.pixel(953, 566)
    if pixel[0] <= global_ability_cd[0]+10 and pixel[0] >= global_ability_cd[0]-10 and pixel[1] <= global_ability_cd[1]+10 and pixel[1] >= global_ability_cd[1]-10:
        return True
    return False

alucard_upgrade = 0
gojo_upgrade = 0
toji_upgrade = 0
sukuna_upgrade = 0
julius_upgrade = 0

alucard_full_aoe_cost2 = 50350

boss_is_out = False
talisman_needed = False
toji_on_spear = False

enabled = False

game_start = True
no_buff = 0
restart = False

game_failed = 222, 136, 22
game_failed2 = 174, 110, 16
game_failed_pos = 1176, 841

while(True):
    if keyboard.is_pressed("p"):
        if enabled:
            enabled = False
            print("disabled")
            game_start = True
            no_buff = 0
            restart = False
            time.sleep(2)
        else:
            enabled = True
            print("enabled")
            time.sleep(2)
    if enabled:
        if game_did_fail() == True:
                    if global_ability() == True:
                        continue
                    game_start = True
                    game_started = False
                    boss_is_out = False
                    talisman_needed = False
                    toji_on_spear = False
                    #unit stanje
                    takorada_upgrade = 0

                    takorada_placed = False
                    alucard_placed = False
                    gojo_placed = False
                    julius_placed = False
                    toji_placed = False
                    sukuna_placed = False

                    #uzete kartice
                    dodge_amount = 0
                    strong_amount = 0
                    press_amount = 0
                    speed_amount = 0
                    alucard_upgrade = 0
                    gojo_upgrade = 0
                    toji_upgrade = 0
                    sukuna_upgrade = 0
                    julius_upgrade = 0

                    mouse_click_at(1176, 821)
                    time.sleep(0.1)
                    continue
        if restart:
            restart_game()
            restart = False
            game_start = True
            no_buff = 0
        if game_start:
            if choose_buff() is False:
                no_buff += 1
                time.sleep(3)
            else:
                mouse_click_at(886, 199)
                game_start = False
                no_buff = 0
            if no_buff == 5:
                restart = True
        else:
            if game_started:
                if game_did_fail() == True:
                    if global_ability() == True:
                        continue
                    game_start = True
                    game_started = False
                    boss_is_out = False
                    talisman_needed = False
                    toji_on_spear = False
                    #unit stanje
                    takorada_upgrade = 0

                    takorada_placed = False
                    alucard_placed = False
                    gojo_placed = False
                    julius_placed = False
                    toji_placed = False
                    sukuna_placed = False

                    #uzete kartice
                    dodge_amount = 0
                    strong_amount = 0
                    press_amount = 0
                    speed_amount = 0
                    alucard_upgrade = 0
                    gojo_upgrade = 0
                    toji_upgrade = 0
                    sukuna_upgrade = 0
                    julius_upgrade = 0

                    uradeni_stage += 1
                    send_to_discord(screenshot())

                    mouse_click_at(1176, 821)
                    time.sleep(0.1)
                    continue
                if choose_card() == True:
                    time.sleep(1.5)
                    continue
                if boss_spawned() == 0 and boss_is_out == False:
                    boss_is_out = True
                    print("Normalan boss")
                if boss_spawned() == 1 and boss_is_out == False:
                    boss_is_out = True
                    print("Shield boss")
                if boss_spawned() == 2 and boss_is_out == False:
                    print("Talisman boss")
                    boss_is_out = True
                    talisman_needed = True
                if boss_spawned() == -1 and boss_is_out == True:
                    print("Prosao boss")
                    boss_is_out = False
                if boss_is_out == True and toji_upgrade >= 11 and toji_on_spear == False:
                    mouse_click_at(toji1[0],toji1[1])
                    time.sleep(0.7)
                    if is_unit_really_placed() == True:
                        if toji_spear_on_cooldown() == False:
                            mouse_click_at(630, 499)
                            toji_on_spear = True
                            continue
                if boss_is_out == False and toji_upgrade >= 11 and toji_on_spear == True:
                    mouse_click_at(toji1[0],toji1[1])
                    time.sleep(0.7)
                    if is_unit_really_placed() == True:
                        if toji_spear_on_cooldown() == False:
                            mouse_click_at(630, 499)
                            toji_on_spear = False
                            continue
                if talisman_needed == True:
                    mouse_click_at(1395, 922)
                    time.sleep(0.2)
                    talisman_needed = False

                time.sleep(1)
                money = current_money()
                if money is None:  
                    continue
                if money > 2000 and alucard_placed == False:
                    place_unit(alucard, 1)
                    time.sleep(0.7)
                    if is_unit_really_placed() == False:
                        continue
                    print("Unit placed o correctly")
                    mouse_click_at(1791, 935)
                    alucard_placed = True
                    money = 0
                    time.sleep(1)
                    continue
                if money > 1800 and alucard_placed == True and gojo_placed == False:
                    place_unit(gojo, 2)
                    time.sleep(0.7)
                    if is_unit_really_placed() == False:
                        continue
                    print("Unit placed o correctly")
                    mouse_click_at(1791, 935)
                    gojo_placed = True
                    money = 0
                    time.sleep(1)
                    continue
                if money > 1600 and gojo_placed == True and julius_placed == False:
                    place_unit(julius, 3)
                    time.sleep(0.7)
                    if is_unit_really_placed() == False:
                        continue
                    print("Unit placed o correctly")
                    mouse_click_at(1791, 935)
                    julius_placed = True
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3000 and julius_placed == True and takorada_upgrade == 1:
                    upgraded = upgrade_unit(takorada)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    takorada_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 4500 and julius_placed == True and takorada_upgrade == 2:
                    upgraded = upgrade_unit(takorada)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    takorada_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7500 and julius_placed == True and takorada_upgrade == 3:
                    upgraded = upgrade_unit(takorada)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    takorada_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 1425 and takorada_upgrade == 4 and alucard_upgrade == 0:
                    upgraded = upgrade_unit(alucard)
                    time.sleep(0.2)
                    if upgraded == False:
                        mouse_click_at(1791, 935)
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 2850 and takorada_upgrade == 4 and alucard_upgrade == 1:
                    upgraded = upgrade_unit(alucard)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3800 and takorada_upgrade == 4 and alucard_upgrade == 2:
                    upgraded = upgrade_unit(alucard)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 4750 and takorada_upgrade == 4 and alucard_upgrade == 3:
                    upgraded = upgrade_unit(alucard)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    sell_unit(sukuna1)
                    sukuna_placed = False
                    money = 0
                    time.sleep(1)
                    continue
                if money > 2000 and sukuna_placed == False:
                    place_unit(sukuna2, 6)
                    time.sleep(0.7)
                    if is_unit_really_placed() == False:
                        continue
                    print("Unit placed o correctly")
                    mouse_click_at(1791, 935)
                    sukuna_placed = True
                    money = 0
                    time.sleep(1)
                    continue
                if money > 10000 and takorada_upgrade == 4:
                    upgraded = upgrade_unit(takorada)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    takorada_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 12500 and takorada_upgrade == 5:
                    upgraded = upgrade_unit(takorada)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    takorada_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7125 and alucard_upgrade == 4:
                    upgraded = upgrade_unit(alucard)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7600 and alucard_upgrade == 5:
                    upgraded = upgrade_unit(alucard)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > alucard_full_aoe_cost2 and alucard_upgrade >= 6 and alucard_upgrade < 10:
                    if alucard_upgrade == 6:
                        upgraded = upgrade_unit(alucard)
                        time.sleep(0.2)
                        if upgraded == False:
                            mouse_click_at(1791, 935)
                            continue
                        alucard_full_aoe_cost2 -= 9500
                        alucard_upgrade+=1
                    if alucard_upgrade == 7:
                        upgraded = upgrade_unit(alucard)
                        time.sleep(0.2)
                        if upgraded == False:
                            mouse_click_at(1791, 935)
                            continue
                        alucard_full_aoe_cost2 -= 11875
                        alucard_upgrade+=1
                    if alucard_upgrade == 8:    
                        upgraded = upgrade_unit(alucard)
                        time.sleep(0.2)
                        if upgraded == False:
                            mouse_click_at(1791, 935)
                            continue
                        alucard_full_aoe_cost2 -= 13300
                        alucard_upgrade+=1
                    if alucard_upgrade == 9:
                        upgraded = upgrade_unit(alucard)
                        time.sleep(0.2)
                        mouse_click_at(1791, 935)
                        if upgraded == False:
                            continue
                        alucard_full_aoe_cost2 -= 15675
                        alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                        
                if money > 19000 and alucard_upgrade == 10:
                    upgraded = upgrade_unit(alucard)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    alucard_upgrade += 1
                    money = 0
                    time.sleep(1)
                    auto_ability(alucard)
                    continue
                if money > 2500 and alucard_upgrade == 11 and gojo_upgrade == 0:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3400 and alucard_upgrade == 11 and gojo_upgrade == 1:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 5000 and alucard_upgrade == 11 and gojo_upgrade == 2:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 6500 and alucard_upgrade == 11 and gojo_upgrade == 3:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7400 and alucard_upgrade == 11 and gojo_upgrade == 4:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 9000 and alucard_upgrade == 11 and gojo_upgrade == 5:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 9900 and alucard_upgrade == 11 and gojo_upgrade == 6:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 12000 and alucard_upgrade == 11 and gojo_upgrade == 7:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    auto_ability(gojo)
                    continue
                if money > 15000 and alucard_upgrade == 11 and gojo_upgrade == 8:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 17700 and alucard_upgrade == 11 and gojo_upgrade == 9:
                    upgraded = upgrade_unit(gojo)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    gojo_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 2500 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 0:
                    upgraded = upgrade_unit(toji1)

                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3550 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 1:
                    upgraded = upgrade_unit(toji1)
                    mouse_click_at(84, 667)
                    time.sleep(0.2)
                    mouse_click_at(88, 787)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 4750 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 2:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 5100 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 3:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 6000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 4:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 6800 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 5:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7300 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 6:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 8400 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 7:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 9250 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 8:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 11000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 9:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 11500 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 10:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 13500 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 11:
                    upgraded = upgrade_unit(toji1)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    toji_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3100 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 0:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 4000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 1:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 5100 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 2:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 6400 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 3:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7300 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 4:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 8000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 5:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 9200 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 6:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 10400 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 7:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    auto_ability(sukuna2)
                    continue
                if money > 13000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 8:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 14200 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 9:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 15500 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 10:
                    upgraded = upgrade_unit(sukuna2)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    sukuna_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 2300 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 0:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 3500 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 1:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 4400 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 2:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 6600 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 3:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 7350 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 4:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 8850 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 5:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 10600 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 6:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 11800 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 7:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 13400 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 8:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                if money > 15000 and alucard_upgrade == 11 and gojo_upgrade == 10 and toji_upgrade == 12 and sukuna_upgrade == 11 and julius_upgrade == 9:
                    upgraded = upgrade_unit(julius)
                    time.sleep(0.2)
                    mouse_click_at(1791, 935)
                    if upgraded == False:
                        continue
                    julius_upgrade += 1
                    money = 0
                    time.sleep(1)
                    continue
                mouse_click_at(1791, 935)
                time.sleep(0.7)
            else:
                init_game()
        