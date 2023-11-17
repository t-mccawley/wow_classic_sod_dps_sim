from utils.classes import Buff

class ArcaneIntellect(Buff):
    def __init__(self,rank):
        super().__init__()

        if rank == 1:
            self.intellect_bonus = 2
        elif rank == 2:
            self.intellect_bonus = 7
        elif rank == 3:
            self.intellect_bonus = 15
        elif rank == 4:
            self.intellect_bonus = 22
        elif rank == 5:
            self.intellect_bonus = 31
        else:
            print("Unsupported rank!")
        
        self.max_duration_sec = 30*60
    
class MarkOfTheWild(Buff):
    def __init__(self,rank):
        super().__init__()
        
        if rank == 1:
            self.intellect_bonus = 0
            self.spirit_bonus = 0
        elif rank == 2:
            self.intellect_bonus = 2
            self.spirit_bonus = 2
        elif rank == 3:
            self.intellect_bonus = 4
            self.spirit_bonus = 4
        elif rank == 4:
            self.intellect_bonus = 6
            self.spirit_bonus = 6
        elif rank == 5:
            self.intellect_bonus = 8
            self.spirit_bonus = 8
        elif rank == 6:
            self.intellect_bonus = 10
            self.spirit_bonus = 10
        elif rank == 7:
            self.intellect_bonus = 12
            self.spirit_bonus = 12
        else:
            print("Unsupported rank!")
        
        self.max_duration_sec = 30*60