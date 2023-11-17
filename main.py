SIM_DELTA_T = 0.1 # time step of sim, in seconds

# simulate

# for each encounter
# for each spec
# for each buff profile
# for each gear set
# for each rotation
# instantiate simulation
# execute simulation

# from utils.character import Character
# from config.buffs import BUFFS_LIST

# char = Character(race="Orc",spec=None,buffs=BUFFS_LIST[0],gear_set=None,rotation=None)

# char.print_current_state()

from config.gear_config import GEAR_SET_LIST
from config.buff_config import BUFFS_LIST
from config.spec_config import SPECS_LIST
from utils.character import *
import matplotlib.pyplot as plt


for rotation in ["A","B","C","D"]:
    char = Character(
        race="Troll",
        level=25,
        spec=SPECS_LIST[0],
        # buffs=[],
        buffs=BUFFS_LIST[0],
        # gear_set = GearSet([],"Empty"),
        gear_set=GEAR_SET_LIST[0],
        rotation=rotation,
    )
    char.print_current_state()
    
    elapsed_time_sec = 0.0
    while elapsed_time_sec < 100.0:
        elapsed_time_sec = char.time_step()

    char.print_perf_stats()

# timeseries, damage_done_timeseries, dps_timeseries, mana_timeseries = char.get_timeseries_data()

# plt.plot(timeseries,dps_timeseries,label="dps")
# plt.plot(timeseries,mana_timeseries,label="mana")
# plt.legend()
# plt.show()