from config.gear_config import GEAR_SET_LIST
from config.buff_config import BUFFS_LIST
from config.spec_config import SPECS_LIST
from config.encounter_duration_config import ENCOUNTER_DURATION_LIST
from config.rotation_config import ROTATION_LIST
from utils.character import *
from db.buffs import *
from utils.classes import Buff
import matplotlib.pyplot as plt
import pandas as pd

# # SMALL SINGLE TEST
# encounter_duration = 5.0
# char = Character(
#     race="Troll",
#     level=25,
#     spec=SPECS_LIST[0],
#     buffs=BUFFS_LIST[0],
#     gear_set=GEAR_SET_LIST[0],
#     rotation=ROTATION_LIST[1],
# )

# # sim
# elapsed_time_sec = 0.0
# while elapsed_time_sec < encounter_duration:
#     elapsed_time_sec = char.time_step(verbose=True)


# FULL SIM
results = pd.DataFrame()
pd.set_option("display.max_columns",None)

id = 0
N_SIM_ITERATIONS = 100
for gear_set in GEAR_SET_LIST:
    for buffs in BUFFS_LIST:
        for spec in SPECS_LIST:
            for rotation in ROTATION_LIST:
                for encounter_duration in [120.0]:
                    dps_sum = 0.0
                    num_spell_casts_sum = 0
                    hit_chance_sum = 0.0
                    crit_chance_sum = 0.0
                    ending_mana_sum = 0
                    for n in range(0,N_SIM_ITERATIONS):
                        char = Character(
                            race="Troll",
                            level=25,
                            spec=spec,
                            buffs=buffs,
                            gear_set=gear_set,
                            rotation=rotation,
                        )

                        # sim
                        elapsed_time_sec = 0.0
                        while elapsed_time_sec < encounter_duration:
                            elapsed_time_sec = char.time_step()

                        # extract data
                        dps_sum += char.get_dps()
                        num_spell_casts_sum += char.get_num_spell_casts()
                        hit_chance_sum += char.get_hit_chance()
                        crit_chance_sum += char.get_crit_chance()
                        ending_mana_sum += char.get_ending_mana()

                    # save results
                    results.loc[id,"id"] = id
                    results.loc[id,'encounter_duration'] = encounter_duration
                    results.loc[id,'rotation'] = rotation
                    results.loc[id,'spec'] = spec.get_name()
                    results.loc[id,'buffs'] = len(buffs)
                    results.loc[id,'gear_set'] = gear_set.get_gear_set_name()
                    results.loc[id,'num_spell_casts_avg'] = num_spell_casts_sum/N_SIM_ITERATIONS
                    results.loc[id,'hit_chance_avg'] = hit_chance_sum/N_SIM_ITERATIONS
                    results.loc[id,'crit_chance_avg'] = crit_chance_sum/N_SIM_ITERATIONS
                    results.loc[id,'ending_mana_avg'] = ending_mana_sum/N_SIM_ITERATIONS
                    results.loc[id,'dps_avg'] = dps_sum/N_SIM_ITERATIONS
                    
                    id += 1

results = results.set_index("id")
results = results.sort_values(['encounter_duration','dps_avg'],ascending=False)
results.to_csv("./outputs/main_sim_output.csv")

# identify best
idx_best = results['dps_avg'].idxmax(axis=0)
print("***** BEST ******")
print(results.loc[idx_best,:])
print()

# get actual objects of best
top_dps = results.loc[idx_best,'dps_avg']
encounter_duration_best = results.loc[idx_best,'encounter_duration']
for gear_set in GEAR_SET_LIST:
    if gear_set.get_gear_set_name() == results.loc[idx_best,'gear_set']:
        best_gear_set = gear_set
for buffs in BUFFS_LIST:
    if len(buffs) == results.loc[idx_best,'buffs']: # TODO make better
        best_buffs = buffs
for spec in SPECS_LIST:
    if spec.get_name() == results.loc[idx_best,'spec']:
        best_spec = spec
best_rotation = results.loc[idx_best,'rotation']

# do stat sensitivity analysis
PURE_STAT_BUFFS = [
    PureIntellect(name="Intellect"),
    PureSpirit(name="Spirit"),
    PureSpellPower(name="Spell Power"),
    PureSpellCrit(name="Spell Crit"),
    PureSpellHit(name="Spell Hit"),
    PureMp5Bonus(name="Mp5"),
]
stat_results = pd.DataFrame()
id = 0
for pure_stat_buff in PURE_STAT_BUFFS:
    buffs = best_buffs + [pure_stat_buff]
    for rotation in ROTATION_LIST: # iterate over rotations to check for possible up-ranking
        dps_sum = 0.0
        num_spell_casts_sum = 0
        hit_chance_sum = 0.0
        crit_chance_sum = 0.0
        ending_mana_sum = 0
        for n in range(0,N_SIM_ITERATIONS):
            char = Character(
                race="Troll",
                level=25,
                spec=best_spec,
                buffs=buffs,
                gear_set=best_gear_set,
                rotation=rotation,
            )

            # sim
            elapsed_time_sec = 0.0
            while elapsed_time_sec < encounter_duration:
                elapsed_time_sec = char.time_step()

            # extract data
            dps_sum += char.get_dps()
            num_spell_casts_sum += char.get_num_spell_casts()
            hit_chance_sum += char.get_hit_chance()
            crit_chance_sum += char.get_crit_chance()
            ending_mana_sum += char.get_ending_mana()

        # save results
        stat_results.loc[id,"id"] = id
        stat_results.loc[id,'encounter_duration'] = encounter_duration
        stat_results.loc[id,'rotation'] = rotation
        stat_results.loc[id,'spec'] = spec.get_name()
        stat_results.loc[id,'buffs'] = pure_stat_buff.get_buff_name()
        stat_results.loc[id,'gear_set'] = gear_set.get_gear_set_name()
        stat_results.loc[id,'num_spell_casts_avg'] = num_spell_casts_sum/N_SIM_ITERATIONS
        stat_results.loc[id,'hit_chance_avg'] = hit_chance_sum/N_SIM_ITERATIONS
        stat_results.loc[id,'crit_chance_avg'] = crit_chance_sum/N_SIM_ITERATIONS
        stat_results.loc[id,'ending_mana_avg'] = ending_mana_sum/N_SIM_ITERATIONS
        stat_results.loc[id,'dps_avg'] = dps_sum/N_SIM_ITERATIONS
        stat_results.loc[id,'dps_avg_change'] = dps_sum/N_SIM_ITERATIONS - top_dps

        id += 1

stat_results = stat_results.set_index("id")
stat_results = stat_results.sort_values(['encounter_duration','dps_avg'],ascending=False)
stat_results.to_csv("./outputs/stat_sim_output.csv")

stat_prio = pd.DataFrame()
for stat in stat_results['buffs'].unique():
    idxs = (stat_results['buffs'] == stat)
    # divide by 10 to get value for 1 of each stat
    stat_prio.loc[stat,'weight'] = stat_results.loc[idxs,'dps_avg_change'].max()/10

print(stat_prio)

stat_prio.to_csv("./outputs/stat_prio.csv")