import random

class MarbleBag:
    def __init__(self, o_bag):
        assert o_bag != [] , "Input array must not be empty"
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
            assert max_attempts >=0 , "max attempts must be more than 0"
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
        assert success_rate >=0 and success_rate <=100, "success rate must be between 0-100"
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
          assert fixed_sucess_rate >=0 , "fixed rate must be more than 0"
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
         