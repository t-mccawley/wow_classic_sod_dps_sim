from utils.classes import Spec
# runes
# chest = Overload
# hands = Lava Burst OR Water Shield
# legs = Ancestral Guidance OR Shamanistic Rage

spec_1 = Spec(
    name = "16/0/0 + Lava Burst + Ancestral Guidance",
    spec = {
        # talents
        "Convection": 5,
        "Concussion": 5,
        "Call of Thunder": 5,
        "Elemental Focus": 1,
        # runes
        "Overload": 1,
        "Lava Burst": 1,
        "Ancestral Guidance": 1,
    },
)

spec_2 = Spec(
    name = "16/0/0 + Water Shield + Ancestral Guidance",
    spec = {
        # talents
        "Convection": 5,
        "Concussion": 5,
        "Call of Thunder": 5,
        "Elemental Focus": 1,
        # runes
        "Overload": 1,
        "Water Shield": 1,
        "Ancestral Guidance": 1,
    },
)

spec_3 = Spec(
    name = "16/0/0 + Lava Burst + Shamanistic Rage",
    spec = {
        # talents
        "Convection": 5,
        "Concussion": 5,
        "Call of Thunder": 5,
        "Elemental Focus": 1,
        # runes
        "Overload": 1,
        "Lava Burst": 1,
        "Shamanistic Rage": 1,
    }
)

SPECS_LIST = [
    spec_1,
    spec_2,
    spec_3,
]