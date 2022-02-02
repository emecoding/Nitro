class Scene:
    def __init__(self, name: str):
        self.__name = name
        self.__entities = []

    def set_entities(self, entities: list):
        self.__entities = entities

    def get_entities(self): return self.__entities

    def get_name(self): return self.__name
