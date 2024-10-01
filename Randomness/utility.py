import random

class MarbleBag:
    def __init__(self, o_bag):
        self.bag = []
        self.o_bag = o_bag
    
    def setseed(self,seed):
         random.seed(seed)

    def draw(self ):
        if not self.bag:
            self.bag = self.o_bag.copy()
            random.shuffle(self.bag)
        return self.bag.pop()
    
class Predeteermination():
         def __init__(self,max_attempts)-> None:
            self.attempts = 0
            self.max_attempts = max_attempts

         def setseed(self,seed):
            random.seed(seed)

         def attempt(self):
              self.attempts =+1
              if self.attempts >= self.max_attempts:
                   self.attempt = 0
                   return True
              else:
                   return False
              
class progressive():
    def __init__(self, success_rate, increment) -> None:
        self.base_success_rate = success_rate
        self.current_success_rate = self.base_success_rate
        self.increment = increment
    
    def setseed(self,seed):
     random.seed(seed)

    def reset_probability(self):
        self.current_success_rate = self.base_success_rate

    def attempt(self):
        p = random.uniform(0, 100)
        if p < self.current_success_rate:
            print(f"successful {self.current_success_rate}")
            self.reset_probability()
            return True
        else:
            self.current_success_rate += self.increment
            print(f"failed {self.current_success_rate}")
            return False
        
class fixedReateProb():
    def __init__(self,probability,fixed_sucess_rate)-> None:
          self.attempt_count = 0
          self.fixed_sucess_rate = fixed_sucess_rate
          self.based_probability = probability

    def setseed(self,seed):
     random.seed(seed)


    def attempt(self):
         self.attempt_count +=1
         if self.attempt_count >= self.fixed_sucess_rate:
              self.attempt_count =0
              return True
         roll = random.uniform(0,100)
         if roll<self.based_probability:
              self.attempt_count = 0
              return True
         else:
              return False
         