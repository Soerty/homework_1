#-*- coding: utf-8 -*-


class Animal(object):
    age = None
    name = None

    def __init__(self, age, name):
        self.age = age
        self.name = name

    def move(self):
        raise NotImplementedError


class Mammal(Animal):
    def move(self):
        return 'I go by land'


class Bird(Animal):
    def move(self):
        return 'I swim in the water'


class Fish(Animal):
    def move(self):
        return 'I believe I can fly'


class Zoo(object):
    animals = []

    def inspection(self):
        print ('\tList of all animals in the zoo:')
        for animal in self.animals:
            print ('=' * 15)
            print ('Ward: %s' % animal.__class__.__name__)
            print ('Name: %s' % animal.name)
            print ('Age: %s years' % animal.age)
            print ('Test of movement: %s' % animal.move())


if __name__ == '__main__':
    zoo = Zoo()
    
    owl = Bird(1.5, 'Hoodini')
    zoo.animals.append(owl)
    nemo = Fish(0.3, 'Nemo')
    zoo.animals.append(nemo)
    simba = Mammal(5, 'simba')
    zoo.animals.append(simba)

    zoo.inspection()
