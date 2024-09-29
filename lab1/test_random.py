import random
from utility import bag

class Predeteermination():
         def __init__(self,max_attempts)-> None:
            self.attempts = 0
            self.max_attempts = max_attempts
         def attempt(self):
              self.attempts =+1
              if self.attempts >= self.max_attempts:
                   self.attempt = 0
                   return True
              else:
                   return False

class fixedReateProb():
    def __init__(self,probability,fixed_sucess_rate)-> None:
          self.attempt_count = 0
          self.self.fixed_sucess_rate = fixed_sucess_rate
          self.based_probability = probability

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

class progressive():
    def __init__(self,success_rate,increment)-> None:
         self.base_success_rate= success_rate
         self.current_sucess_rate = self.base_success_rate
         self.increment- increment
    def reset_probability(self):
        self.current_sucess_rate = self.base_success_rate    

    def attemp(self, success_rate):
        assert success_rate >=0 and success_rate <=100, "success rate must be between 0-100"
        p = random.uniform(0,100)
        base_probability = self.base_success_rate
        if p< base_probability:
            print("sucessful")
            return True
        else:
            print("failed")
            return False


def progressive_attempt(success_rate, i):
    assert success_rate >=0 and success_rate <=100, "success rate must be between 0-100"
    i =0

    p = random.uniform(i,100)
    base_probability = success_rate
    if p< base_probability:
            print("sucessful")
            return True
    else:
            print("failed")
            i = i+1
            return False

def attemp(success_rate):
    assert success_rate >=0 and success_rate <=100, "success rate must be between 0-100"
    p = random.uniform(0,100)
    base_probability = success_rate
    if p< base_probability:
        print("sucessful")
        return True
    else:
        print("failed")
        return False

    def main():
        for _ in range(10):
            attemp(20)
        W = 0
        for _ in range(10):
            A = progressive_attempt(20,W)
            if not A:
                W = W+1


    if __name__ == "__main__":
        main()