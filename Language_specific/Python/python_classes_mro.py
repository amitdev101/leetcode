class Base:
    def __init__(self):
        print("Base init")

class Derived1(Base):
    def __init__(self):
        super().__init__()
        print("Derived1 init")

class Derived2(Base):
    def __init__(self):
        super().__init__()
        print("Derived2 init")

class DerivedFinal(Derived1, Derived2):
    def __init__(self):
        super().__init__()
        print("DerivedFinal init")

df = DerivedFinal()
print(DerivedFinal.__mro__)

# output
# Base init
# Derived2 init
# Derived1 init
# DerivedFinal init
# (<class '__main__.DerivedFinal'>, <class '__main__.Derived1'>, <class '__main__.Derived2'>, <class '__main__.Base'>, <class 'object'>)

'''
why this happened
Inside Derived1.__init__(), super().__init__() calls Derived2.__init__(), again following the MRO.
shouldn't Derived1.__init__() should finish itself
ChatGPT

In Python, the behavior of super().__init__() within the context of multiple inheritance and the Method Resolution Order (MRO) can indeed be a bit counterintuitive. To clarify, let's break down what happens when super().__init__() is called in Derived1.__init__().
The Role of super() in Python's Multiple Inheritance

When you use super() in a method, it doesn't just call the same method in the parent class. Instead, it continues along the Method Resolution Order (MRO). The MRO determines the order in which base classes are searched when a method is called. In a multiple inheritance scenario, this means that super() might call a method from a different class than the immediate parent.
Why Derived2.__init__() is Called from Derived1.__init__():

    DerivedFinal.__init__(): When an instance of DerivedFinal is created, DerivedFinal.__init__() is the first to be called.

    Derived1.__init__() via super(): Inside DerivedFinal.__init__(), the call to super().__init__() follows the MRO and reaches Derived1.__init__().

    Continuing the MRO in Derived1.__init__():
        Within Derived1.__init__(), when super().__init__() is called, it doesn't just call Base.__init__() (the immediate parent of Derived1).
        Instead, it continues along the MRO, which leads to Derived2.__init__() next.
        This is because super() in Python is more about continuing the MRO chain rather than directly calling the parent class's method.

    Derived2.__init__() and Then Base.__init__():
        After Derived2.__init__() is executed, super().__init__() inside it finally calls Base.__init__(), since that's the next in the MRO.
        This ensures that each class in the MRO is executed in order, and Base.__init__() is called only once, avoiding duplicate initializations.

    Control Returns Back Up the Chain:
        After Base.__init__() completes, control returns back up the chain: to Derived2.__init__(), then to Derived1.__init__(), and finally to DerivedFinal.__init__().

Conclusion

In summary, super().__init__() in Derived1.__init__() doesn’t directly call its immediate superclass’s __init__ but follows the MRO to find the next class in line. This behavior is central to how Python handles method resolution in multiple inheritance, ensuring a consistent and logical order of method calls and preventing issues like the diamond problem.
'''