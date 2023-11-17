from db.gear import *
from db.enchants import *
from utils.constants import GearSet

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
    azure_silk_pants.enchant(arcanum_of_focus_legs),
    tundra_boots,
    snake_hoop,
    lavishly_jeweled_ring,
]

GEAR_SET_LIST = [
    GearSet(
    gear_set=pre_bis_lvl_25_classic,
    name="Pre-BiS Lvl 25 (Classic)",
    ),
]
