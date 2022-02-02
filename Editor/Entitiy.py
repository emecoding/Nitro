from .Entity_Components.Transform import Transform
from .Entity_Components.Component import Component

class Entity:
    def __init__(self, name: str, x=0, y=0):
        self.__name = name
        self.__components = []

        self.transform = self.add_component(Transform(x, y))

    def get_name(self): return self.__name

    def add_component(self, component: Component):
        self.__components.append(component)
        return component

    def remove_component(self, component: Component):
        if component in self.__components:
            self.__components.remove(component)



