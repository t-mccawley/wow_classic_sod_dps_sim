from utils.classes import Race, Buff, GearSet, Spec
from typing import List
import random
import math

class Character(Race):
    """High level class to define a character"""
    def __init__(
            self,
            race: str,
            level: int,
            spec: Spec,
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
        self.current_cast_spell_name = None # name of current cast
        self.current_cast_damage = 0.0 # damage that will land with cast completes
        self.current_cast_mana_cost = 0.0 # mana that will be spent when cast completes
        # cooldowns
        self.on_cooldown = {
            "GCD": False,
            "Flame Shock": False,
            "Lava Burst": False,
            "Ancestral Guidance": False,
            "Shamanistic Rage": False,
        }
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
        # short buffs
        self.short_buff_active = {
            "Elemental Focus": False,
            "Flame Shock": False,
            "Ancestral Guidance": False,
            "Shamanistic Rage": False,
        }
        self.short_buff_remaining = {
            "Elemental Focus": 0.0,
            "Flame Shock": 0.0,
            "Ancestral Guidance": 0.0,
            "Shamanistic Rage": 0.0,
        }
        self.short_buff_max_duration = {
            "Elemental Focus": float('inf'),
            "Flame Shock": 12.0,
            "Ancestral Guidance": 10.0,
            "Shamanistic Rage": 15.0,
        }
        # dot tracking
        self.dot_active = {
            "Flame Shock": False,
        }
        self.dot_tick_damage = {
            "Flame Shock": 0.0,
        }
        self.dot_tick_frequency = { # seconds between each tick of damage
            "Flame Shock": 3.0,
        }
        self.dot_remaining_duration = {
            "Flame Shock": 0.0
        }
        self.dot_max_duration = {
            "Flame Shock": 12.0,
        }
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
        self.max_mana *= (1 + 0.01*self.spec.get_points("Ancestral Knowledge"))
        self.spell_crit_chance = 0.05 + (self.intellect / 59.5) / 100
        self.spellpower = self.gear_set.get_total_spellpower_bonus()
        self.mp5_while_casting = self.gear_set.get_total_mp5_bonus()
        self.mp5_while_not_casting = self.mp5_while_casting + (self.spirit/5 + 17)/2*5
        self.spell_hit_raid_boss = min(0.99, 0.83 + self.gear_set.get_total_spell_hit_bonus())

    def _update_cooldowns(self,verbose=False):
        for spell in self.remaining_cooldowns:
            if self.remaining_cooldowns[spell] > 0.1:
                if verbose:
                    print("{} on cooldown, {:0.2f} s remaining".format(spell,self.remaining_cooldowns[spell]))
                self.remaining_cooldowns[spell] -= 0.1
            else:
                self.remaining_cooldowns[spell] = 0.0
                self.on_cooldown[spell] = False
    
    def _update_current_cast(self,verbose=False):
        if self.casting:
            self.current_cast_time_remaining -= 0.1
            if verbose:
                print("current cast time remaining {:0.2f} s".format(self.current_cast_time_remaining))
            if self.current_cast_time_remaining <= 0.0:
                # cast complete!
                if verbose:
                    print("{} cast complete!".format(self.current_cast_spell_name))
                # check for Overload
                if (self.spec.check("Overload")) and (self.current_cast_damage != 0) and (self.current_cast_spell_name in ["Lightning Bolt","Chain Lightning","Lava Burst"]):
                    if random.random() < 0.33:
                        # add second bolt of 50% damage
                        self.overload_count += 1
                        self.current_cast_damage *= 1.5
                # perform cast action
                # record damage and mana (all spells, can be zero)
                self.damage_done_this_tick = self.current_cast_damage
                self.mana_spent_this_tick = self.current_cast_mana_cost
                # activate buff if any
                if self.current_cast_spell_name in self.short_buff_active:
                    self.short_buff_active[self.current_cast_spell_name] = True
                    self.short_buff_remaining[self.current_cast_spell_name] = self.short_buff_max_duration[self.current_cast_spell_name]
                # check for new clearcasting
                if self.spec.check("Elemental Focus") and self.current_cast_mana_cost != 0: 
                    if random.random() < 0.1:
                        self.short_buff_active["Elemental Focus"] = True
                        self.clear_cast_count += 1
                # put spell on CD if it has one
                if self.current_cast_spell_name in self.on_cooldown:
                    self.remaining_cooldowns[self.current_cast_spell_name] = self.cooldowns_max[self.current_cast_spell_name]
                    self.on_cooldown[self.current_cast_spell_name] = True
                # reset cast
                self.casting = False
                self.current_cast_time = 0.0
                self.current_cast_spell_name = None
                self.current_cast_damage = 0.0
                self.current_cast_mana_cost = 0.0
    
    def _update_mana_regen(self,verbose=False):
        if ((self.elapsed_ticks*0.1) % 2.0) == 0.0:
            mana_gain = self.mp5_while_casting * 2 / 5
            if verbose:
                print("mana gain of {}".format(mana_gain))
            self.mana += mana_gain
    
    def _update_dots(self,verbose=False):
        for dot in self.dot_active:
            self.dot_remaining_duration[dot] -= 0.1
            if self.dot_active[dot] and self.dot_remaining_duration[dot] < 0.0:
                # reset
                self.dot_active[dot] = False
                self.dot_remaining_duration[dot] = 0.0
                self.dot_tick_damage[dot] = 0.0
            elif self.dot_active[dot] and ((self.dot_remaining_duration[dot] % self.dot_tick_frequency[dot]) == 0.0):
                # tick damage
                self.damage_done_this_tick += self.dot_tick_damage[dot]

        return

    def _record_data(self,verbose=False):
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

        return

    def get_dps(self):
        return(0.0 if self.elapsed_ticks == 0 else self.cumulative_damage_done/(self.elapsed_ticks*0.1))
    
    def get_num_spell_casts(self):
        return(self.spell_cast_count)
    
    def get_hit_chance(self):
        return(0.0 if self.spell_cast_count == 0 else self.spell_hit_count/self.spell_cast_count)
    
    def get_crit_chance(self):
        return(0.0 if self.spell_cast_count == 0 else self.spell_crit_count/self.spell_cast_count)
    
    def get_ending_mana(self):
        return(self.mana_timeseries[len(self.mana_timeseries) - 1])
    
    def print_perf_stats(self):
        """Prints performance stats for encounter"""
        print("Performance:")
        print("total damage done: {:0.2f}".format(self.cumulative_damage_done))
        print("elapsed time: {:0.2f} s".format(self.elapsed_ticks*0.1))
        print("dps: {:0.2f}".format(self.get_dps()))
        print()
        print("number of spell casts: {}".format(self.get_num_spell_casts()))
        print("hit chance: {:0.2f} %".format(self.get_hit_chance()*100))
        print("crit chance: {:0.2f} %".format(self.get_crit_chance()*100.0))
        print("overload chance: {:0.2f} %".format(self.overload_count/self.spell_cast_count*100.0))
        print("clear cast chance: {:0.2f} %".format(self.clear_cast_count/self.spell_cast_count*100.0))
        print()
        print("ending mana: {}".format(self.get_ending_mana()))

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

        if not self.on_cooldown["GCD"] and not self.casting:
            mana_cost = MANA_COST_MAP[rank]*(1 - 0.02*self.spec.get_points("Convection"))
            if self.short_buff_active["Elemental Focus"]:
                mana_cost = 0
                self.short_buff_active["Elemental Focus"] = False # turn off clear casting

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time - self.spec.get_points("Lightning Mastery")*0.2
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_spell_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]
                self.on_cooldown["GCD"] = True

                # compute damage
                damage = 0.0
                hit_roll = random.random()
                crit_roll = random.random()
                if hit_roll < self.spell_hit_raid_boss:
                    # hit!
                    self.spell_hit_count += 1
                    if verbose:
                        print("HIT!")
                    base_damage = BASE_DAMAGE_MAP[rank]*(1 + self.spec.get_points("Concussion")*0.01)
                    spc = max(min(base_cast_time,3.5),1.5) / 3.5
                    spc_penalty = 1 - (20 - min(20,LEARNED_LEVEL_MAP[rank]))*0.0375
                    damage = base_damage + (spc * spc_penalty * self.spellpower)
                    crit_chance = self.spell_crit_chance + self.spec.get_points("Call of Thunder")*0.01 + self.spec.get_points("Tiday Mastery")*0.01
                    if self.spec.get_points("Call of Thunder") == 5:
                        crit_chance += 0.01 # additional 1% for 5th talent point...
                    if crit_roll < crit_chance:
                        # crit!
                        self.spell_crit_count += 1
                        if verbose:
                            print("CRIT!")
                        if self.spec.check("Elemental Fury"):
                            damage *= 2.0
                        else:
                            damage *= 1.5

                self.current_cast_damage = damage

                if verbose:
                    print("When {} cast is complete, it will do {:0.2f} damage for {} mana.".format(spell_name,damage,mana_cost))
        
        return
    
    def lava_burst(self,rank,verbose=False):
        """https://www.wowhead.com/classic/spell=408491/lava-burst"""
        # constants (maps from rank to value)
        spell_name = "Lava Burst"
        BASE_CAST_TIME_MAP = {
            1: 2.0,
        }
        MANA_COST_PCT_OF_BASE_MAP = {
            1: 0.1,
        }
        BASE_DAMAGE_MAP = {
            1: 227,
        }
        LEARNED_LEVEL_MAP = {
            1 : 1,
        }

        if self.spec.check(spell_name) and not self.on_cooldown[spell_name] and not self.on_cooldown["GCD"] and not self.casting:
            mana_cost = MANA_COST_PCT_OF_BASE_MAP[rank]*(self.base_mana + self.base_intellect*15)
            if self.short_buff_active["Elemental Focus"]:
                mana_cost = 0
                self.short_buff_active["Elemental Focus"] = False # turn off clear casting

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_spell_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]
                self.on_cooldown["GCD"] = True

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
                    spc = max(min(base_cast_time,3.5),1.5) / 3.5
                    spc_penalty = 1 - (20 - min(20,LEARNED_LEVEL_MAP[rank]))*0.0375
                    damage = base_damage + (spc * spc_penalty * self.spellpower)
                    crit_chance = self.spell_crit_chance
                    if self.short_buff_active["Flame Shock"]:
                        crit_chance = 1.0 # Flame Shock causes guaranteed crit
                    if crit_roll < crit_chance:
                        # crit!
                        self.spell_crit_count += 1
                        if verbose:
                            print("CRIT!")
                        if self.spec.check("Elemental Fury"):
                            damage *= 2.0
                        else:
                            damage *= 1.5

                self.current_cast_damage = damage

                if verbose:
                    print("When {} cast is complete, it will do {:0.2f} damage for {} mana.".format(spell_name,damage,mana_cost))
        
        return
    
    def flame_shock(self,rank,verbose=False):
        """https://www.wowhead.com/classic/spell=8050/flame-shock"""
        # constants (maps from rank to value)
        spell_name = "Flame Shock"
        BASE_CAST_TIME_MAP = {
            1: 0.0,
            2: 0.0,
        }
        DOT_DURATION = {
            1: 12,
            2: 12,
        }
        NUMBER_OF_TICKS = {
            1: 4,
            2: 4,
        }
        MANA_COST_MAP = {
            1: 55,
            2: 95,
        }
        BASE_DIRECT_DAMAGE_MAP = {
            1: 25.0,
            2: 51.0,
        }
        BASE_DOT_DAMAGE_MAP = {
            1: 28.0,
            2: 48.0,
        }
        LEARNED_LEVEL_MAP = {
            1 : 10,
            2 : 18,
        }

        if not self.on_cooldown[spell_name] and not self.on_cooldown["GCD"] and not self.casting:
            mana_cost = MANA_COST_MAP[rank]*(1 - 0.02*self.spec.get_points("Convection"))
            if self.short_buff_active["Elemental Focus"]:
                mana_cost = 0
                self.short_buff_active["Elemental Focus"] = False # turn off clear casting

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time
                dot_duration = DOT_DURATION[rank]
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_spell_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]
                self.on_cooldown["GCD"] = True

                # compute damage
                direct_damage = 0.0
                hit_roll = random.random()
                crit_roll = random.random()
                if hit_roll < self.spell_hit_raid_boss:
                    # hit!
                    self.spell_hit_count += 1
                    if verbose:
                        print("HIT!")
                    base_direct_damage = BASE_DIRECT_DAMAGE_MAP[rank]*(1 + self.spec.get_points("Concussion")*0.01)
                    base_dot_damage = BASE_DOT_DAMAGE_MAP[rank]*(1 + self.spec.get_points("Concussion")*0.01)
                    spc_cast = max(min(base_cast_time,3.5),1.5) / 3.5
                    spc_dur = min(dot_duration,15.0) / 15.0
                    spc_direct = math.pow(spc_cast,2) / (spc_cast + spc_dur)
                    spc_dot = math.pow(spc_dur,2) / (spc_cast + spc_dur)
                    spc_penalty = 1 - (20 - min(20,LEARNED_LEVEL_MAP[rank]))*0.0375
                    direct_damage = base_direct_damage + (spc_direct * spc_penalty * self.spellpower)
                    dot_damage_per_tick = (base_dot_damage + (spc_dot * spc_penalty * self.spellpower)) / NUMBER_OF_TICKS[rank]
                    crit_chance = self.spell_crit_chance
                    if crit_roll < crit_chance:
                        # crit!
                        self.spell_crit_count += 1
                        if verbose:
                            print("CRIT!")
                        if self.spec.check("Elemental Fury"):
                            direct_damage *= 2.0
                        else:
                            direct_damage *= 1.5

                self.current_cast_damage = direct_damage
                self.dot_tick_damage[spell_name] = dot_damage_per_tick

                if verbose:
                    print("When {} cast is complete, it will do {:0.2f} direct damage and {:0.2f} dot damage for {} mana.".format(spell_name,direct_damage,dot_damage_per_tick,mana_cost))
        
        return
    
    def ancestral_guidance(self,rank,verbose=False):
        """https://www.wowhead.com/classic/spell=409337/ancestral-guidance"""
        # constants (maps from rank to value)
        spell_name = "Ancestral Guidance"
        BASE_CAST_TIME_MAP = {
            1: 0.0,
        }
        MANA_COST_MAP = {
            1: 0,
        }

        if self.spec.check(spell_name) and not self.on_cooldown["GCD"] and not self.casting and not self.on_cooldown[spell_name]:
            mana_cost = MANA_COST_MAP[rank]

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_spell_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]
                self.on_cooldown["GCD"] = True
        
        return
    
    def shamanistic_rage(self,rank,verbose=False):
        """https://www.wowhead.com/classic/spell=425336/shamanistic-rage"""
        # constants (maps from rank to value)
        spell_name = "Shamanistic Rage"
        BASE_CAST_TIME_MAP = {
            1: 0.0,
        }
        MANA_COST_MAP = {
            1: 0,
        }

        if self.spec.check(spell_name) and not self.on_cooldown["GCD"] and not self.casting and not self.on_cooldown[spell_name]:
            mana_cost = MANA_COST_MAP[rank]

            if mana_cost <= self.mana:
                base_cast_time = BASE_CAST_TIME_MAP[rank]
                cast_time = base_cast_time
                
                if verbose:
                    print("casting {} (Rank {})!".format(spell_name,rank))
                
                # begin casting spell
                self.spell_cast_count += 1
                self.casting = True
                self.current_cast_time_remaining = cast_time
                self.current_cast_spell_name = spell_name
                self.current_cast_mana_cost = mana_cost
                # start GCD
                self.remaining_cooldowns["GCD"] = self.cooldowns_max["GCD"]
                self.on_cooldown["GCD"] = True
        
        return

    #TODO:
    # make spells for healing wave, flame shock
    # update the primary / secondary stats to consider shamanistic rage
    # test on single encounter
    
    # ROTATIONS
    def kitchen_sink_rotation(self,lightning_bolt_rank,verbose=False):
        # if self.spec.check("Ancestral Guidance") and not self.on_cooldown["Ancestral Guidance"]:
        #     self.ancestral_guidance(rank=1,verbose=verbose)
        # elif self.short_buff_active["Ancestral Guidance"]:
        #     self.healing_wave(rank=4,verbose=verbose)
        # elif self.spec.check("Shamanistic Rage") and not self.on_cooldown["Shamanistic Rage"]:
        #     self.shamanistic_rage(rank=1,verbose=verbose)
        if not self.short_buff_active["Flame Shock"] and not self.on_cooldown["Flame Shock"]:
            self.flame_shock(rank=2,verbose=verbose)
        elif self.spec.check("Lava Burst") and not self.on_cooldown["Lava Burst"]:
            self.lava_burst(rank=1,verbose=verbose)
        else:
            self.lightning_bolt(rank=lightning_bolt_rank,verbose=verbose)
        return

    def rotation_a(self,verbose=False):
        self.lightning_bolt(rank=4,verbose=verbose)
        return
    
    def rotation_b(self,verbose=False):
        self.kitchen_sink_rotation(lightning_bolt_rank=4,verbose=verbose)
        return
    
    def rotation_c(self,verbose=False):
        self.kitchen_sink_rotation(lightning_bolt_rank=3,verbose=verbose)
        return
    
    def rotation_d(self,verbose=False):
        self.kitchen_sink_rotation(lightning_bolt_rank=2,verbose=verbose)
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
        self._update_cooldowns(verbose=verbose)

        # update casting
        self._update_current_cast(verbose=verbose)

        # apply dots
        self._update_dots(verbose=verbose)

        # update mana regen
        self._update_mana_regen()
        
        # perform rotation
        # TODO: "Kitchen Sink Max Rank",
        if self.rotation == "LB R4":
            self.rotation_a(verbose=verbose)
        elif self.rotation == "KS LB R4":
            self.rotation_b(verbose=verbose)
        elif self.rotation == "KS LB R3":
            self.rotation_c(verbose=verbose)
        elif self.rotation == "KS LB R2":
            self.rotation_d(verbose=verbose)

        # record data
        self._record_data(verbose=verbose)
        
        return(self.elapsed_ticks*0.1)