from utils
# for each spec
# for each buff profile
# for each gear set
# for each rotation
# instantiate character
# for each encounter


class Sim:
    """ Class used to simulate a particular encounter and character"""
    def __init__(self,encounter,spec,buff_profile,gear_set,rotation):
        self.encounter = encounter
        self.character = 