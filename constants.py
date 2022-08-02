import asyncio
import random
from datetime import datetime
import pytz
from config import db_object, db_connection
import math

lvl_dict = {
    1: 525, 2: 1235, 3: 2021, 4: 3403, 5: 5002, 6: 7138, 7: 10053, 8: 13804, 9: 18512,
    10: 24297, 11: 31516, 12: 39878, 13: 50352, 14: 62261, 15: 76465, 16: 92806, 17: 112027, 18:
        133876, 19: 158538, 20: 187025, 21: 218895, 22: 255366, 23: 295852, 24: 341805, 25:
        392470, 26: 449555, 27: 512121, 28: 583857, 29: 662181, 30: 747411, 31: 844146, 32:
        949053, 33: 1064952, 34: 1192712, 35: 1333241, 36: 1487491, 37: 1656447, 38: 1841143, 39:
        2046202, 40: 2265837, 41: 2508528, 42: 2776124, 43: 3061734, 44: 3379914, 45: 3723676,
    46: 4099570, 47: 4504444, 48: 4951099, 49: 5430907, 50: 5957868, 51: 6528910, 52: 7153414, 53:
        7827968, 54: 8555414, 55: 9353933, 56: 10212541, 57: 11142646, 58: 12157041, 59: 13252160, 60:
        14441758, 61: 15731508, 62: 17127265, 63: 18635053, 64: 20271765, 65: 22044909, 66: 23950783, 67: 26019833,
    68: 28261412, 69: 30672515, 70: 33287878, 71: 36118904, 72: 39163425, 73: 42460810, 74: 46024718, 75: 49853964,
    76: 54008554, 77: 58473753, 78: 63314495, 79: 68516464, 80: 74132190, 81: 80182477, 82: 86725730, 83: 93748717,
    84: 101352108, 85: 109524907, 86: 118335069, 87: 127813148, 88: 138033822, 89: 149032822, 90: 160890604,
    91: 173648795, 92: 187372170, 93: 202153736, 94: 218041909, 95: 235163399, 96: 253547862, 97: 273358532,
    98: 294631836, 99: 317515914
}

rank_dict = {
    0: 0,
    1: 25,
    2: 5000,
    3: 10000,
    4: 20000,
    5: 30000
}

primogems_wish_outcome = {
    3: [
        'free watch of youtube for 1 hour', '1 episode of anime', '2 episode of anime/show',
        '1game/30 minutes of game time', 'discord/free 40 minutes', '2game/60 minutes of game time',
        'free watch of youtube for 30 minutes'
    ],
    4: [
        'watch a film', '4 episode of anime', '3 games / 2hour of games', 'free watch of youtube for 2 hour',
        'discord/free 90 minutes', '2 episode of show', 'small walk/ rpg development'
    ],
    5: [
        'whole day off!', '3 charges of going out\ rpg development'
    ]
}

areas_dict = {
    1: 'desert',
    2: 'test1',
    3: 'test2',
    4: 'test3'
}

mobs_dict = {'Abandoned Teddy Bear.jpg': 'abyss', 'Abysmal Knight.jpg': 'abyss', 'Agav.jpg': 'save for later'
    ,'Agony Of Royal Knight.jpg': 'shadow isles', 'Airship Raid.jpg': 'desert', 'Alarm.jpg':
                 'save for later', 'Alice.jpg': 'save for later', 'Alicel.jpg': 'abyss', 'Aliot.jpg':
                 'abyss', 'Aliza.jpg': 'save for later', 'Alligator.jpg': 'save for later', 'Alnoldi.jpg':
                 'save for later', 'Alphoccio.jpg': 'land of sorcery', 'Am Mut.jpg': 'save for later', 'Ambernite.jpg':
                 'save for later', 'Amdarais.jpg': 'shadow isles', 'Amon Ra.jpg': 'save for later', 'Anacondaq.jpg':
                 'save for later', 'Ancient Megalith.jpg': 'realm of ice', 'Ancient Mimic.jpg': 'save for later',
             'Ancient Mummy.jpg': 'save for later', 'Ancient Stalactic Golem.jpg': 'realm of ice',
             'Ancient Stone Shooter.jpg': 'forest', 'Ancient Tree.jpg': 'forest',
             'Ancient Tri Joint.jpg': 'save for later', 'Ancient Wootan Fighter.jpg': 'forest',
             'Ancient Wootan Shooter.jpg': 'forest', 'Ancient Worm.jpg': 'save for later',
             'Andre Egg.jpg': 'save for later', 'Andre Larva.jpg': 'save for later', 'Andre.jpg': 'save for later',
             'Anger Ninetail.jpg': 'forest', 'Angra Mantis.jpg': 'save for later', 'Angry Gazeti.jpg': 'realm of ice',
             'Angry Ice Titan.jpg': 'realm of ice', 'Angry Snowier.jpg': 'realm of ice',
             'Anolian.jpg': 'save for later', 'Anopheles.jpg': 'save for later', 'Antique Book.jpg': 'save for later',
             'Antonio.jpg': 'save for later', 'Anubis.jpg': 'shadow isles', 'Apocalipse.jpg': 'abyss',
             'Aqua Elemental.jpg': 'spirit world', 'Arc Angeling.jpg': 'save for later',
             'Arc Elder.jpg': 'land of sorcery', 'Arch Bishop Magaleta.jpg': 'land of sorcery',
             'Archdam.jpg': 'save for later', 'Archer Skeleton.jpg': 'save for later', 'Arclouze.jpg': 'save for later',
             'Argiope.jpg': 'save for later', 'Argos.jpg': 'save for later', 'Arhi.jpg': 'little man territory',
             'Armed Guard Soheon.jpg': 'spirit world', 'Armeyer Dinze.jpg': 'land of sorcery',
             'Assaulter.jpg': 'save for later', 'Aster.jpg': 'save for later', 'Atroce.jpg': 'save for later',
             'Aunoe.jpg': 'shadow isles', 'Baby Desert Wolf.jpg': 'save for later',
             'Baby Leopard.jpg': 'save for later', 'Banaspaty.jpg': 'save for later',
             'Banshee Master.jpg': 'land of sorcery', 'Banshee.jpg': 'shadow isles', 'Bapho Jr..jpg': 'save for later',
             'Baphomet.jpg': 'save for later', 'Baroness of Retribution.jpg': 'caves', 'Bathory.jpg': 'save for later',
             'Beetle King.jpg': 'save for later', 'Beholder Master.jpg': 'save for later',
             'Beholder.jpg': 'save for later', 'Berzebub.jpg': 'abyss', 'Big Bell.jpg': 'save for later',
             'Big Ben.jpg': 'save for later', 'Big Eggring.jpg': 'save for later', 'Bigfoot.jpg': 'save for later',
             'Bijou.jpg': 'spirit world', 'Bitter BonGun.jpg': 'realm of ice', 'Bitter Munak.jpg': 'spirit world',
             'Bitter Sohee.jpg': 'spirit world', 'Blazer.jpg': 'save for later',
             'Bloody Butterfly.jpg': 'save for later', 'Bloody Knight.jpg': 'save for later',
             'Bloody Murderer.jpg': 'save for later', 'Blue Acidus.jpg': 'save for later',
             'Blut Hase.jpg': 'little man territory', 'Boitata.jpg': 'forest', 'Bomi.jpg': 'mountain ranges',
             'Bongun.jpg': 'save for later', 'Bow Guardian.jpg': 'caves', 'Bradium Golem.jpg': 'save for later',
             'Breeze.jpg': 'save for later', 'Brilight.jpg': 'save for later', 'Brown Rat.jpg': 'save for later',
             'Bungisngis.jpg': 'save for later', 'Butoijo.jpg': 'caves', 'Byorgue.jpg': 'mountain ranges',
             'Captain Felock.jpg': 'save for later', 'Carat.jpg': 'save for later',
             'Cat O Nine Tails.jpg': 'save for later', 'Caterpillar.jpg': 'save for later',
             'Cecil Damon.jpg': 'save for later', 'Celia.jpg': 'spirit world', 'Celine Kimi.jpg': 'abyss',
             'Cendrawasih.jpg': 'save for later', 'Cenere.jpg': 'save for later',
             'Centipede Larva.jpg': 'save for later', 'Centipede.jpg': 'save for later',
             'Chaos Acolyte.jpg': 'save for later', 'Chaos Baphomet Jr..jpg': 'save for later',
             'Chaos Ghostring.jpg': 'save for later', 'Chaos Hunter Fly.jpg': 'save for later',
             'Chaos Killer Mantis.jpg': 'save for later', 'Chaos Mantis.jpg': 'save for later',
             'Chaos Poporing.jpg': 'save for later', 'Chaos Side Winder.jpg': 'save for later',
             'Chaos Stem Worm.jpg': 'save for later', 'Charge Basilisk.jpg': 'save for later',
             'Charleston.jpg': 'save for later', 'Chen.jpg': 'spirit world', 'Chepet.jpg': 'save for later',
             'Chimera.jpg': 'save for later', 'Choco.jpg': 'save for later', 'Chonchon.jpg': 'save for later',
             'Christmas Cookie.jpg': 'save for later', 'Clock.jpg': 'save for later',
             'Cloud Hermit.jpg': 'little man territory', 'Cobalt Mineral.jpg': 'save for later',
             'Coco.jpg': 'save for later', 'Colorful Teddy Bear.jpg': 'save for later', 'Comodo.jpg': 'save for later',
             'Condor.jpg': 'save for later', 'Cookie.jpg': 'save for later', 'Cornus.jpg': 'save for later',
             'Cornutus.jpg': 'save for later', 'Corrupt Life.jpg': 'caves', 'Corrupted Archer.jpg': 'abyss',
             'Corrupted Raydric.jpg': 'abyss', 'Corrupted Sting.jpg': 'save for later',
             'Corrupted Wanderer.jpg': 'abyss', 'Corruption Root.jpg': 'save for later', 'Coyote.jpg': 'desert',
             'Crab.jpg': 'save for later', 'Cramp.jpg': 'save for later', 'Creamy Fear.jpg': 'save for later',
             'Creamy.jpg': 'save for later', 'Creepy Demon.jpg': 'save for later', 'Cruiser.jpg': 'save for later',
             'Curupira.jpg': 'save for later', 'Dame of Sentinel.jpg': 'save for later',
             'Dancing Marionette.jpg': 'shadow isles', 'Dark Faceworm.jpg': 'forest',
             'Dark Frame.jpg': 'save for later', 'Dark Illusion.jpg': 'save for later', 'Dark Lord.jpg': 'shadow isles',
             'Dark Pinguicula.jpg': 'mountain ranges', 'Dark Priest.jpg': 'land of sorcery',
             'Dark Shadow.jpg': 'save for later', 'Death Word.jpg': 'save for later',
             'Decorated Evil Tree.jpg': 'save for later', 'Demon Pungus.jpg': 'save for later',
             'Demon-Apostle Ahat.jpg': 'abyss', 'Demon-Apostle Shaim.jpg': 'abyss',
             'Deranged Adventurer.jpg': 'mountain ranges', 'Desert Wolf.jpg': 'save for later',
             'Despero of Thanatos.jpg': 'save for later', 'Deviace.jpg': 'save for later',
             'Deviling.jpg': 'save for later', 'Deviruchi.jpg': 'save for later', 'Diabolic.jpg': 'save for later',
             'Dimik.jpg': 'save for later', 'Dio Anemos.jpg': 'little man territory', 'Disguise.jpg': 'save for later',
             'Dokebi.jpg': 'save for later', 'Dolomedes.jpg': 'save for later',
             'Dolor of Thanatos.jpg': 'save for later', 'Dolor.jpg': 'caves', 'Doppelganger.jpg': 'save for later',
             'DR815.jpg': 'save for later', 'Draco Egg.jpg': 'save for later', 'Draco.jpg': 'save for later',
             'Dracula.jpg': 'save for later', 'Dragon Egg.jpg': 'save for later', 'Dragon Fly.jpg': 'save for later',
             'Dragon Tail.jpg': 'save for later', 'Drake.jpg': 'save for later', 'Driller.jpg': 'desert',
             'Drops.jpg': 'save for later', 'Drosera.jpg': 'save for later', 'Dryad.jpg': 'forest',
             'Dullahan.jpg': 'shadow isles', 'Dumpling Child.jpg': 'save for later', 'Duneyrr.jpg': 'forest',
             'Dustiness.jpg': 'save for later', 'Dwigh.jpg': 'little man territory', 'E-EA1L.jpg': 'spirit world',
             'E-EA2S.jpg': 'save for later', 'Earth Deleter.jpg': 'save for later',
             'Earth Petite.jpg': 'save for later', 'Echio.jpg': 'little man territory', 'Eclipse.jpg': 'save for later',
             'Eddga.jpg': 'save for later', 'Eggring.jpg': 'save for later', 'Eggyra.jpg': 'save for later',
             'Egnigem Cenia.jpg': 'save for later', 'EL-A17T.jpg': 'save for later',
             'Elder Willow.jpg': 'save for later', 'Elder.jpg': 'save for later',
             'Elite Revolver Buffalo Bandit.jpg': 'caves', 'Elite Scimitar Buffalo Bandit.jpg': 'caves',
             'Elite Shotgun Buffalo Bandit.jpg': 'caves', 'Elvira.jpg': 'save for later',
             'Enchanted Peach Tree.jpg': 'save for later', 'Engkanto.jpg': 'forest', 'Enhanced Amdarais.jpg': 'desert',
             'Enhanced Archer Skeleton.jpg': 'abyss', 'Enhanced Soldier Skeleton.jpg': 'save for later',
             'Entweihen Crothen.jpg': 'save for later', 'Eremes Guile.jpg': 'shadow isles',
             'Errende Ebecee.jpg': 'land of sorcery', 'Essence of Evil.jpg': 'save for later',
             'Evil Druid.jpg': 'save for later', 'Evil Dwelling Box.jpg': 'save for later',
             'Evil Nymph.jpg': 'save for later', 'Evil Shadow.jpg': 'save for later',
             'Evil Snake Lord.jpg': 'save for later', 'Executioner.jpg': 'save for later',
             'Exploration Rover Turbo.jpg': 'save for later', 'Explosion.jpg': 'save for later',
             'Fabre.jpg': 'save for later', 'Faceworm Egg.jpg': 'save for later',
             'Faceworm Larva.jpg': 'save for later', 'Faceworm.jpg': 'save for later',
             'Faithful Manager.jpg': 'save for later', 'Fallen Bishop Hibram.jpg': 'save for later',
             'False Angel.jpg': 'save for later', 'Familiar.jpg': 'save for later', 'Fanat.jpg': 'shadow isles',
             'Fay Kanavian.jpg': 'save for later', 'Faymont.jpg': 'save for later',
             'Female Thief Bug.jpg': 'save for later', 'Fire Condor.jpg': 'save for later',
             'Fire Frilldora.jpg': 'save for later', 'Fire Golem.jpg': 'save for later',
             'Fire Sandman.jpg': 'save for later', 'Firebug.jpg': 'save for later',
             'Firelock Soldier.jpg': 'save for later', 'Firm Air Deleter.jpg': 'save for later',
             'Firm Blazzer.jpg': 'save for later', 'Firm Explosion.jpg': 'save for later',
             'Firm Ground Deleter.jpg': 'save for later', 'Firm Kaho.jpg': 'spirit world',
             'Firm Lava Golem .jpg': 'shadow isles', 'Firm Nightmare Terror.jpg': 'save for later',
             'Flame Ghost.jpg': 'abyss', 'Flame Skull.jpg': 'save for later', 'Flamel.jpg': 'abyss',
             'Flora.jpg': 'save for later', 'Freezer.jpg': 'save for later', 'Frilldora.jpg': 'save for later',
             'Frozen Wolf.jpg': 'realm of ice', 'Fruit Pom Spider.jpg': 'save for later', 'Frus.jpg': 'save for later',
             'Gajomart.jpg': 'save for later', 'Galapago.jpg': 'save for later', 'Galion.jpg': 'desert',
             'Gargoyle.jpg': 'save for later', 'Gaster.jpg': 'save for later', 'Gazeti.jpg': 'save for later',
             'GC109.jpg': 'save for later', 'Geffen Bully.jpg': 'save for later',
             'Geffen Gang Member.jpg': 'save for later', 'Geffen Shoplifter.jpg': 'save for later',
             'Gemini-S58.jpg': 'save for later', 'General Egnigem Cenia.jpg': 'shadow isles',
             'Genetic Flamel.jpg': 'land of sorcery', 'Geographer.jpg': 'save for later',
             'Gertie.jpg': 'save for later', 'Ghostring.jpg': 'save for later', 'Ghoul.jpg': 'save for later',
             'Giant Hornet.jpg': 'save for later', 'Giant Spider.jpg': 'save for later',
             'Giant Whisper.jpg': 'save for later', 'Gibbet.jpg': 'save for later', 'Giearth.jpg': 'save for later',
             'Gig.jpg': 'save for later', 'Gigantes.jpg': 'caves', 'Gioia.jpg': 'save for later',
             'Gloom Under Night.jpg': 'save for later', 'Goat.jpg': 'save for later',
             'Goblin Archer.jpg': 'save for later', 'Goblin Leader.jpg': 'save for later',
             'Goblin Steamrider.jpg': 'save for later', 'Goblin.jpg': 'save for later',
             'Gold Acidus.jpg': 'save for later', 'Gold Queen Scaraba.jpg': 'caves',
             'Gold Scaraba.jpg': 'save for later', 'Golden Thief Bug.jpg': 'save for later',
             'Golem.jpg': 'save for later', 'Gopinich.jpg': 'save for later', 'Grand Peco.jpg': 'save for later',
             'Grass Fabre.jpg': 'save for later', 'Greater Bellare.jpg': 'mountain ranges',
             'Greater Sanare.jpg': 'land of sorcery', 'Green Cenere.jpg': 'save for later',
             'Green Ferus.jpg': 'save for later', 'Green Maiden.jpg': 'save for later', 'Gremlin.jpg': 'save for later',
             'Grim Reaper Ankou.jpg': 'shadow isles', 'Grizzly.jpg': 'save for later', 'Grove.jpg': 'save for later',
             'Grudge of Royal Knight.jpg': 'abyss', 'Gryphon.jpg': 'desert',
             'Guillotine Cross Eremes.jpg': 'shadow isles', 'Gullinbursti.jpg': 'save for later',
             'Hallway Security Device.jpg': 'save for later', 'Hardrock Mammoth.jpg': 'realm of ice',
             'Hardworking Pitman.jpg': 'save for later', 'Harpy.jpg': 'save for later',
             'Hatii Babe.jpg': 'save for later', 'Hatii.jpg': 'save for later', 'Headless Mule.jpg': 'save for later',
             'Heart Hunter Bellare.jpg': 'save for later', 'Heart Hunter Evil.jpg': 'abyss',
             'Heart Hunter.jpg': 'caves', 'Heater.jpg': 'save for later', 'Heavy Metaling.jpg': 'save for later',
             'Hell Apocalypse.jpg': 'save for later', 'Hell Poodle.jpg': 'save for later',
             'Hermit Plant.jpg': 'save for later', 'High Orc.jpg': 'save for later', 'Hill Wind.jpg': 'save for later',
             'Hillsrion.jpg': 'save for later', 'Hode.jpg': 'save for later', 'Hodremlin.jpg': 'save for later',
             'Holden.jpg': 'save for later', 'Holy Frus.jpg': 'save for later', 'Holy Skogul.jpg': 'spirit world',
             'Horn.jpg': 'save for later', 'Hornet.jpg': 'save for later', 'Horong.jpg': 'save for later',
             'Howard Alt-Eisen.jpg': 'save for later', 'Humanoid Chimera.jpg': 'land of sorcery',
             'Hunter Fly.jpg': 'save for later', 'Hunter Wolf.jpg': 'save for later', 'Hydra.jpg': 'save for later',
             'Hydrolancer.jpg': 'save for later', 'Hylozoist.jpg': 'spirit world', 'Iara.jpg': 'save for later',
             'Ice Ghost.jpg': 'realm of ice', 'Ice Titan.jpg': 'save for later', 'Ifodes.jpg': 'save for later',
             'Ifrit.jpg': 'spirit world', 'Immortal Corps.jpg': 'save for later',
             'Immortal Cursed Knight.jpg': 'save for later', 'Immortal Wind Ghost.jpg': 'save for later',
             'Imp.jpg': 'save for later', 'Incubus.jpg': 'save for later', 'Injustice.jpg': 'save for later',
             'Irene High Elder.jpg': 'save for later', 'Iron Fist.jpg': 'save for later', 'Isilla.jpg': 'shadow isles',
             'Isis.jpg': 'shadow isles', 'Jaguar.jpg': 'save for later', 'Jakk.jpg': 'save for later',
             'Jejeling.jpg': 'save for later', 'Jing Guai.jpg': 'save for later', 'Jitterbug.jpg': 'save for later',
             'Joker.jpg': 'save for later', 'Ju.jpg': 'little man territory', 'Jungle Mandragora.jpg': 'save for later',
             'Kaho.jpg': 'save for later', 'Kapha.jpg': 'save for later', 'Karakasa.jpg': 'save for later',
             'Kasa.jpg': 'save for later', 'Kathryne Keyron.jpg': 'save for later',
             'Kavach Icarus.jpg': 'save for later', 'Khalitzburg Knight.jpg': 'save for later',
             'Khalitzburg.jpg': 'save for later', 'Kiel-D-01.jpg': 'save for later',
             'Killer Mantis.jpg': 'save for later', 'King Dramoh.jpg': 'save for later',
             'Knight Sakray.jpg': 'shadow isles', 'Knocker.jpg': 'save for later',
             'Kobold Archer.jpg': 'save for later', 'Kobold Leader.jpg': 'save for later',
             'Kobold.jpg': 'save for later', 'Kraben.jpg': 'save for later', 'Kraken.jpg': 'save for later',
             'Kukre.jpg': 'save for later', 'Kuro Akuma.jpg': 'save for later', 'Lady Solace.jpg': 'save for later',
             'Lady Tanee.jpg': 'save for later', 'Laurell Weinder.jpg': 'save for later',
             'Lava Golem.jpg': 'save for later', 'Leaf Cat.jpg': 'save for later', 'Leaf Lunatic.jpg': 'save for later',
             'Leak.jpg': 'save for later', 'Leib Olmai.jpg': 'save for later', 'Les.jpg': 'save for later',
             'Licheniyes.jpg': 'save for later', 'Lichtern Blue.jpg': 'save for later',
             'Lichtern Green.jpg': 'save for later', 'Lichtern Red.jpg': 'save for later',
             'Lichtern Yellow.jpg': 'save for later', 'Little Fatum.jpg': 'save for later',
             'Lockstep.jpg': 'save for later', 'Loli Ruri.jpg': 'save for later',
             'Lord of The Dead.jpg': 'save for later', 'Luciola Vespa.jpg': 'save for later',
             'Lude.jpg': 'save for later', 'Lunatic.jpg': 'save for later', 'Maero of Thanatos.jpg': 'spirit world',
             'Magmaring.jpg': 'save for later', 'Magnolia.jpg': 'save for later', 'Majoruros.jpg': 'save for later',
             'Male Thief Bug.jpg': 'save for later', 'Malicious Baby Ghost.jpg': 'little man territory',
             'Manananggal.jpg': 'forest', 'Mandragora.jpg': 'save for later', 'Mangkukulam.jpg': 'save for later',
             'Mantis.jpg': 'save for later', 'Mao Guai.jpg': 'land of sorcery', 'Marc.jpg': 'save for later',
             'Marduk.jpg': 'save for later', 'Margaretha Sorin.jpg': 'spirit world', 'Marin.jpg': 'save for later',
             'Marina.jpg': 'save for later', 'Marine Sphere.jpg': 'save for later', 'Marionette.jpg': 'shadow isles',
             'Marse.jpg': 'save for later', 'Marsh Arclouse.jpg': 'save for later', 'Martin.jpg': 'save for later',
             'Mastering.jpg': 'save for later', 'Material Chimera.jpg': 'save for later',
             'Matt Drainliar.jpg': 'save for later', 'Matyr.jpg': 'save for later', 'Mavka.jpg': 'save for later',
             'Maya Purple.jpg': 'save for later', 'Maya.jpg': 'save for later',
             'Mechanic Howard.jpg': 'mountain ranges', 'Mechaspider.jpg': 'caves', 'Medusa.jpg': 'save for later',
             'Megalith.jpg': 'save for later', 'Megalodon.jpg': 'save for later', 'Memory of Thanatos.jpg': 'desert',
             'Menblatt.jpg': 'save for later', 'Merman.jpg': 'save for later', 'Metaling.jpg': 'save for later',
             'Metaller.jpg': 'save for later', 'Mi Gao.jpg': 'save for later', 'Mimic.jpg': 'save for later',
             'Miming.jpg': 'save for later', 'Mineral.jpg': 'save for later', 'Mini Demon.jpg': 'save for later',
             'Minorous.jpg': 'save for later', 'Minstel Alphoccio.jpg': 'abyss',
             'Mistress of Shelter.jpg': 'spirit world', 'Mistress.jpg': 'save for later',
             'Miyabi Doll.jpg': 'save for later', 'Mobster.jpg': 'save for later',
             'Moonlight Flower.jpg': 'save for later', 'Moroccs Minion.jpg': 'spirit world',
             'Muka.jpg': 'save for later', 'Mummy.jpg': 'save for later', 'Munak.jpg': 'save for later',
             'Muscipular.jpg': 'save for later', 'Mutand Dolor.jpg': 'caves', 'Mutant Dragonoid.jpg': 'forest',
             'Mutant Plaga.jpg': 'desert', 'Mutant Twin Caput.jpg': 'save for later',
             'Mutant Venenum.jpg': 'save for later', 'Myst Case.jpg': 'save for later', 'Myst.jpg': 'save for later',
             'Mysteltainn.jpg': 'save for later', 'Naga.jpg': 'save for later', 'Necromancer.jpg': 'save for later',
             'Neo Punk.jpg': 'save for later', 'Nepenthes.jpg': 'save for later', 'Nereid.jpg': 'save for later',
             'Nidhoggur Shadow.jpg': 'save for later', 'Nightmare Amon Ra.jpg': 'save for later',
             'Nightmare Ancient Mummy.jpg': 'desert', 'Nightmare Arclouse.jpg': 'save for later',
             'Nightmare Mimic.jpg': 'save for later', 'Nightmare Minorous.jpg': 'save for later',
             'Nightmare Mummy.jpg': 'save for later', 'Nightmare Terror.jpg': 'save for later',
             'Nightmare Timer Keeper.jpg': 'desert', 'Nightmare Verit.jpg': 'save for later',
             'Nightmare.jpg': 'save for later', 'Nine Tail.jpg': 'save for later',
             'Novice Poring.jpg': 'save for later', 'Noxious.jpg': 'save for later', 'Obeaune.jpg': 'save for later',
             'Obsidian.jpg': 'save for later', 'Octopus.jpg': 'save for later',
             'Odium ofThanatos.jpg': 'save for later', 'Odoric.jpg': 'save for later',
             'Ogretooth.jpg': 'save for later', 'Ominous Assaulter.jpg': 'save for later',
             'Ominous Freezer.jpg': 'save for later', 'Ominous Heater.jpg': 'save for later',
             'Ominous Permeter.jpg': 'save for later', 'Ominous Solider.jpg': 'save for later',
             'Orc Archer.jpg': 'save for later', 'Orc Baby.jpg': 'save for later', 'Orc Hero.jpg': 'save for later',
             'Orc Lady.jpg': 'save for later', 'Orc Lord.jpg': 'save for later', 'Orc Skeleton.jpg': 'save for later',
             'Orc Warrior.jpg': 'save for later', 'Orc Zombie.jpg': 'save for later', 'Ordre.jpg': 'save for later',
             'Osiris.jpg': 'save for later', 'Owl Baron.jpg': 'save for later', 'Owl Duke.jpg': 'save for later',
             'Owl Marquees.jpg': 'save for later', 'Owl Viscount.jpg': 'save for later',
             'Panzer Goblin.jpg': 'save for later', 'Parasite.jpg': 'save for later', 'Parus.jpg': 'save for later',
             'Pasana.jpg': 'save for later', 'Payon Soldier.jpg': 'save for later',
             'Peco Peco Egg.jpg': 'save for later', 'Peco Peco.jpg': 'save for later', 'Penomena.jpg': 'save for later',
             'Permeter.jpg': 'save for later', 'Pest.jpg': 'save for later', 'Petal.jpg': 'save for later',
             'Pharaoh.jpg': 'save for later', 'Phen.jpg': 'save for later', 'Phendark.jpg': 'save for later',
             'Phreeoni.jpg': 'save for later', 'Phylla.jpg': 'spirit world', 'Picky Egg.jpg': 'save for later',
             'Picky.jpg': 'save for later', 'Pinguicula.jpg': 'save for later', 'Piranha.jpg': 'save for later',
             'Pirate Skeleton.jpg': 'save for later', 'Pitman.jpg': 'save for later', 'Plaga.jpg': 'caves',
             'Plankton.jpg': 'save for later', 'Plasma.jpg': 'save for later', 'Playing Pere.jpg': 'save for later',
             'Poison Spore.jpg': 'save for later', 'Poisonous Toad.jpg': 'save for later',
             'Pom Spider.jpg': 'save for later', 'Poporing.jpg': 'save for later', 'Porcellio.jpg': 'save for later',
             'Poring.jpg': 'save for later', 'Pot Dofle.jpg': 'save for later',
             'Powerful Skeleton.jpg': 'save for later', 'Punk.jpg': 'save for later', 'Pupa.jpg': 'save for later',
             'Queen Scaraba.jpg': 'caves', 'Quve.jpg': 'save for later', 'Rafflesia.jpg': 'save for later',
             'Ragged Zombie.jpg': 'save for later', 'Raggler.jpg': 'save for later', 'Randel.jpg': 'abyss',
             'Randgris.jpg': 'abyss', 'Ranger Cecil.jpg': 'mountain ranges', 'Rata.jpg': 'save for later',
             'Raydric Archer.jpg': 'save for later', 'Raydric.jpg': 'save for later',
             'Realized Amdarais.jpg': 'save for later', 'Realized Corruption Root.jpg': 'save for later',
             'Red Eruma.jpg': 'save for later', 'Red Ferus.jpg': 'save for later', 'Red Novus.jpg': 'save for later',
             'Remover.jpg': 'save for later', 'Repair Robot Turbo.jpg': 'save for later',
             'Requiem.jpg': 'save for later', 'Restless Dead.jpg': 'save for later',
             'Revolver Buffalo Bandit.jpg': 'desert', 'Rhyncho.jpg': 'save for later', 'Rideword.jpg': 'save for later',
             'Rocker.jpg': 'save for later', 'Roda Frog.jpg': 'save for later', 'Rotar Zairo.jpg': 'save for later',
             'Roween.jpg': 'save for later', 'Royal Guard Randel.jpg': 'save for later',
             'RSX-0806.jpg': 'save for later', 'Rudo.jpg': 'save for later', 'Rune Knight Seyren.jpg': 'shadow isles',
             'Rybio.jpg': 'save for later', 'Sage Worm.jpg': 'save for later', 'Salamander.jpg': 'abyss',
             'Samurai Spector.jpg': 'save for later', 'Sanare.jpg': 'land of sorcery', 'Sandman.jpg': 'save for later',
             'Santa Poring.jpg': 'save for later', 'Sarah.jpg': 'save for later', 'Sasquatch.jpg': 'save for later',
             'Savage Babe.jpg': 'save for later', 'Savage.jpg': 'save for later', 'Scaraba.jpg': 'save for later',
             'Scimitar Buffalo Bandit.jpg': 'save for later', 'Scorpion King.jpg': 'save for later',
             'Scorpion.jpg': 'save for later', 'Scout Basilisk.jpg': 'save for later',
             'Scrap Robots.jpg': 'save for later', 'Sea-Otter.jpg': 'save for later', 'Seal.jpg': 'save for later',
             'Security Robot.jpg': 'save for later', 'Sedora.jpg': 'little man territory',
             'Seeker.jpg': 'save for later', 'Seyren Windsor.jpg': 'caves', 'Shadow Chaser Gertie.jpg': 'caves',
             'Shell Fish.jpg': 'save for later', 'Shinobi.jpg': 'save for later',
             'Shotgun Buffalo Bandit.jpg': 'desert', 'Sidewinder.jpg': 'save for later',
             'Singing Pere.jpg': 'save for later', 'Sinister Obsidian.jpg': 'save for later',
             'Siorava.jpg': 'save for later', 'Siroma.jpg': 'save for later', 'Skeggiold.jpg': 'save for later',
             'Skeleton General.jpg': 'save for later', 'Skeleton Prisoner.jpg': 'save for later',
             'Skeleton Worker.jpg': 'save for later', 'Skeleton.jpg': 'save for later', 'Skogul.jpg': 'save for later',
             'Sky Deleter.jpg': 'save for later', 'Sky Petite.jpg': 'save for later', 'Sleeper.jpg': 'save for later',
             'Smokie.jpg': 'save for later', 'Snake.jpg': 'save for later', 'Snowier.jpg': 'save for later',
             'Sohee.jpg': 'save for later', 'Soldier Andre.jpg': 'save for later',
             'Soldier Skeleton.jpg': 'save for later', 'Solider.jpg': 'save for later',
             'Sorcerer Celia.jpg': 'shadow isles', 'Soul Fragment.jpg': 'save for later', 'Spore.jpg': 'save for later',
             'Spring Rabbit.jpg': 'save for later', 'Sropho.jpg': 'save for later', 'Stainer.jpg': 'save for later',
             'Stalactic Golem.jpg': 'save for later', 'Stalker Gertie.jpg': 'save for later',
             'Stapo.jpg': 'save for later', 'Steel Chonchon.jpg': 'save for later', 'Stem Worm.jpg': 'save for later',
             'Step.jpg': 'save for later', 'Stephen Jack Ernest Wolf.jpg': 'save for later',
             'Sting.jpg': 'save for later', 'Stone Shooter.jpg': 'save for later',
             'Stormy Knight.jpg': 'save for later', 'Strouf.jpg': 'save for later', 'Succubus.jpg': 'save for later',
             'Sura Chen.jpg': 'spirit world', 'Sweet Nightmare.jpg': 'shadow isles',
             'Sweet Roda Frog.jpg': 'save for later', 'Sword Guardian.jpg': 'save for later',
             'Swordfish.jpg': 'save for later', 'Taffy.jpg': 'save for later', 'Tamruan.jpg': 'save for later',
             'Tao Gunka.jpg': 'save for later', 'Tarou.jpg': 'save for later', 'Tatacho.jpg': 'save for later',
             'Teddy Bear.jpg': 'save for later', 'Tendrilrion.jpg': 'save for later', 'Tengu.jpg': 'save for later',
             'Thara Frog.jpg': 'save for later', 'The Paper.jpg': 'save for later',
             'Thief Bug Egg.jpg': 'save for later', 'Thief Bug.jpg': 'save for later',
             'Tikbalang.jpg': 'save for later', 'Time Holder.jpg': 'save for later', 'Tiyanak.jpg': 'save for later',
             'Toad.jpg': 'save for later', 'Toucan.jpg': 'save for later', 'Tower Keeper.jpg': 'save for later',
             'Trance Spore.jpg': 'save for later', 'Trentini.jpg': 'save for later', 'Tri Joint.jpg': 'save for later',
             'True Alphoccio.jpg': 'little man territory', 'True Cecil Damon.jpg': 'little man territory',
             'True Celia Alde.jpg': 'little man territory', 'True Chen Liu.jpg': 'little man territory',
             'True Eremes Guile.jpg': 'little man territory', 'True Flamel Emure.jpg': 'little man territory',
             'True Gertie.jpg': 'save for later', 'True Howard Alt-Eisen.jpg': 'little man territory',
             'True Kathryne Keyron.jpg': 'little man territory', 'True Margaretha Sorin.jpg': 'little man territory',
             'True Randel Lawrence.jpg': 'little man territory', 'True Seyren Windsor.jpg': 'save for later',
             'True Trentini.jpg': 'save for later', 'Turtle General.jpg': 'save for later',
             'Twin Caput.jpg': 'save for later', 'Ungoliant.jpg': 'save for later', 'Uzhas.jpg': 'save for later',
             'Vadon.jpg': 'save for later', 'Vagabond Wolf.jpg': 'save for later', 'Vanberk.jpg': 'save for later',
             'Vavayaga.jpg': 'save for later', 'Venatu.jpg': 'save for later', 'Venenum.jpg': 'save for later',
             'Venomous Chimera.jpg': 'save for later', 'Venomous.jpg': 'save for later', 'Verit.jpg': 'save for later',
             'Vesper.jpg': 'save for later', 'Vicious Cookie.jpg': 'save for later', 'Violy.jpg': 'save for later',
             'Vitata.jpg': 'save for later', 'Vocal.jpg': 'save for later', 'Wakwak.jpg': 'save for later',
             'Wanderer Trentini.jpg': 'save for later', 'Wanderer.jpg': 'save for later',
             'Warlock Kathryne.jpg': 'save for later', 'Warrior Lola.jpg': 'save for later',
             'Waste Stove.jpg': 'save for later', 'Watcher.jpg': 'save for later',
             'Weakened Fenrir.jpg': 'save for later', 'Whisper.jpg': 'save for later', 'White Knight.jpg': 'abyss',
             'White Lady.jpg': 'save for later', 'Wickebine Tres.jpg': 'save for later',
             'Wild Hornet.jpg': 'save for later', 'Wild Rider.jpg': 'save for later', 'Willow.jpg': 'save for later',
             'Wind Ghost.jpg': 'save for later', 'Wizard Of Veritas.jpg': 'realm of ice', 'Wolf.jpg': 'save for later',
             'Wood Goblin.jpg': 'save for later', 'Wooden Golem.jpg': 'save for later',
             'Wootan Fighter.jpg': 'save for later', 'Wootan Shooter.jpg': 'save for later',
             'Wormtail.jpg': 'save for later', 'Wraith Dead.jpg': 'spirit world', 'Wraith.jpg': 'abyss',
             'Yao Jun.jpg': 'save for later', 'Yellow Novus.jpg': 'save for later', 'Yoyo.jpg': 'save for later',
             'Zakudam.jpg': 'save for later', 'Zealotus.jpg': 'save for later', 'Zenorc.jpg': 'save for later',
             'Zerom.jpg': 'save for later', 'Zhu Po Long.jpg': 'save for later', 'Zipper Bear.jpg': 'save for later',
             'Zombie Guard.jpg': 'shadow isles', 'Zombie Master.jpg': 'save for later',
             'Zombie Prisoner.jpg': 'save for later', 'Zombie Slaughter.jpg': 'save for later',
             'Zombie.jpg': 'save for later', }

first_area_dict = {
    'slime': ['enemies/area_1/first_enemy.png']
}

for enemy, path in mobs_dict.items():
    if path == 'save for later':
        pass
    else:
        if path == 'desert':
            pic_path = 'enemies/area_1/' + enemy
            lvl = random.randint(1, 10)
            first_area_dict[enemy[:-4]] = [pic_path]


def wish_processing(wish_type):
    if wish_type == 'primogems':
        wished_number = random.randint(1, 10000)
        print(wished_number)
        if wished_number < 3333:
            return 5
        elif wished_number < 6666:
            return 4
        else:
            return 3
    else:
        pass


def wish_reward(wish_type, item_rarity):
    outcome = ''
    if wish_type == 'primogems':
        outcome = random.choice(primogems_wish_outcome[item_rarity])
        print(outcome)

    return outcome


def get_time():
    samara_time = pytz.timezone('Europe/Samara')
    time = datetime.now(samara_time)
    return time.strftime("%H:%M:%S")[:2]


async def dailie_reset():
    while True:
        time = get_time()
        print(time)
        if int(time) == 0:
            db_object.execute(f'UPDATE users SET start_lvl = 0')
            db_object.execute(f'UPDATE dailies SET accomplishment = 0')
            db_object.execute(f'UPDATE users set energy_left = 100')
            db_object.execute(f'UPDATE users set rank_exp_left = 1000')
            db_object.execute(f'UPDATE users set dailies_left = daily')
            db_connection.commit()
            print('daily reset was done successfully ')
        await asyncio.sleep(3600)
