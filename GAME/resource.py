from os.path import split, abspath
from pyglet.image import load
path = split(abspath(__file__))[0] + '\\' + 'resource'
bgBackup1 = path + '\\' + 'bg.png'
bgBackup2 = path + '\\' + 'bg1.png'

flying_squirrel = load(path + '\\' + 'flying_squirrel.png')
flying_squirrel_flying = load(path + '\\' + 'flying_squirrel_flying.png')
bg = load(path + '\\' + 'bg2.png')
volume = load(path + '\\' + 'volume.png')
block = load(path + '\\' + 'block.png')
nut = load(path + '\\' + 'nut.png')
peanut = load(path + '\\' + 'peanut.png')

bgm = path + '\\' + 'bgm.mp3'
bgm2 = path + '\\' + 'bgm2.mp3'

rush = path + '\\' + 'rush.wav'
die = path + '\\' + 'die.wav'
jump = path + '\\' + 'jump.wav'