'''
vivosaur database module
'''

vivosaur_database = {
    # when calling an attack, first check if it's a team attack by checking if there is a True boolean in...
    "Spinax": [480, 'air', 72, 36, 48, 20, [["Spinax Fang", 84, 50, ['no_effect', 'n/a'], False],
                                            ["Spinax Combo", 117, 150, ['no_effect', 'n/a'], False],
                                            ["Cyclone", 127, 220, ['no_effect', 'n/a'], False],
                                            ["Harden", 0, 50, ['raise_def', 1], False],
                                            ["Cyclonic Breath", 132, 260, ['az_and_sz', 1], True]]],
    ## [Dmg, Fp, ~any special effects~]
    "Carchar": [540, 'earth', 88, 41, 45, 11, [["Massive Jaws", 108, 70, ['no_effect', 'n/a'], False],
                                               ["Carchar Combo", 128, 140, ['no_effect', 'n/a'], False],
                                               ["Carchar Fury", 168, 280, ['rotate', 0.8], False],
                                               ["Law of the Jungle", 0, 200, ['jungle', 1], False],
                                               ["Earthen Blast", 150, 270, ['az_and_sz', 1], True]]],
    "Venator": [480, 'earth', 72, 36, 48, 24, [["Venator Bite", 86, 60, ['no_effect', 'n/a'], False],
                                               ["Venator Combo", 117, 160, ['no_effect', 'n/a'], False],
                                               ["Venator Fury", 147, 270, ['excite', 0.5], False],
                                               ["Quicken", 0, 50, ['raise_eva', 1], False],
                                               ["Sand Storm", 134, 270, ['az_and_sz', 1], True]]],
    "Tricera": [500, 'water', 72, 36, 45, 21, [["Running Smash", 87, 50, ['no_effect', 'n/a'], False],
                                               ["Tricera Combo", 124, 180, ['knock_to_ez', 0.8], False],
                                               ["Triple Threat", 159, 300, ['enrage', 0.8], False],
                                               ["Enflame", 0, 50, ['raise_att', 1], False],
                                               ["Tri-Torpedo", 112, 170, ['az_and_sz', 1], True]]],
    # tricera has a 'knock to az' effect, but ez not implemented yet
    "Allo": [580, 'neutral', 88, 45, 48, 18,
             [["Allo Bite", 106, 70, ['no_effect', 'n/a'], False], ["Allo Combo", 126, 150, ['excite', 0.3], False],
              ["Allo Fury", 185, 300, ['super_excite', 1], False], ["Law of the Jungle", 0, 200, ['jungle', 1], False],
              ["Void Blast", 153, 280, ['az_and_sz', 1], True]]],
    "Amargo": [500, 'fire', 62, 27, 48, 21,
               [["Amargo Stomp", 78, 60, ['no_effect', 'n/a'], False], ["Amargo Combo", 93, 120, ['scare', 0.4], False],
                ["Blazing Doom", 114, 180, ['no_effect', 'n/a'], False],
                ["Power Scale", 0, 50, ['equalize_fp', 1], False], ["Fire Cannon", 115, 230, ['az_and_sz', 1], True]]],
}