from enum import Enum

# constants
GCD = 1.5 #s

class Race:
    def __init__(self,race):
        # https://www.wowhead.com/classic/guide/classic-wow-horde-races-and-racial-abilities
        self.race = race
        if race == "Orc":
            self.base_intellect = 18
            self.base_spirit = 25
        elif race == "Tauren":
            self.base_intellect = 16
            self.base_spirit = 24
        elif race == "Troll":
            self.base_intellect = 17
            self.base_spirit = 23
        else:
            print("Unsupported race!")

class Character(Race):
    """High level class to define a character"""
    def __init__(self,race,spec,buffs,gear_set,rotation):
        super().__init__(race)
        # time elapsed
        self.time_elapsed_sec = 0
        # determine base stats
        self.base_intellect = self._determine_base_intellect(gear_set)
        # current stats
        self.intellect = self._determine_current_intellect(spec,buffs,gear_set)
        self.spirit = 0
        self.max_mana = 0
        self.mana = 0
        self.spell_crit_chance = 0
        self.spellpower = 0
        self.mp5_while_casting = 0
        self.mp5_while_not_casting = 0
        self.mp5 = self.mp5_while_not_casting
        # other
        self.rotation = rotation
    
    def _determine_base_intellect(self,gear_set):
        """Determines the characters base intellect, which is time invariant"""
        intellect = self.base_intellect
    
    def _determine_current_intellect(self,buffs):
        """Determines the characters current intellect, which is time varying"""
        intellect = self.base_intellect
        for buff in buffs:
            intellect += buff.get_intellect_bonus(self.time_elapsed_sec)
        
        return(intellect)

    def _determine_current_intellect(self,spec,buffs,gear_set):
        """Determines the characters intellect"""
        intellect = self.intellect
        for buff in buffs:
            intellect += buff.get_intellect_bonus(self.time_elapsed_sec)
        
        return(intellect)
    
    def print_current_state(self):
        """Prints the current character state"""
        print("Character State:")
        print("\tintellect: {}".format(self.intellect))
        print("\tspirit: {}".format(self.spirit))
        print("\tmax_mana: {}".format(self.max_mana))
        print("\tmana: {}".format(self.mana))
        print("\tspell_crit_chance: {}".format(self.spell_crit_chance))
        print("\tspellpower: {}".format(self.spellpower))
        print("\tmp5_while_casting: {}".format(self.mp5_while_casting))
        print("\tmp5_while_not_casting: {}".format(self.mp5_while_not_casting))
        print("\tmp5: {}".format(self.mp5))

class GearSlot(Enum):
    HEAD = 1
    NECK = 2
    SHOULDERS = 3
    BACK = 4
    CHEST = 5
    WRISTS = 6
    MAINHAND = 7
    OFFHAND = 8
    HANDS = 9
    WAIST = 10
    LEGS = 11
    FEET = 12
    FINGER = 13
    TRINKET = 14

class Enchant:
    def __init__(self,name,slot,intellect_bonus=0,spirit_bonus=0,spellpower_bonus=0,mp5_bonus=0):
        self.name = name
        self.slot = slot
        self.intellect_bonus = intellect_bonus
        self.spirit_bonus = spirit_bonus
        self.spellpower_bonus = spellpower_bonus
        self.mp5_bonus = mp5_bonus

    def get_intellect_bonus(self):
        return(self.intellect_bonus)

    def get_spirit_bonus(self):
        return(self.spirit_bonus) 

    def get_spellpower_bonus(self):
        return(self.spellpower_bonus) 

    def get_mp5_bonus(self):
        return(self.mp5_bonus)       

class Gear:
    def __init__(self,name,slot,intellect_bonus=0,spirit_bonus=0,spellpower_bonus=0,mp5_bonus=0):
        self.name = name
        self.slot = slot
        self.intellect_bonus = intellect_bonus
        self.spirit_bonus = spirit_bonus
        self.spellpower_bonus = spellpower_bonus
        self.mp5_bonus = mp5_bonus

    def get_intellect_bonus(self):
        return(self.intellect_bonus)

    def get_spirit_bonus(self):
        return(self.spirit_bonus) 

    def get_spellpower_bonus(self):
        return(self.spellpower_bonus) 

    def get_mp5_bonus(self):
        return(self.mp5_bonus)

    def enchant(self,enchant):
        self.intellect_bonus += enchant.get_intellect_bonus()
        self.spirit_bonus += enchant.get_spirit_bonus()
        self.spellpower_bonus += enchant.get_spellpower_bonus()
        self.mp5_bonus += enchant.get_mp5_bonus()
        return(self)

    def print_stat_bonuses(self):
        print("{} ({})".format(self.name,self.slot))
        print("\tintellect_bonus: {}".format(self.intellect_bonus))
        print("\tspirit_bonus: {}".format(self.spirit_bonus))
        print("\tspellpower_bonus: {}".format(self.spellpower_bonus))
        print("\tmp5_bonus: {}".format(self.mp5_bonus))