#  Helper for storing small pieces of state in NAO's ALMemory service.

#  Convenience methods to read, write and clear ALMemory keys used by the game.
class MemoryHelper:
#  Store the ALMemory service reference.
    def __init__(self, session):
        self.memory = session.service("ALMemory")

#  Remove a value from ALMemory if it exists.
    def RemoveMemoryEntry(self, name):
        if self.memory:
            try:
                self.memory.removeData(name)
            except:
                pass

#  Safely read a value from ALMemory (returns None if missing).
    def GetMemoryEntry(self, name):
        if self.memory:
            try:
                return self.memory.getData(name)
            except:
                pass

#  Safely write a value into ALMemory.
    def InsertMemoryEntry(self, name, value):
        if self.memory:
            try:
                self.memory.insertData(name, value)
                print("Saved in memory: " + name + " Value:" + str(value))
            except:
                pass

#  Remove the specific keys used by the game to avoid stale data.
    def ClearMemory(self):
        self.RemoveMemoryEntry("Image1")
        self.RemoveMemoryEntry("Image2")
        self.RemoveMemoryEntry("Image3")
        self.RemoveMemoryEntry("Result")