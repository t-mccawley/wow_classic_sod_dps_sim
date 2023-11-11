from db.gear import *
from db.enchants import *

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

    def get_total_intellect_bonus(self,gear_set_index):
        return(self.total_intellect_bonus)

    def get_total_spirit_bonus(self,gear_set_index):
        return(self.total_spirit_bonus) 

    def get_total_spellpower_bonus(self,gear_set_index):
        return(self.total_spellpower_bonus)

    def get_total_mp5_bonus(self,gear_set_index):
        return(self.total_mp5_bonus)

class GearSets:
    """container of a list of gear_sets which are lists of Gear"""
    def __init__(self):
        # metadata
        self.total_num_gear_sets = 0
        # data stored in lists (index for each gear set)
        self.gear_sets = [] 

    def append_new_gear_set(self,gear_set):
        self.gear_sets.append(gear_set)
        return(self)

    def get_total_intellect_bonus(self,gear_set_index):
        return(self.total_intellect_bonus[gear_set_index])

    def get_total_spirit_bonus(self,gear_set_index):
        return(self.total_spirit_bonus[gear_set_index]) 

    def get_total_spellpower_bonus(self,gear_set_index):
        return(self.total_spellpower_bonus[gear_set_index])

    def get_total_mp5_bonus(self,gear_set_index):
        return(self.total_mp5_bonus[gear_set_index])

    def print_all_gear_sets_total_stat_bonuses(self):
        for gear_set_index in range(0,self.total_num_gear_sets):
            self.print_gear_set_total_stat_bonuses(gear_set_index)
        return

    def print_gear_set_total_stat_bonuses(self,gear_set_index):
        print("{} (idx: {})".format(self.gear_set_names[gear_set_index],gear_set_index))
        print("\tgear_set_piece_count: {}".format(self.gear_set_piece_count[gear_set_index]))
        print("\ttotal_intellect_bonus: {}".format(self.get_total_intellect_bonus(gear_set_index)))
        print("\ttotal_spirit_bonus: {}".format(self.get_total_spirit_bonus(gear_set_index)))
        print("\ttotal_spellpower_bonus: {}".format(self.get_total_spellpower_bonus(gear_set_index)))
        print("\ttotal_mp5_bonus: {}".format(self.get_total_mp5_bonus(gear_set_index)))
        return

pre_bis_lvl_25_classic = [
    spellpower_goggles_xtreme.enchant(arcanum_of_focus_head),
    glowing_green_talisman,
    magicians_mantle,
    soft_willow_cape,
    robes_of_arugal.enchant(greater_stats_chest),
    fingerbone_bracers.enchant(greater_intellect_bracer),
    crested_scepter.enchant(spell_power_weapon),
    seedcloud_buckler.enchant(greater_spirit_shield),
    shredder_operating_gloves,
    belt_of_arugal,
    azure_silk_pants,
    tundra_boots,
    snake_hoop,
    lavishly_jeweled_ring,
]

GEAR_SETS = GearSets()
GEAR_SETS.append_new_gear_set(
    gear_set=pre_bis_lvl_25_classic,
    name="Pre-BiS Lvl 25 (Classic)",
)
