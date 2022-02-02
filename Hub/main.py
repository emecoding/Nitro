import Editor.main
from PyQt5.QtWidgets import *
import sys, json, os

class Hub:
    def __init__(self):
        self.__config_data = self.__get_config_data()
        self.__old_projects = self.__get_old_projects()

        self.__app = QApplication([])
        self.__window = QMainWindow()
        self.__window.resize(800, 600)
        self.__window.setWindowTitle("Nitro Hub")
        self.__window.setMinimumSize(800, 600)

        y = 10
        for project in self.__old_projects["OLD_PROJECTS"]:
            btn = QPushButton(project["name"], self.__window)
            btn.move(10, y)
            btn.resize(200, 30)
            btn.clicked.connect(lambda: self.__load_project(f"{project['dir']}/{project['name']}{self.__config_data['PROJECT_EXTENSION']}"))

            y += 40

        self.__project_name_entry = QLineEdit(self.__window)
        self.__project_name_entry.resize(200, 30)
        self.__project_name_entry.move(300, 150)
        self.__project_name_entry.show()

        self.__create_new_project_btn = QPushButton("Create a new project", self.__window)
        self.__create_new_project_btn.resize(200, 30)
        self.__create_new_project_btn.move(300, 200)
        self.__create_new_project_btn.clicked.connect(self.__create_new_project)
        self.__create_new_project_btn.show()

        self.__window.show()

        self.__app.exec_()

    def __get_old_projects(self):
        data = {}
        with open("HUB.json", "r") as file:
            data = json.loads(file.read())
            file.close()
        return data

    def __get_config_data(self):
        data = {}
        with open("../Editor/EDITOR.json", "r") as file:
            data = json.loads(file.read())
            file.close()
        return data


    def __load_project(self, dir):
        Editor.main.Editor(dir, self.__app, self.__window)

    def __create_new_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        project_dir = QFileDialog.getExistingDirectory(self.__window, "Select directory for your project", options=options)
        project_name = self.__project_name_entry.text()
        project_name = project_name.replace(" ", "_")

        project_file = f"{project_dir}/{project_name}/{project_name}{self.__config_data['PROJECT_EXTENSION']}"

        data_to_write = {
            "EDITOR": {
                "PROJECT_NAME": project_name,
                "EDITOR_WINDOW_WIDTH": self.__config_data["DEFAULT_EDITOR_WINDOW_WIDTH"],
                "EDITOR_WINDOW_HEIGHT": self.__config_data["DEFAULT_EDITOR_WINDOW_HEIGHT"],
                "GAME_WINDOW_WIDTH": self.__config_data["DEFAULT_GAME_WINDOW_WIDTH"],
                "GAME_WINDOW_HEIGHT": self.__config_data["DEFAULT_GAME_WINDOW_HEIGHT"]
            },
            "SCENES": [
                {"NAME": "Sample scene", "ENTITIES": []}
            ]
        }


        if os.path.isdir(f"{project_dir}/{project_name}") == False:
            os.mkdir(f"{project_dir}/{project_name}")
            with open(project_file, "w+") as file:
                file.write(json.dumps(data_to_write, indent=3))
                file.close()

        new_project_data = {
            "dir": f"{project_dir}/{project_name}",
            "name": project_name
        }
        data = {}

        with open("HUB.json", "r") as file:
            data = json.loads(file.read())
            file.close()

        data["OLD_PROJECTS"].append(new_project_data)

        with open("HUB.json", "w") as file:
            file.write(json.dumps(data, indent=3))
            file.close()


        self.__load_project(project_file)






hub = Hub()