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

from config.gear_sets import GEAR_SETS_LIST
# print(GEAR_SETS_LIST)
for gear_set in GEAR_SETS_LIST:
    # print(gear_set)
    for gear in gear_set:
        # print(gear)
        gear.print_stat_bonuses()