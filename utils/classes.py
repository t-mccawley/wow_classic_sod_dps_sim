from enum import Enum

class Race:
    def __init__(self,race: str, level: int):
        # https://www.wowhead.com/classic/guide/classic-wow-horde-races-and-racial-abilities
        self.race = race
        self.level = level
        if race == "Orc":
            if level == 25:
                self.base_intellect = 40
                self.base_spirit = 50
                self.base_mana = self._compute_base_mana(825)
            else:
                print("Unsupported level!")
        elif race == "Tauren":
            if level == 25:
                self.base_intellect = 38
                self.base_spirit = 49
                self.base_mana = self._compute_base_mana(795)
            else:
                print("Unsupported level!")
        elif race == "Troll":
            if level == 25:
                self.base_intellect = 39
                self.base_spirit = 48
                self.base_mana = self._compute_base_mana(810)
            else:
                print("Unsupported level!")
        else:
            print("Unsupported race!")
    
    def _compute_base_mana(self,total_mana):
        return(total_mana - min(20,self.base_intellect) - 15*( self.base_intellect - min(20,self.base_intellect)))

    def _print_state(self):
        print("base_intellect: {}".format(self.base_intellect))
        print("base_spirit: {}".format(self.base_spirit))
        print("base_mana: {}".format(self.base_mana))

class Buff:
    def __init__(self):
        self.intellect_bonus = 0
        self.spirit_bonus = 0
        self.pct_max_mana_as_mp5 = 0
        self.max_duration_sec = 0

    def get_intellect_bonus(self,time_elapsed_sec):
        if time_elapsed_sec <= self.max_duration_sec:
            return(self.intellect_bonus)
        else:
            return(0)
        
    def get_spirit_bonus(self,time_elapsed_sec):
        if time_elapsed_sec <= self.max_duration_sec:
            return(self.spirit_bonus)
        else:
            return(0)
        
    def get_pct_max_mana_as_mp5(self,time_elapsed_sec):
        if time_elapsed_sec <= self.max_duration_sec:
            return(self.pct_max_mana_as_mp5)
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
    def __init__(self,name,slot,intellect_bonus=0,spirit_bonus=0,spellpower_bonus=0,mp5_bonus=0,spell_hit_bonus=0):
        self.name = name
        self.slot = slot
        self.intellect_bonus = intellect_bonus
        self.spirit_bonus = spirit_bonus
        self.spellpower_bonus = spellpower_bonus
        self.mp5_bonus = mp5_bonus
        self.spell_hit_bonus = spell_hit_bonus

    def get_intellect_bonus(self):
        return(self.intellect_bonus)

    def get_spirit_bonus(self):
        return(self.spirit_bonus) 

    def get_spellpower_bonus(self):
        return(self.spellpower_bonus) 

    def get_mp5_bonus(self):
        return(self.mp5_bonus)
    
    def get_spell_hit_bonus(self):
        return(self.spell_hit_bonus)

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
        self.total_spell_hit_bonus = 0

        for gear in gear_set:
            self.total_intellect_bonus += gear.get_intellect_bonus()
            self.total_spirit_bonus += gear.get_spirit_bonus()
            self.total_spellpower_bonus += gear.get_spellpower_bonus()
            self.total_mp5_bonus += gear.get_mp5_bonus()
            self.total_spell_hit_bonus += gear.get_spell_hit_bonus()

        return

    def get_total_intellect_bonus(self):
        return(self.total_intellect_bonus)

    def get_total_spirit_bonus(self):
        return(self.total_spirit_bonus) 

    def get_total_spellpower_bonus(self):
        return(self.total_spellpower_bonus)

    def get_total_mp5_bonus(self):
        return(self.total_mp5_bonus)
    
    def get_total_spell_hit_bonus(self):
        return(self.total_spell_hit_bonus)
    
    def get_gear_set_piece_count(self):
        return(self.gear_set_piece_count)
    
    def get_gear_set_name(self):
        return(self.gear_set_name)
    
class Spec:
    def __init__(self,name,spec):
        # includes both talents and runes
        self.name = name
        self.spec = spec # map of talent name to # of points in that talent
        return
    
    def get_name(self):
        return(self.name)
    
    def check(self,talent_name):
        return(talent_name in self.spec)
    
    def get_points(self,talent_name):
        if talent_name in self.spec:
            return(self.spec[talent_name])
        return(0)