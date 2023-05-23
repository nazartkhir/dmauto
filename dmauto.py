import random

class Simulator():
    def __init__(self) -> None:
        self.sleep = self.sleep()
        self.study = self.study()
        self.workout = self.workout()
        self.rest = self.rest()
        self.drunk = self.drunk()
        self.friday = self.friday()
        self.motivation = self.motivation()
        self.wrote_test = self.wrote_test()
        self.cur_state = self.sleep
        self.events = [self.friday, self.motivation, self.wrote_test]
        self.energy = 0
        next(self.sleep)
        next(self.study)
        next(self.workout)
        next(self.rest)
        next(self.drunk)
        next(self.friday)
        next(self.motivation)
        next(self.wrote_test)
        
    def day_sim(self):
        for i in range(24):
            event = random.choice(self.events)
            event.send(i)
            self.cur_state.send(i)
    def friday(self):
        while True:
            hour = yield
            if random.random() < 1/7 and hour > 15:
                print('It is Friday.\n')
                self.cur_state = self.drunk
    def motivation(self):
        while True:
            hour = yield
            if random.random() < 1/8:
                print('You had extra motivation.\n')
                self.energy += 50
    def wrote_test(self):
        while True:
            hour = yield
            if random.random() < 1/10 and hour > 15:
                print('You just wrote a test.\n')
                self.cur_state = self.drunk
    def sleep(self):
        while True:
            hour = yield
            print(f'Current hour: {hour}\nYou are sleeping.\n')
            if 0 < hour < 7 or self.energy < 30:
                self.cur_state = self.sleep
                self.energy += 20
            else:
                self.cur_state = self.study
            
    def study(self):
        while True:
            hour = yield
            print(f'Current hour: {hour}\nYou are studying.\n')
            if hour < 19 and self.energy > 20:
                self.cur_state = self.study
            else:
                self.cur_state = self.rest
            self.energy -= 15

    def rest(self):
        while True:
            hour = yield
            print(f'Current hour: {hour}\nYou are resting.\n')
            if self.energy > 40:
                self.cur_state = self.workout
            else:
                self.cur_state = self.rest
            self.energy += 20
    
    def workout(self):
        while True:
            hour = yield
            print(f'Current hour: {hour}\nYou are working out.\n')
            self.cur_state = self.rest
            self.energy = 5
    
    def drunk(self):
        while True:
            hour = yield
            print(f'Current hour: {hour}\nYou are drunk.\n')
            self.energy += 20
            self.cur_state = self.drunk
            if hour >= 22:
                self.energy = 0
                self.cur_state = self.sleep


sim = Simulator()
sim.day_sim()