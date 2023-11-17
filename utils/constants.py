from enum import Enum
from typing import List
import random

# constants
GCD = 1.5 #s

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
    
class Character(Race):
    """High level class to define a character"""
    def __init__(
            self,
            race: str,
            level: int,
            spec: map, # from name of talent to number of points
            buffs: List[Buff],
            gear_set: GearSet,
            rotation: str,
        ):
        super().__init__(race,level)
        # metadata
        self.time_elapsed_sec = -0.1 # start negative so first step is 0.0
        self.spec = spec
        self.gear_set = gear_set # list gear
        self.buffs = buffs # list of buffs
        self.rotation = rotation
        # update primary stats
        self._update_primary_stats()
        # update secondary stats
        self._update_secondary_stats()
        # character state
        self.mana = self.max_mana
        self.casting = False # boolean indicating if actively casting 
        self.current_cast_time = None # number of seconds into a cast
        self.current_cast_max = None # number of seconds that the current cast will take
        self.current_cast_name = None # name of current cast
        self.current_cast_damage = None # damage that will land with cast completes
        self.current_cast_mana_cost = None # mana that will be spent when cast completes
        self.gcd = False # boolean indicating if actively on GCD
        self.gcd_time = None # number of seconds into the GCD
        # cooldowns
        # data tracking
        self.timeseries = []
        self.damage_done_timeseries = []
        self.dps_timeseries = []
        self.mana_timeseries = []
        self.cumulative_damage_done = 0.0

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
        if "Ancestral Knowledge" in self.spec:
            self.max_mana *= (1 + 0.01*self.spec["Ancestral Knowledge"])
        self.spell_crit_chance = 0.05 + (self.intellect / 59.5) / 100
        self.spellpower = self.gear_set.get_total_spellpower_bonus()
        self.mp5_while_casting = self.gear_set.get_total_mp5_bonus()
        self.mp5_while_not_casting = self.mp5_while_casting + (self.spirit/5 + 17)/2*5
        self.spell_hit_raid_boss = min(0.99, 0.83 + self.gear_set.get_total_spell_hit_bonus())
    
    def print_current_state(self):
        """Prints the current character state"""
        print("Character State:")
        print("\tLevel {} {} Shaman".format(self.level,self.race))
        print("\tbuff count: {}".format(len(self.buffs)))
        print("\tgear count: {}".format(self.gear_set.get_gear_set_piece_count()))
        print("\tintellect: {}".format(self.intellect))
        print("\tspirit: {}".format(self.spirit))
        print("\tmax_mana: {}".format(self.max_mana))
        print("\tmana: {}".format(self.mana))
        print("\tspell_hit_raid_boss: {:0.2f} %".format(self.spell_hit_raid_boss*100.0))
        print("\tspell_crit_chance: {:0.2f} %".format(self.spell_crit_chance*100.0))
        print("\tspellpower: {}".format(self.spellpower))
        print("\tmp5_while_casting: {}".format(self.mp5_while_casting))
        print("\tmp5_while_not_casting: {}".format(self.mp5_while_not_casting))
   
    # DEFINE SPELLS
    # spell power coefficients: https://www.reddit.com/r/classicwow/comments/95abc8/list_of_spellcoefficients_1121/

    def lightning_bolt(self,rank):
        """https://www.wowhead.com/classic/spell=403/lightning-bolt"""
        # constants (maps from rank to value)
        BASE_CAST_TIME_MAP = {
            1: 1.5,
            2: 2.0,
            3: 2.5,
            4: 3.0,
        }
        NAME_MAP = {
            1: "Lightning Bold (Rank 1)",
            2: "Lightning Bold (Rank 2)",
            3: "Lightning Bold (Rank 3)",
            4: "Lightning Bold (Rank 4)",
        }
        MANA_COST_MAP = {
            1: 15,
            2: 30,
            3: 45,
            4: 75,
        }
        BASE_DAMAGE_MAP = {
            1: 16.0,
            2: 30.5,
            3: 52.5,
            4: 94.0,
        }
        LEARNED_LEVEL_MAP = {
            1 : 1,
            2 : 8,
            3: 14,
            4: 20,
        }

        if not self.gcd and not self.casting:
            mana_cost = MANA_COST_MAP[rank]
            if "Convection" in self.spec:
                mana_cost *= (1 - 0.02*self.spec["Convection"])
            if mana_cost <= self.mana:
                name = NAME_MAP[rank]
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                if "Lightning Mastery" in self.spec:
                    base_cast_time -= self.spec["Lightning Mastery"]*0.2

                print("casting {} !".format(name))
                # compute spell damage and mana
                self.casting = True
                self.current_cast_time = 0.0
                self.current_cast_max = base_cast_time # todo modify with talents
                self.current_cast_name = name
                self.current_cast_mana_cost = mana_cost

                # compute damage
                damage = 0.0
                hit_roll = random.random()
                crit_roll = random.random()
                if hit_roll < self.spell_hit_raid_boss:
                    # hit!
                    base_damage = BASE_DAMAGE_MAP[rank]
                    if "Concussion" in self.spec:
                        base_damage *= self.spec["Concussion"]*0.01
                    print("HIT!")
                    spc = max(min(base_cast_time,3.5),1.5) / 3.5
                    spc_penalty = 1 - (20 - min(20,LEARNED_LEVEL_MAP[rank]))*0.0375
                    damage = base_damage + (spc * spc_penalty * self.spellpower)
                    crit_chance = self.spell_crit_chance
                    if "Call of Thunder" in self.spec:
                        if self.spec["Call of Thunder"] <= 4:
                            crit_chance += self.spec["Call of Thunder"]*0.01
                        else:
                            crit_chance += 0.06
                    if "Tidal Mastery" in self.spec:
                        crit_chance += self.spec["Tiday Mastery"]*0.01
                    if crit_roll < crit_chance:
                        # crit!
                        print("CRIT!")
                        if "Elemental Fury" in self.spec:
                            damage *= 2.0
                        else:
                            damage *= 1.5

                self.current_cast_damage = damage
        
        return

    # PRIMARY SIMULATION LOOP
    def time_step(self):
        """take one simulation time step (0.1s)"""
        # take time step
        self.time_elapsed_sec += 0.1
        self.timeseries.append(self.time_elapsed_sec)
        print("starting time step at elapsed time {:0.2f} s".format(self.time_elapsed_sec))

        # update stats
        self._update_primary_stats()
        self._update_secondary_stats()

        # check gcd
        if self.gcd:
            self.gcd_time += 0.1
            print("GCD time {:0.2f} s".format(self.gcd_time))
            if self.gcd_time >= 1.5:
                # reset
                self.gcd = False
                self.gcd_time = None

        
        # check other CDs

        # check casting
        if self.casting:
            self.current_cast_time += 0.1
            print("current cast time {:0.2f} s".format(self.current_cast_time))
            if self.current_cast_time >= self.current_cast_max:
                # cast complete!
                # check if clearcasting already active
                mana_cost = self.current_cast_mana_cost
                if self.clear_cast_active:
                    mana_cost = 0
                    self.clear_cast_active = False
                # check for Overload
                if ("Overload" in self.spec) and (self.current_cast_damage != 0) and ("Lightning Bolt" in self.current_cast_name or "Chain Lightning" in self.current_cast_name or "Lava Burst" in self.current_cast_name):
                    if random.rand() < 0.33:
                        # add second bolt of 50% damage
                        self.current_cast_damage *= 1.5
                # record damage and mana
                # TODO use new structures
                self.cumulative_damage_done += self.current_cast_damage
                self.damage_done_timeseries.append(self.cumulative_damage_done)
                self.dps_timeseries.append(self.cumulative_damage_done / self.time_elapsed_sec)
                self.mana -= mana_cost
                self.mana_timeseries.append(self.mana)
                # check for new clearcasting
                if "Elemental Focus" in self.spec and mana_cost != 0: 
                    if random.random() < 0.1:
                        self.clear_cast_active = True
                # reset
                self.casting = False
                self.current_cast_time = None
                self.current_cast_max = None
                self.current_cast_name = None
                self.current_cast_damage = None
                self.current_cast_mana_cost = None
                self.gcd = True
                self.gcd_time = 0.0


        # perform rotation
        # XXX
        self.lightning_bolt_r1()
        # XXX
        
        # check for mana regen
        
        return
