from config.gear_config import GEAR_SET_LIST
from config.buff_config import BUFFS_LIST
from config.spec_config import SPECS_LIST
from config.encounter_duration_config import ENCOUNTER_DURATION_LIST
from config.rotation_config import ROTATION_LIST
from utils.character import *
import matplotlib.pyplot as plt
import pandas as pd

# SMALL SINGLE TEST
encounter_duration = 5.0
char = Character(
    race="Troll",
    level=25,
    spec=SPECS_LIST[0],
    buffs=BUFFS_LIST[0],
    gear_set=GEAR_SET_LIST[0],
    rotation=ROTATION_LIST[1],
)

# sim
elapsed_time_sec = 0.0
while elapsed_time_sec < encounter_duration:
    elapsed_time_sec = char.time_step(verbose=True)


# # FULL SIM
# results = pd.DataFrame()

# id = 0
# N_SIM_ITERATIONS = 100
# for gear_set in GEAR_SET_LIST:
#     for buffs in BUFFS_LIST:
#         for spec in SPECS_LIST:
#             for rotation in ROTATION_LIST:
#                 for encounter_duration in ENCOUNTER_DURATION_LIST:
#                     dps_sum = 0.0
#                     num_spell_casts_sum = 0
#                     hit_chance_sum = 0.0
#                     crit_chance_sum = 0.0
#                     ending_mana_sum = 0
#                     for n in range(0,N_SIM_ITERATIONS):
#                         char = Character(
#                             race="Troll",
#                             level=25,
#                             spec=spec,
#                             buffs=buffs,
#                             gear_set=gear_set,
#                             rotation=rotation,
#                         )

#                         # sim
#                         elapsed_time_sec = 0.0
#                         while elapsed_time_sec < encounter_duration:
#                             elapsed_time_sec = char.time_step()

#                         # extract data
#                         dps_sum += char.get_dps()
#                         num_spell_casts_sum += char.get_num_spell_casts()
#                         hit_chance_sum += char.get_hit_chance()
#                         crit_chance_sum += char.get_crit_chance()
#                         ending_mana_sum += char.get_ending_mana()

#                     # save results
#                     results.loc[id,'encounter_duration'] = encounter_duration
#                     results.loc[id,'rotation'] = rotation
#                     results.loc[id,'spec'] = spec.get_name()
#                     results.loc[id,'buffs'] = len(buffs)
#                     results.loc[id,'gear_set'] = gear_set.get_gear_set_name()
#                     results.loc[id,'num_spell_casts_avg'] = num_spell_casts_sum/N_SIM_ITERATIONS
#                     results.loc[id,'hit_chance_avg'] = hit_chance_sum/N_SIM_ITERATIONS
#                     results.loc[id,'crit_chance_avg'] = crit_chance_sum/N_SIM_ITERATIONS
#                     results.loc[id,'ending_mana_avg'] = ending_mana_sum/N_SIM_ITERATIONS
#                     results.loc[id,'dps_avg'] = dps_sum/N_SIM_ITERATIONS
                    
#                     id += 1

# print(results.sort_values(['encounter_duration','dps_avg'],ascending=False))

# # timeseries, damage_done_timeseries, dps_timeseries, mana_timeseries = char.get_timeseries_data()

# # plt.plot(timeseries,dps_timeseries,label="dps")
# # plt.plot(timeseries,mana_timeseries,label="mana")
# # plt.legend()
# # plt.show()