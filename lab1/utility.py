import random

class bag:
    def __init__(self,obag):
     self.stuffs = obag
     self.bag = []

    def draw(self):
     self.bag = self.stuffs.copy()
     random.shuffle(self.bag)
     return self.bag.pop()
