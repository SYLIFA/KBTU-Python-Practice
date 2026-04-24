class Parent:
  def myMethod(self):
    print("Parent")
class Child(Parent):
  def myMethod(self):
    print("Child")
c = Child()
c.myMethod()
