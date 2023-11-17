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
from utils.constants import *

char = Character(
    race="Troll",
    level=25,
    spec=None,
    # buffs=[],
    buffs=BUFFS_LIST[0],
    # gear_set = GearSet([],"Empty"),
    gear_set=GEAR_SET_LIST[0],
    rotation=None
)

char.print_current_state()

char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()
char.time_step()