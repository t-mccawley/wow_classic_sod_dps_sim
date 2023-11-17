from utils.classes import Race, Buff, GearSet
from typing import List
import random

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
        self.elapsed_ticks = 0 # int, each tick = 0.1s
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
        self.current_cast_time_remaining = 0.0 # number of seconds remaining on cast
        self.current_cast_name = None # name of current cast
        self.current_cast_damage = 0.0 # damage that will land with cast completes
        self.current_cast_mana_cost = 0.0 # mana that will be spent when cast completes
        # cooldowns
        self.remaining_cooldowns = {
            "GCD": 0.0,
            "Flame Shock": 0.0,
            "Lava Burst": 0.0,
            "Ancestral Guidance": 0.0,
            "Shamanistic Rage": 0.0,
        }
        self.cooldowns_max = {
            "GCD": 1.5,
            "Flame Shock": 6.0,
            "Lava Burst": 8.0,
            "Ancestral Guidance": 120.0,
            "Shamanistic Rage": 60.0,
        }
        # personal buffs / debuffs tracking
        self.clear_cast_active = False
        self.water_shield_active = False
        self.water_shield_duration_remaining = 0.0
        self.flame_shock_applied = False
        self.flame_shock_duration_remaining = 0.0
        # data tracking
        self.damage_done_this_tick = 0.0
        self.mana_spent_this_tick = 0.0
        self.timeseries = []
        self.damage_done_timeseries = []
        self.dps_timeseries = []
        self.mana_timeseries = []
        self.cumulative_damage_done = 0.0
        self.spell_cast_count = 0
        self.spell_hit_count = 0
        self.spell_crit_count = 0
        self.overload_count = 0
        self.clear_cast_count = 0
        
    def get_timeseries_data(self):
        return(self.timeseries,self.damage_done_timeseries,self.dps_timeseries,self.mana_timeseries)
   
    def _update_primary_stats(self):
        """Updates primary stats"""
        self.intellect = self.base_intellect + self.gear_set.get_total_intellect_bonus()
        self.spirit = self.base_spirit + self.gear_set.get_total_spirit_bonus()
        for buff in self.buffs:
            self.intellect += buff.get_intellect_bonus(self.elapsed_ticks*0.1)
            self.spirit += buff.get_spirit_bonus(self.elapsed_ticks*0.1)
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

    def _update_cooldowns(self,verbose=False):
        for spell in self.remaining_cooldowns:
            if self.remaining_cooldowns[spell] > 0:
                if verbose:
                    print("{} on cooldown, {:0.2f} s remaining".format(spell,self.remaining_cooldowns[spell]))
                self.remaining_cooldowns[spell] = max(0.0,self.remaining_cooldowns[spell] - 0.1)
            else:
                self.remaining_cooldowns[spell] = 0.0
    
    def _update_current_cast(self,verbose=False):
        if self.casting:
            self.current_cast_time_remaining = max(0.0, self.current_cast_time_remaining - 0.1)
            if verbose:
                print("current cast time remaining {:0.2f} s".format(self.current_cast_time_remaining))
            if self.current_cast_time_remaining <= 0.0:
                # cast complete!
                if verbose:
                    print("{} cast complete!".format(self.current_cast_name))
                # check for Overload
                if ("Overload" in self.spec) and (self.current_cast_damage != 0) and (self.current_cast_name in ["Lightning Bolt","Chain Lightning","Lava Burst"]):
                    if random.rand() < 0.33:
                        # add second bolt of 50% damage
                        self.overload_count += 1
                        self.current_cast_damage *= 1.5
                # record damage and mana
                self.damage_done_this_tick = self.current_cast_damage
                self.mana_spent_this_tick = self.current_cast_mana_cost
                # check for new clearcasting
                if "Elemental Focus" in self.spec and self.current_cast_mana_cost != 0: 
                    if random.random() < 0.1:
                        self.clear_cast_active = True
                        self.clear_cast_count += 1
                # reset cast
                self.casting = False
                self.current_cast_time = 0.0
                self.current_cast_name = None
                self.current_cast_damage = 0.0
                self.current_cast_mana_cost = 0.0
    
    def _update_mana_regen(self,verbose=False):
        if ((self.elapsed_ticks*0.1) % 2.0) == 0.0:
            mana_gain = self.mp5_while_casting * 2 / 5
            if verbose:
                print("mana gain of {}".format(mana_gain))
            self.mana += mana_gain
    
    def _record_data(self):
        # scalars
        self.cumulative_damage_done += self.damage_done_this_tick
        self.mana = max(0.0,self.mana - self.mana_spent_this_tick)
        # timeseries
        self.timeseries.append(self.elapsed_ticks*0.1)
        self.damage_done_timeseries.append(self.cumulative_damage_done)
        dps = 0.0
        if self.elapsed_ticks*0.1 > 0.0:
            dps = self.cumulative_damage_done/self.elapsed_ticks*0.1
        self.dps_timeseries.append(dps)
        self.mana_timeseries.append(self.mana)

    def print_perf_stats(self):
        """Prints performance stats for encounter"""
        print("Performance:")
        print("total damage done: {:0.2f}".format(self.cumulative_damage_done))
        print("elapsed time: {:0.2f} s".format(self.elapsed_ticks*0.1))
        print("dps: {:0.2f}".format(self.cumulative_damage_done/(self.elapsed_ticks*0.1)))
        print()
        print("number of spell casts: {}".format(self.spell_cast_count))
        print("hit chance: {:0.2f} %".format(self.spell_hit_count/self.spell_cast_count*100.0))
        print("crit chance: {:0.2f} %".format(self.spell_crit_count/self.spell_cast_count*100.0))
        print("overload chance: {:0.2f} %".format(self.overload_count/self.spell_cast_count*100.0))
        print("clear cast chance: {:0.2f} %".format(self.clear_cast_count/self.spell_cast_count*100.0))
        print()
        print("ending mana: {}".format(self.mana))

    def print_current_state(self):
        """Prints the current character state"""
        print("Character State:")
        print("\tLevel {} {} Shaman".format(self.level,self.race))
        print("\trotation: {}".format(self.rotation))
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

    def lightning_bolt(self,rank,verbose=False):
        """https://www.wowhead.com/classic/spell=403/lightning-bolt"""
        # constants (maps from rank to value)
        spell_name = "Lightning Bolt"
        BASE_CAST_TIME_MAP = {
            1: 1.5,
            2: 2.0,
            3: 2.5,
            4: 3.0,
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

        if self.remaining_cooldowns["GCD"] <= 0.0 and not self.casting:
            mana_cost = MANA_COST_MAP[rank]
            if self.clear_cast_active:
                mana_cost = 0
                self.clear_cast_active = False # turn off clear casting
            elif "Convection" in self.spec:
                mana_cost *= (1 - 0.02*self.spec["Convection"])

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time
                if "Lightning Mastery" in self.spec:
                    cast_time -= self.spec["Lightning Mastery"]*0.2
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]

                # compute damage
                damage = 0.0
                hit_roll = random.random()
                crit_roll = random.random()
                if hit_roll < self.spell_hit_raid_boss:
                    # hit!
                    self.spell_hit_count += 1
                    if verbose:
                        print("HIT!")
                    base_damage = BASE_DAMAGE_MAP[rank]
                    if "Concussion" in self.spec:
                        base_damage *= self.spec["Concussion"]*0.01
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
                        self.spell_crit_count += 1
                        if verbose:
                            print("CRIT!")
                        if "Elemental Fury" in self.spec:
                            damage *= 2.0
                        else:
                            damage *= 1.5

                self.current_cast_damage = damage
        
        return

    # ROTATIONS
    def rotation_a(self,verbose=False):
        self.lightning_bolt(rank=4,verbose=verbose)
        return
    
    def rotation_b(self,verbose=False):
        self.lightning_bolt(rank=3,verbose=verbose)
        return
    
    def rotation_c(self,verbose=False):
        self.lightning_bolt(rank=2,verbose=verbose)
        return
    
    def rotation_d(self,verbose=False):
        self.lightning_bolt(rank=1,verbose=verbose)
        return
    
    # PRIMARY SIMULATION LOOP
    def time_step(self,verbose=False):
        """take one simulation time step (0.1s)"""
        # take time step and reset data
        self.elapsed_ticks += 1
        self.damage_done_this_tick = 0.0
        self.mana_spent_this_tick = 0.0
        if verbose:
            print("time: {:0.2f} s".format(self.elapsed_ticks*0.1))

        # update stats
        self._update_primary_stats()
        self._update_secondary_stats()

        # update cooldowns
        self._update_cooldowns(verbose=False)

        # update casting
        self._update_current_cast(verbose=False)

        # update mana regen
        self._update_mana_regen()
        
        # perform rotation
        if self.rotation == "A":
            self.rotation_a()
        elif self.rotation == "B":
            self.rotation_b()
        elif self.rotation == "C":
            self.rotation_c()
        elif self.rotation == "D":
            self.rotation_d()

        # record data
        self._record_data()
        
        return(self.elapsed_ticks*0.1)