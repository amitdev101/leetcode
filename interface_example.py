from abc import ABC, abstractmethod

# Define an interface for a vehicle
class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

# Implement the interface for a car
class Car(Vehicle):
    def start(self):
        print("Starting the car...")

    def stop(self):
        print("Stopping the car...")

# Implement the interface for a motorcycle
class Motorcycle(Vehicle):
    def start(self):
        print("Starting the motorcycle...")

    def stop(self):
        print("Stopping the motorcycle...")

# Use the interfaces to start and stop different vehicles
car = Car()
motorcycle = Motorcycle()

car.start()
car.stop()

motorcycle.start()
motorcycle.stop()
