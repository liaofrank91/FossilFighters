import pygame
import database
from random import randint

'''
current issues: 
- show: Vivosaur Names, VIVOSAUR HEALTH AND HEALTHBAR (place health in blue portion)
- maybe I should also display the damage for the attacks and not just the FP? 
- HAVE A 'FEED' OF SORTS: showing most recent actions (i.e. Spinax did x damage to Carchar)
- image paths! (when upload)
- EZ TO IMPLEMENT: TITLE SCREEN WELCOME TO FOSSIL FIGHTERS SLAP A T-REX SPRITE LOGO OR SMTH ON THERE
- EZ TO IMPLEMENT AND MORE IMPORTANT!! ENDING SCREEN SAYING WHO WON! and maybe click space to restart or smth
- A BIT MORE TEDIOUS TO IMPLEMENT: during selection screen, cycle through all the available vivosaurs with the help of a
- ... timer. Show the SPRITE and NAME 
- ADD AN END TURN BUTTON IF IM GOING TO ALLOW MORE THAN ONE ATTACK PER TURN

'''

vivosaur_database = database.vivosaur_database

class Vivosaur(pygame.sprite.Sprite):
    def __init__(self, name, element, health, attack, defense, accuracy, speed, attack_info, vivosaur_index, team,
                 original_health):
        # vivosaur index is for rect placement
        super().__init__()
        self.name = name
        self.element = element
        self.health = health
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.speed = speed
        self.attack_info = attack_info
        self.vivosaur_index = vivosaur_index
        self.team = team
        self.original_health = original_health

        self.image = pygame.image.load(
            f'C:\\Users\\liaof\\PycharmProjects\\fossil_fighters_1.5\\vivosaur images\\{self.name.lower()}_image.png')

        if self.team == 1:
            if self.vivosaur_index == 0:
                self.rect = self.image.get_rect(center=(300, 200))
            if self.vivosaur_index == 1:
                self.rect = self.image.get_rect(center=(150, 120))
            if self.vivosaur_index == 2:
                self.rect = self.image.get_rect(center=(150, 280))
        if self.team == 2:
            self.image = pygame.transform.flip(self.image, True, False)
            if self.vivosaur_index == 0:
                self.rect = self.image.get_rect(center=(500, 200))
            if self.vivosaur_index == 1:
                self.rect = self.image.get_rect(center=(650, 120))
            if self.vivosaur_index == 2:
                self.rect = self.image.get_rect(center=(650, 280))

class Attack(pygame.sprite.Sprite):
    def __init__(self, vivosaur, index, turn):
        super().__init__()
        self.image = font.render(f'{vivosaur.attack_info[index][0]}: {vivosaur.attack_info[index][2]} FP', False,
                                 (64, 64, 64))
        if turn == 0:
            x = 600
        else:
            x = 200
        if index == 0:
            y = 50
            colour = ()
        if index == 1:
            y = 100
        if index == 2:
            y = 150
        if index == 3:
            y = 200
        if index == 4:
            y = 250
        self.rect = self.image.get_rect(center=(x, y))

def create_vivosaur(vivosaur_index, vivosaur_name):
    name = vivosaur_name.capitalize()

    stats = vivosaur_database[name][:6]
    health = stats[0]
    element = stats[1]
    attack = stats[2]
    defense = stats[3]
    accuracy = stats[4]
    speed = stats[5]
    team = 0
    if vivosaur_index <= 2:
        vivosaur_index = vivosaur_index  # vivosaur_index is for rect placement (which of the 3 positions)
        team = 1  # team is for rect placement (left or right)
    if vivosaur_index >= 3:
        vivosaur_index = vivosaur_index - 3
        team = 2
    attack_info = vivosaur_database[name][6]  # attack_info is a list with lists inside it
    original_health = health  # basically just making an extra copy of health that is not affected by dmg

    return Vivosaur(name, element, health, attack, defense, accuracy, speed, attack_info, vivosaur_index, team,
                    original_health)

def layout(team1, team2):
    print("STATUS UPDATE")
    print("")
    print("")
    print("------------------------------")
    print("Player 1 Team!")
    for vivosaur in team1:  # printing all team1 vivosaurs
        print(vivosaur.name + ": " + str(vivosaur.health))
    print("------------------------------")
    print("")
    print("------------------------------")
    print("Player 2 Team!")
    for vivosaur in team2:
        print(vivosaur.name + ": " + str(vivosaur.health))
    print("------------------------------")

def who_goes_first(team1, team2):
    from random import randint

    total_lp_1 = 0
    total_lp_2 = 0

    for vivosaur in team1:
        total_lp_1 += vivosaur.health

    for vivosaur in team2:
        total_lp_2 += vivosaur.health

    if total_lp_1 < total_lp_2:
        return 0
    elif total_lp_2 < total_lp_1:
        return 1
    elif total_lp_1 == total_lp_2:
        random = randint(0, 1)
        print(
            "Both teams have the same total LP. The person who goes first will be decided randomly")  # test this later
        return random

def check_attack_fp(team, vivosaur_index, attack_index, player_fp):
    print(f'FP COST: {team[vivosaur_index].attack_info[attack_index][2]}')  # temporary: for troubleshooting purposes

    if team[vivosaur_index].attack_info[attack_index][2] <= player_fp:
        return True
    elif team[vivosaur_index].attack_info[attack_index][2] > player_fp:
        print("Sorry the cost of that attack is too high - please choose another")
        return False

def calc_damage(attacker_team, defender_team, attacker_index, attack_index, defender_index):
    # check for: elemental damage (1.5x, 0.75x)

    dmg_mult = 1

    att_element = attacker_team[attacker_index].element
    def_element = defender_team[defender_index].element

    if (att_element == 'air' and def_element == 'water') or (att_element == 'water' and def_element == 'fire') or (
            att_element == 'fire' and def_element == 'earth') or (att_element == 'earth' and def_element == 'air'):
        dmg_mult = 1.5
    elif (att_element == 'water' and def_element == 'air') or (att_element == 'fire' and def_element == 'water') or (
            att_element == 'earth' and def_element == 'fire') or (att_element == 'air' and def_element == 'earth'):
        dmg_mult = 0.85

    # attacking from az or sz (1.2x or 0.75x)

    zone_multiplier = 0  ##### note this - could help troubleshoot, if dmg output is 0 then problem is with below if/else

    if attacker_index == 0 and defender_index == 0:
        zone_multiplier = 1.75
    else:
        zone_multiplier = 1

    # attack and defense stats

    net_attack = (attacker_team[attacker_index].attack - defender_team[defender_index].defense) / 100

    # putting it all together - calculating damage

    total_damage = attacker_team[attacker_index].attack_info[attack_index][1] * zone_multiplier * net_attack * dmg_mult
    print(f"{attacker_team[attacker_index].name} did {total_damage} damage to {defender_team[defender_index].name}!!")

    if dmg_mult == 1.5:
        print(f"It was a critical hit! {att_element} to {def_element} ")
    elif dmg_mult == 0.85:
        print(f"It wasn't very effective... {att_element} to {def_element}")

    defender_team[defender_index].health -= total_damage

    return defender_team[defender_index].health

def subtract_fp(attacker_team, vivosaur_index, attack_index, player_fp):  # player indicates player 1 or player 2
    player_fp -= attacker_team[vivosaur_index].attack_info[attack_index][2]
    return player_fp

def update_teams(team1, team2):  # hmm maybe should just use 'team' and then call update_teams two times lmao
    for vivosaur in team1:
        if vivosaur.health <= 0:
            team1.remove(vivosaur)
            vivosaur.kill()

    for vivosaur in team2:
        if vivosaur.health <= 0:
            team2.remove(vivosaur)
            vivosaur.kill()

def update_rects(group1, group2):  # same suggestion as above ^ for update_teams
    index = -1
    for vivosaur in group1:
        index += 1
        if index == 0:
            vivosaur.rect = vivosaur.image.get_rect(center=(300, 200))
        if index == 1:
            vivosaur.rect = vivosaur.image.get_rect(center=(150, 120))
        if index == 2:
            vivosaur.rect = vivosaur.image.get_rect(center=(150, 280))
    index = -1
    for vivosaur in group2:
        index += 1
        if index == 0:
            vivosaur.rect = vivosaur.image.get_rect(center=(500, 200))
        if index == 1:
            vivosaur.rect = vivosaur.image.get_rect(center=(650, 120))
        if index == 2:
            vivosaur.rect = vivosaur.image.get_rect(center=(650, 280))

def check_win(p1_team, p2_team):
    pass

def display_base():
    screen.fill((79, 93, 117))
    # screen.blit(stadium, (0, 0))
    screen.blit(background, (0, 0))

    group1.draw(screen)
    group1.update()

    group2.draw(screen)
    group2.update()

    # full rectangle is 100 length

    if len(p1_team) >= 1:
        # TEAM 1 RECT 1
        health_percent = p1_team[0].health / p1_team[0].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(250, 235, 100, 20)) # BLUE
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(250 + blue_portion, 235, (200 - (100 + blue_portion)), 20))

    if len(p1_team) >= 2:
        # TEAM 1 RECT 2
        health_percent = p1_team[1].health / p1_team[1].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(100, 155, 100, 20))
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(100 + blue_portion, 155, (200 - (100 + blue_portion)),
                                                            20))  # health bar = red rect + green rect

    if len(p1_team) == 3:
        # TEAM 1 RECT 3
        health_percent = p1_team[2].health / p1_team[2].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(100, 315, 100, 20))
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(100 + blue_portion, 315, (200 - (100 + blue_portion)), 20))

    if len(p2_team) >= 1:
        # TEAM 2 RECT 1
        health_percent = p2_team[0].health / p2_team[0].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(450, 235, 100, 20))  # RED
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(450, 235, blue_portion, 20)) # BLUE

    if len(p2_team) >= 2:
        # TEAM 2 RECT 2
        health_percent = p2_team[1].health / p2_team[1].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(600, 155, 100, 20))
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(600, 155, blue_portion, 20))

    if len(p2_team) == 3:
        # TEAM 2 RECT 3
        health_percent = p2_team[2].health / p2_team[2].original_health
        blue_portion = 100 * health_percent
        pygame.draw.rect(screen, (152, 38, 73), pygame.Rect(600, 315, 100, 20))
        pygame.draw.rect(screen, (93, 183, 222), pygame.Rect(600, 315, blue_portion, 20))

def create_attacks(vivosaur, turn):
    attack_group = pygame.sprite.Group()

    for x in range(0, 5):
        attack_group.add(Attack(vivosaur, x, turn))
    return attack_group

def display_attacks(attack_group):
    colour = (251, 159, 137)
    counter = 0
    for attack in attack_group:  # displaying the appropriate colour rectangles
        if counter == 3:
            colour = (33, 161, 121)
        if counter == 4:
            colour = (255, 77, 128)
        pygame.draw.rect(screen, colour, attack.rect)
        counter += 1

    attack_group.draw(screen)  # then displaying the actual sprites that the user interacts with

def display_targets(index, turn, defending_group):
    if turn == 0:
        x1 = 500
        x2 = 650
    else:
        x1 = 300
        x2 = 150
    target1 = target_symbol
    target1_rect = target1.get_rect(center=(x1, 200))
    target2 = target_symbol
    target2_rect = target2.get_rect(center=(x2, 120))
    target3 = target_symbol
    target3_rect = target3.get_rect(center=(x2, 280))

    target_list = [target1, target2, target3]
    target_rect_list = [target1_rect, target2_rect, target3_rect]

    counter = 0
    for vivosaur in defending_group:
        print(vivosaur.name)
        counter += 1
        print(counter)

    target_list = target_list[:counter]
    target_rect_list = target_rect_list[:counter]
    print(target_list)
    print(target_rect_list)

    if index == 0:
        for i in range(counter):
            screen.blit(target_list[i], target_rect_list[i])
            print('hello')
    else:
        screen.blit(target_list[0], target_rect_list[0])
        # target_rect_list = [target_rect_list[0]]

    return target_rect_list

pygame.init()
font = pygame.font.Font(r'fonts\amatic font\AmaticSC-Regular.ttf', 40)

p1_team = []
p2_team = []

group1 = pygame.sprite.Group()
group2 = pygame.sprite.Group()

pygame.display.set_caption('Fossil Fighters')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# stadium = pygame.image.load(r'misc images\ZongaZonga_Castle.png')
# stadium = pygame.transform.scale(stadium, (800, 400))

background = pygame.image.load(r'misc images\blue_pixels.jpeg')

target_symbol = pygame.image.load(r'misc images\red target.png')
target_symbol = pygame.transform.scale(target_symbol, (80, 80))
# target_symbol_rect = target_symbol.get_rect(center=())
target1_rect = pygame.image.load(r'misc images\red target.png').get_rect(center=(0, 0))  # any picture
target2_rect = target1_rect
target3_rect = target1_rect

# DISPLAY CONTROLLERS
battle = False
base_layout = True
show_attacks = False
show_targets = False
execute_attack = False

p1_fp = 0
p2_fp = 0

attack_rect_list = []
attacker_index = 0
attack_index = 0
defender_index = 0
target_list = []
user_text = ''
vivosaur_creation_index = 0

# TIMERS
test_timer = pygame.USEREVENT + 1
pygame.time.set_timer(test_timer, 1500)

# GAME
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == test_timer:
            pass
        if battle:
            if event.type == pygame.MOUSEBUTTONUP and show_attacks == False and show_targets == True:
                print('hello3')
                pos = pygame.mouse.get_pos()
                defender_index = 0
                for target in target_list:  # target_list is a list of rects
                    if target.collidepoint(pos):
                        execute_attack = True
                        break
                    else:
                        print('nope')
                        defender_index += 1
                print(f'{defender_index} is the defender index')

            if event.type == pygame.MOUSEBUTTONUP and show_attacks == False and show_targets == False:
                print('hello')
                pos = pygame.mouse.get_pos()
                show_attacks = False  # this WAS causing the problem before
                attacker_index = -1
                if turn == 0:
                    for sprite in group1:
                        attacker_index += 1
                        if sprite.rect.collidepoint(pos):
                            vivo_sprite = sprite
                            show_attacks = True
                            break
                else:
                    for sprite in group2:
                        attacker_index += 1
                        if sprite.rect.collidepoint(pos):
                            vivo_sprite = sprite
                            show_attacks = True
                            break

            if event.type == pygame.MOUSEBUTTONUP and show_attacks == True and show_targets == False:
                print('hello2')
                pos = pygame.mouse.get_pos()
                # print(pos)

                attack_group = create_attacks(vivo_sprite, turn)

                attack_index = 0
                for attack in attack_group:
                    print('working too')
                    if attack.rect.collidepoint(pos):
                        # attacks have been made into sprite object type
                        attack_sprite = attack
                        if turn == 0:
                            player_team = p1_team
                            player_fp = p1_fp
                            print(f'Original Player FP: {p1_fp}')
                        else:
                            player_team = p2_team
                            player_fp = p2_fp
                            print(f'Original Player FP: {p2_fp}')
                        bool = check_attack_fp(player_team, attacker_index, attack_index, player_fp)
                        if bool == True:
                            if turn == 0:
                                p1_fp = subtract_fp(player_team, attacker_index, attack_index,
                                                    player_fp)  # need to subtract from p1 or p2_fp directly, not player_fp
                                print(f"Updated Player FP: {p1_fp}")
                            else:
                                p2_fp = subtract_fp(player_team, attacker_index, attack_index, player_fp)
                                print(f'Updated Player FP: {p2_fp}')
                            show_targets = True
                            show_attacks = False
                            print(show_targets)
                            break
                    attack_index += 1
        if not battle:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        vivo = create_vivosaur(vivosaur_creation_index, user_text)
                        if vivosaur_creation_index <= 2:
                            p1_team.append(vivo)
                            group1.add(vivo)
                        else:
                            p2_team.append(vivo)
                            group2.add(vivo)
                    except:
                        user_text = ''
                        break
                    user_text = ''
                    vivosaur_creation_index += 1
                    if vivosaur_creation_index == 6:  # ( after adding 1 )
                        battle = True
                        turn = who_goes_first(p1_team, p2_team)
                        if turn == 0:
                            p1_fp += 180
                        else:
                            p2_fp += 180
                else:
                    user_text += event.unicode

    if not battle:
        screen.fill((0, 0, 0))

        text_surface = font.render(user_text, True, (255, 255, 255))
        input_rect = pygame.Rect(50,50,150,50)
        input_rect.w = max((text_surface.get_width() + 10), 100)

        text_rect_colour = pygame.Color('lightskyblue3')

        pygame.draw.rect(screen,text_rect_colour,input_rect,3)
        screen.blit(text_surface,(input_rect.x + 5, input_rect.y - 1))

        if vivosaur_creation_index == 0:
            instruction_surface = font.render("Player 1, enter your FIRST vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))
        if vivosaur_creation_index == 1:
            instruction_surface = font.render("Player 1, enter your SECOND vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))
        if vivosaur_creation_index == 2:
            instruction_surface = font.render("Player 1, enter your THIRD vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))
        if vivosaur_creation_index == 3:
            instruction_surface = font.render("Player 2, enter your FIRST vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))
        if vivosaur_creation_index == 4:
            instruction_surface = font.render("Player 2 enter your SECOND vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))
        if vivosaur_creation_index == 5:
            instruction_surface = font.render("Player 2, enter your THIRD vivosaur", True, (255, 255, 255))
            screen.blit(instruction_surface, (400, 200))

    if battle:

        if turn == 0:
            attacker_team = p1_team
            defender_team = p2_team
        else:
            attacker_team = p2_team
            defender_team = p1_team

        if base_layout == True and show_attacks == False and show_targets == False and execute_attack == False:
            display_base()
        if show_attacks == True and show_targets == False and execute_attack == False:
            display_base()
            display_attacks(attack_group)  # WORK ON THIS PART NEXT -->
        if show_targets == True and execute_attack == False:
            display_base()
            if turn == 0:
                defending_group = group2
            else:
                defending_group = group1
            target_list = display_targets(attacker_index, turn, defending_group)
        if execute_attack == True:
            defender_team[defender_index].health = calc_damage(attacker_team, defender_team, attacker_index,
                                                               attack_index, defender_index)
            print(defender_team[defender_index].health)
            update_teams(p1_team, p2_team)
            update_rects(group1, group2)  # new addition
            # if turn == 0:
            #     defending_group = group2
            # else:
            #     defending_group = group1
            #
            # target_list = update_target_list(target_list,defending_group)

            if turn == 0:
                p2_fp += 180
                turn = 1  # adding this: remove/modify if problems arise
            else:
                turn = 0
                p1_fp += 180

            base_layout = True
            show_attacks = False
            show_targets = False
            execute_attack = False

        team1_surf = font.render("TEAM 1", False, (255, 255, 255))
        team1_rect = team1_surf.get_rect(center = (50, 50))
        pygame.draw.rect(screen, (18, 94, 138), team1_rect)
        screen.blit(team1_surf, team1_rect)

        team2_surf = font.render("TEAM 2", False, (255, 255, 255))
        team2_rect = team2_surf.get_rect(center = (750, 50))
        pygame.draw.rect(screen, (18, 94, 138), team2_rect)
        screen.blit(team2_surf, team2_rect)

        turn_surf = font.render(f"Player {turn + 1}'s Turn", False, (255, 255, 255))
        turn_rect = turn_surf.get_rect(center=(400, 50))
        pygame.draw.rect(screen, (18, 94, 138), turn_rect)
        screen.blit(turn_surf, turn_rect)

        fp1_surf = font.render(f"FP: {p1_fp}", False, (255, 255, 255))
        fp1_rect = fp1_surf.get_rect(center=(200, 370))
        pygame.draw.rect(screen, (18, 94, 138), fp1_rect)
        screen.blit(fp1_surf, fp1_rect)

        fp2_surf = font.render(f"FP: {p2_fp}", False, (255, 255, 255))
        fp2_rect = fp2_surf.get_rect(center=(600, 370))
        pygame.draw.rect(screen, (18, 94, 138), fp2_rect)
        screen.blit(fp2_surf, fp2_rect)

    pygame.display.update()
    clock.tick(60)
