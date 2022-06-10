# philosophers state : THINGKING, EATING,  HUNGRY
import random

# input
number_of_philosopher = 5
number_of_chopstick = number_of_philosopher
max_eating_time = 5

max_time = 100
thinking = 0


class Philosopher:
    def __init__(self, ID, max_eat_time):
        self.LEFT = '-'
        self.RIGHT = '-'
        self.status = 'sleep'
        self.ID = ID
        self.max_eat_time = max_eat_time
        self.eating_time = 0

    def check(self, chopstickStatus):  # to check either the philosopher is sleeping or not
        if self.status == 'sleep':
            # if want to make starvation directly occur
            # self.status = 'HUNGRY'

            # if want to make starvation indirectly to occur
            hungry = random.randint(0, 2)
            if hungry == 1:
                self.status = 'HUNGRY'
                return 0
        else:
            return self.check2(chopstickStatus)
        return 0

    def check2(self, chopstickStatus):  # to update philosopher status
        if self.status == 'HUNGRY' or self.status == 'THINKING':
            if 'free' in chopstickStatus:
                freeChopIndex = chopstickStatus.index('free')
                chopstickStatus[freeChopIndex] = 'holded'  # later update the chopstickStatus
                if self.LEFT == '-':
                    self.LEFT = freeChopIndex
                    self.status = 'THINKING'
                    return 1
                else:
                    self.RIGHT = freeChopIndex
                    self.status = 'EATING'
                    self.eating_time = random.randint(1, self.max_eat_time)
                    return -1
        else:
            self.eating_time -= 1
            if self.eating_time <= 0:
                chopstickStatus[self.LEFT] = 'free'
                self.LEFT = '-'
                chopstickStatus[self.RIGHT] = 'free'
                self.RIGHT = '-'
                self.status = 'sleep'
            return 0

        return 0


philosopher = [Philosopher(i, max_eating_time) for i in range(number_of_philosopher)]
chopstick_status = ['free' for i in range(number_of_chopstick)]

for i in range(max_time):
    for j in range(number_of_philosopher):
        returned = philosopher[j].check(chopstick_status)
        thinking += returned

    # print all the situation
    to_print = 'Philosopher\t\tstatus\t\t\t\tLeft\t\tRight\n'
    to_print += '-------------------------------------------------------\n'
    for j in range(number_of_philosopher):
        to_print += '\t' + str(philosopher[j].ID) + '\t\t\t' + philosopher[j].status + '\t\t\t\t' + str(philosopher[j].LEFT) + '\t\t\t' + str(philosopher[j].RIGHT) + '\n'
    to_print += '\n\n'
    print(to_print)

    if thinking == number_of_philosopher:
        print('starvation occurs')
        break;
