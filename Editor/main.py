import json, threading
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from .Game_window import Game_Window
from .Scene import Scene
from .Entitiy import Entity

class Editor:
    def __init__(self, project_file_dir: str, app: QApplication, Window: QMainWindow):
        self.__project_file_dir = project_file_dir
        self.__project_data = self.__get_project_data()
        self.__scenes, self.__current_scene = self.__get_scenes_from_project_data()

        self.__hierarchy_x = 0
        self.__hierarchy_y = 0

        self.__app = app
        self.__editor_window = Window
        self.__init_UI()

    def __get_scenes_from_project_data(self):
        scenes = self.__project_data["SCENES"]
        ss = []
        for s in scenes:
            new_scene = Scene(s["NAME"])
            new_scene.set_entities(s["ENTITIES"])
            ss.append(new_scene)

        return ss, 0

    def __init_UI(self):
        self.__clear_editor_window()

        self.__editor_window.setWindowTitle(f"Nitro - {self.__project_data['EDITOR']['PROJECT_NAME']} - {self.__scenes[self.__current_scene].get_name()}")
        self.__editor_window.resize(self.__project_data["EDITOR"]["EDITOR_WINDOW_WIDTH"],
                                    self.__project_data["EDITOR"]["EDITOR_WINDOW_HEIGHT"])



        self.__hierarchy_label = QWidget(self.__editor_window)
        self.__hierarchy_label.resize(200, self.__editor_window.height())
        self.__hierarchy_label.move(0, 0)
        #self.__hierarchy_label.setStyleSheet("background-color: red;")
        self.__hierarchy_label.show()

        for e in self.__scenes[self.__current_scene].get_entities():
            self.__create_slot_for_entity(e)

        self.__game_window = Game_Window(self.__project_data)

        self.__game_window_thread = threading.Thread(target=self.__game_window.main_loop, args=(self.__editor_window,))
        self.__game_window_thread.start()

        self.__editor_window.show()

    def __create_slot_for_entity(self, entity: Entity):
        btn = QPushButton(entity.get_name(), self.__hierarchy_label)
        btn.move(self.__hierarchy_x, self.__hierarchy_y)
        btn.resize(200, 30)
        btn.show()

    def __create_new_entity(self):
        print("NEW")

    def __clear_editor_window(self):
        for i in self.__editor_window.children():
            if type(i) != QLayout:
                i.deleteLater()




    def __get_project_data(self):
        data = {}
        with open(self.__project_file_dir, "r") as file:
            data = json.loads(file.read())
            file.close()
        return data

