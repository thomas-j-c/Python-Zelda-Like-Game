WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HBOXOFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'nonVis': 0
}

FONT = '../res/font/joystix.ttf'
FONTSIZE = 18
FONTCOLOUR = '#EEEEEE'
BARHEIGHT = 20
BARWIDTH = 200
BOXSIZE = 80

WATERCOLOUR = '#71ddee'
UIBGCOLOUR = '#222222'
UIBORDERCOLOUR = '#111111'


UPGRADETEXTCOLOUR = '#111111'
BARCOLOUR = '#EEEEEE'
BARCOLOURSELECTED = '#111111'
UPGRADECOLOURSELECTED = '#111111'
UPGRADEBGCOLOURSELECTED = '#EEEEEE'

HEALTHCOLOUR = 'red'
ENERGYCOLOUR = 'green'
ACTIVEUICOLOUR = 'gold'

weapons = {
    'sword': {'cd': 100, 'dmg': 15, 'img': '../res/weapons/sword/full.png'},
    'lance': {'cd': 400, 'dmg': 50, 'img': '../res/weapons/lance/full.png'},
    'axe': {'cd': 250, 'dmg': 25, 'img': '../res/weapons/axe/full.png'},
    'rapier': {'cd': 50, 'dmg': 7, 'img': '../res/weapons/rapier/full.png'},
    'sai': {'cd': 80, 'dmg': 10, 'img': '../res/weapons/sai/full.png'},
}

magic = {
    'flame': {'strength': 5, 'cost': 20, 'img': '../res/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'img': '../res/particles/heal/heal.png'}
}


enemies = {
    'squid': {'health': 100, 'exp': 100, 'dmg': 20, 'attackType': 'slash', 'attackSound': '../audio/attack/slash.wav',
              'speed': 3, 'res': 9, 'attackRad': 80, 'noticeRad': 360},

    'raccoon': {'health': 250, 'exp': 175, 'dmg': 50, 'attackType': 'claw', 'attackSound': '../audio/attack/claw.wav',
                'speed': 5, 'res': 2, 'attackRad': 100, 'noticeRad': 400},

    'spirit': {'health': 300, 'exp': 150, 'dmg': 30, 'attackType': 'thunder',
               'attackSound': '../audio/attack/fireball.wav', 'speed': 9, 'res': 6, 'attackRad': 50, 'noticeRad': 200},

    'bamboo': {'health': 50, 'exp': 75, 'dmg': 10, 'attackType': 'leafAttack',
               'attackSound': '../audio/attack/slash.wav', 'speed': 1, 'res': 5, 'attackRad': 50, 'noticeRad': 500}
}
