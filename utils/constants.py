from enum import Enum
from collections.abc import Callable

# constants
GCD = 1.5 #s

class Race(Enum):
    ORC = 1
    TAUREN = 2
    TROLL = 3

class Race:
    def __init__(self,race: Race):
        # https://www.wowhead.com/classic/guide/classic-wow-horde-races-and-racial-abilities
        self.race = race
        self.base_mana = 55
        if race == Race.ORC:
            self.base_intellect = 18
            self.base_spirit = 25
        elif race == Race.TAUREN:
            self.base_intellect = 16
            self.base_spirit = 24
        elif race == Race.TROLL:
            self.base_intellect = 17
            self.base_spirit = 23
        else:
            print("Unsupported race!")

class Buff:
    def __init__(self):
        self.intellect_bonus = 0
        self.spirit_bonus = 0
        self.max_duration_sec = 0

    def get_intellect_bonus(self,time_elapsed_sec):
        """Returns the intellect bonus"""
        if time_elapsed_sec <= self.max_duration_sec:
            return(self.intellect_bonus)
        else:
            return(0)
        
    def get_spirit_bonus(self,time_elapsed_sec):
        """Returns the intellect bonus"""
        if time_elapsed_sec <= self.max_duration_sec:
            return(self.spirit_bonus)
        else:
            return(0)

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

class GearSet:
    "single set of gear"
    def __init__(self,gear_set,name):
        self.gear_set = gear_set
        self.gear_set_name = name
        self.gear_set_piece_count = len(gear_set)
        self.total_intellect_bonus = 0
        self.total_spirit_bonus = 0
        self.total_spellpower_bonus = 0
        self.total_mp5_bonus = 0

        for gear in gear_set:
            self.total_intellect_bonus += gear.get_intellect_bonus()
            self.total_spirit_bonus += gear.get_spirit_bonus()
            self.total_spellpower_bonus += gear.get_spellpower_bonus()
            self.total_mp5_bonus += gear.get_mp5_bonus()

        return

    def get_total_intellect_bonus(self):
        return(self.total_intellect_bonus)

    def get_total_spirit_bonus(self):
        return(self.total_spirit_bonus) 

    def get_total_spellpower_bonus(self):
        return(self.total_spellpower_bonus)

    def get_total_mp5_bonus(self):
        return(self.total_mp5_bonus)
    
class Character(Race):
    """High level class to define a character"""
    def __init__(
            self,
            race: Race,
            spec,
            buffs: list[Buff],
            gear_set: GearSet,
            rotation: Callable,
        ):
        super().__init__(race)
        # metadata
        self.time_elapsed_sec = 0
        self.spec = spec
        self.gear_set = gear_set # list gear
        self.buffs = buffs # list of buffs
        self.rotation = rotation
        # update primary stats
        self._update_primary_stats()
        # update secondary stats
        self._update_secondary_stats()
        # update mana
        self.mana = self.max_mana

    def _update_primary_stats(self):
        """Updates primary stats"""
        self.intellect = self.base_intellect + self.gear_set.get_total_intellect_bonus()
        self.spirit = self.base_spirit + self.gear_set.get_total_spirit_bonus()
        for buff in self.buffs:
            self.intellect += buff.get_intellect_bonus(self.time_elapsed_sec)
            self.spirit += buff.get_spirit_bonus(self.time_elapsed_sec)
        return

    def _update_secondary_stats(self):
        """Updates secondary stats"""
        self.max_mana = self.base_mana + min(20,self.intellect) + 15*(self.intellect - min(20,self.intellect))
        self.spell_crit_chance = (self.intellect / 59.5) / 100
        self.spellpower = self.gear_set.get_total_spellpower_bonus()
        self.mp5_while_casting = self.gear_set.get_total_mp5_bonus()
        self.mp5_while_not_casting = self.mp5_while_casting + (self.spirit/5 + 17)/2*5
    
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
