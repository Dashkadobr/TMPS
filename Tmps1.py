import tkinter as tk
from tkinter import scrolledtext
import copy
from abc import ABC, abstractmethod


# ---------------- Singleton Pattern: Логгер ----------------
class SingletonLogger:
    _instance = None

    def __new__(cls, gui_callback=None):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance.gui_callback = gui_callback
        return cls._instance

    def log(self, message):
        log_message = f"[LOG]: {message}"
        print(log_message)
        if self.gui_callback:
            self.gui_callback(log_message + "\n")


# ---------------- Prototype Pattern: Базовый класс робота ----------------
class Robot(ABC):
    def __init__(self, name):
        self.name = name
        self.components = {}  # Словарь для хранения деталей робота

    @abstractmethod
    def perform(self):
        pass

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.name}: {self.components}"


# Конкретные реализации роботов
class HumanoidRobot(Robot):
    def perform(self):
        return f"{self.name} is performing human-like actions."


class HeavyRobot(Robot):
    def perform(self):
        return f"{self.name} is performing heavy-duty tasks."


# ---------------- Abstract Factory Pattern: Фабрика деталей робота ----------------
class RobotPartFactory(ABC):
    @abstractmethod
    def create_head(self):
        pass

    @abstractmethod
    def create_torso(self):
        pass

    @abstractmethod
    def create_limbs(self):
        pass


class HumanoidPartFactory(RobotPartFactory):
    def create_head(self):
        return "Smart Face"

    def create_torso(self):
        return "Sleek Body"

    def create_limbs(self):
        return "Agile Limbs"


class HeavyPartFactory(RobotPartFactory):
    def create_head(self):
        return "Armored Head"

    def create_torso(self):
        return "Reinforced Frame"

    def create_limbs(self):
        return "Robust Limbs"


# ---------------- Builder Pattern: Построение робота ----------------
class RobotBuilder(ABC):
    @abstractmethod
    def build_head(self):
        pass

    @abstractmethod
    def build_torso(self):
        pass

    @abstractmethod
    def build_limbs(self):
        pass

    @abstractmethod
    def get_robot(self):
        pass


class HumanoidRobotBuilder(RobotBuilder):
    def __init__(self, name):
        self.robot = HumanoidRobot(name)
        self.part_factory = HumanoidPartFactory()
        SingletonLogger().log("HumanoidRobotBuilder initialized")

    def build_head(self):
        self.robot.components['head'] = self.part_factory.create_head()
        SingletonLogger().log("Built humanoid head")

    def build_torso(self):
        self.robot.components['torso'] = self.part_factory.create_torso()
        SingletonLogger().log("Built humanoid torso")

    def build_limbs(self):
        self.robot.components['limbs'] = self.part_factory.create_limbs()
        SingletonLogger().log("Built humanoid limbs")

    def get_robot(self):
        return self.robot


class HeavyRobotBuilder(RobotBuilder):
    def __init__(self, name):
        self.robot = HeavyRobot(name)
        self.part_factory = HeavyPartFactory()
        SingletonLogger().log("HeavyRobotBuilder initialized")

    def build_head(self):
        self.robot.components['head'] = self.part_factory.create_head()
        SingletonLogger().log("Built heavy robot head")

    def build_torso(self):
        self.robot.components['torso'] = self.part_factory.create_torso()
        SingletonLogger().log("Built heavy robot torso")

    def build_limbs(self):
        self.robot.components['limbs'] = self.part_factory.create_limbs()
        SingletonLogger().log("Built heavy robot limbs")

    def get_robot(self):
        return self.robot


class RobotDirector:
    def __init__(self, builder: RobotBuilder):
        self.builder = builder
        SingletonLogger().log("RobotDirector initialized")

    def construct_robot(self):
        self.builder.build_head()
        self.builder.build_torso()
        self.builder.build_limbs()
        return self.builder.get_robot()


# ---------------- Factory Method Pattern: Фабрики роботов ----------------
class RobotFactory(ABC):
    @abstractmethod
    def create_robot(self, name):
        pass


class HumanoidRobotFactory(RobotFactory):
    def create_robot(self, name):
        SingletonLogger().log(f"Creating Humanoid Robot: {name}")
        builder = HumanoidRobotBuilder(name)
        director = RobotDirector(builder)
        return director.construct_robot()


class HeavyRobotFactory(RobotFactory):
    def create_robot(self, name):
        SingletonLogger().log(f"Creating Heavy Robot: {name}")
        builder = HeavyRobotBuilder(name)
        director = RobotDirector(builder)
        return director.construct_robot()


# ---------------- GUI: Приложение для создания и визуализации роботов ----------------
class RobotFactoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Factory Application")

        # Левая панель: управление и лог
        self.left_panel = tk.Frame(root)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        # Правая панель: визуализация роботов
        self.right_panel = tk.Frame(root)
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Элементы управления на левой панели
        self.name_label = tk.Label(self.left_panel, text="Enter Robot Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.left_panel, width=25)
        self.name_entry.pack(pady=5)
        self.btn_humanoid = tk.Button(self.left_panel, text="Create Humanoid Robot", command=self.create_humanoid_robot)
        self.btn_humanoid.pack(pady=5)
        self.btn_heavy = tk.Button(self.left_panel, text="Create Heavy Robot", command=self.create_heavy_robot)
        self.btn_heavy.pack(pady=5)
        self.btn_clone = tk.Button(self.left_panel, text="Clone Last Robot", command=self.clone_robot)
        self.btn_clone.pack(pady=5)
        self.robot_list_label = tk.Label(self.left_panel, text="Robots:")
        self.robot_list_label.pack(pady=5)
        self.robot_listbox = tk.Listbox(self.left_panel, width=40, height=8)
        self.robot_listbox.pack(pady=5)
        self.log_label = tk.Label(self.left_panel, text="Log:")
        self.log_label.pack(pady=5)
        self.log_text = scrolledtext.ScrolledText(self.left_panel, width=40, height=10, state=tk.DISABLED)
        self.log_text.pack(pady=5)

        # Область визуализации робота на правой панели
        self.canvas = tk.Canvas(self.right_panel, width=400, height=400, bg="lightgray")
        self.canvas.pack(fill="both", expand=True)

        # Инициализация логгера с передачей функции обновления лога
        self.logger = SingletonLogger(self.update_log)
        self.logger.log("Application started")

        # Фабрики роботов
        self.humanoid_factory = HumanoidRobotFactory()
        self.heavy_factory = HeavyRobotFactory()

        self.robots = []
        self.last_robot = None

    def update_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_robot_list(self):
        self.robot_listbox.delete(0, tk.END)
        for robot in self.robots:
            self.robot_listbox.insert(tk.END, str(robot))

    def draw_robot(self, robot):
        self.canvas.delete("all")
        if isinstance(robot, HumanoidRobot):
            # Голова: вариант "Oval" (по умолчанию) или "Square"
            head_style = robot.components.get("head_style", "Oval").lower()
            if head_style == "square":
                self.canvas.create_rectangle(170, 40, 230, 100, fill="peachpuff", outline="black", width=2)
                self.canvas.create_line(230, 40, 230, 100, fill="gray", width=2, dash=(2, 2))
            else:
                self.canvas.create_oval(170, 40, 230, 100, fill="peachpuff", outline="black", width=2)
                self.canvas.create_arc(175, 45, 225, 95, start=30, extent=120, style=tk.ARC, outline="white", width=1)
            # Глаза – прорисовка белков и радужки
            eye_color = robot.components.get("eye_color", "black")
            self.canvas.create_oval(185, 60, 195, 70, fill="white", outline="black")
            self.canvas.create_oval(188, 63, 192, 67, fill=eye_color, outline=eye_color)
            self.canvas.create_oval(205, 60, 215, 70, fill="white", outline="black")
            self.canvas.create_oval(208, 63, 212, 67, fill=eye_color, outline=eye_color)
            # Рот – легкая улыбка
            self.canvas.create_arc(180, 70, 220, 90, start=200, extent=140, style=tk.CHORD, fill="red")
            # Торс: если "Muscular" – более массивный с "мышцами"
            torso_style = robot.components.get("torso_style", "Standard").lower()
            if torso_style == "muscular":
                self.canvas.create_rectangle(175, 100, 215, 170, fill="lightblue", outline="black", width=4)
                self.canvas.create_line(175, 135, 215, 135, fill="blue", width=2)
                self.canvas.create_line(195, 100, 195, 170, fill="blue", width=2)
            else:
                self.canvas.create_rectangle(185, 100, 215, 170, fill="skyblue", outline="black", width=2)
            # Руки: если "Hydraulic" – более массивные с суставами
            arm_style = robot.components.get("arm_style", "Standard").lower()
            if arm_style == "hydraulic":
                self.canvas.create_line(185, 110, 150, 140, fill="black", width=5)
                self.canvas.create_oval(145, 135, 155, 145, fill="gray", outline="black")
                self.canvas.create_line(215, 110, 250, 140, fill="black", width=5)
                self.canvas.create_oval(245, 135, 255, 145, fill="gray", outline="black")
            else:
                self.canvas.create_line(185, 110, 150, 140, fill="black", width=3)
                self.canvas.create_line(215, 110, 250, 140, fill="black", width=3)
                self.canvas.create_oval(145, 135, 155, 145, fill="black")
                self.canvas.create_oval(245, 135, 255, 145, fill="black")
            # Ноги: если "Wide" – рисуем широкие ноги с суставами
            if robot.components.get("legs", "Standard").lower() == "wide":
                self.canvas.create_rectangle(180, 170, 200, 220, fill="black")
                self.canvas.create_rectangle(200, 170, 220, 220, fill="black")
                self.canvas.create_oval(190, 215, 200, 225, fill="gray", outline="black")
                self.canvas.create_oval(210, 215, 220, 225, fill="gray", outline="black")
            else:
                self.canvas.create_line(190, 170, 190, 220, fill="black", width=3)
                self.canvas.create_line(210, 170, 210, 220, fill="black", width=3)
                self.canvas.create_oval(185, 215, 195, 225, fill="black")
                self.canvas.create_oval(205, 215, 215, 225, fill="black")
            # Антенна: прорисовка, если выбрана
            if robot.components.get("antenna", "None").lower() != "none":
                self.canvas.create_line(200, 40, 200, 15, fill="green", width=2)
                self.canvas.create_oval(195, 10, 205, 20, fill="green", outline="black")
                self.canvas.create_oval(197, 12, 203, 18, fill="lightgreen", outline="green")
            self.canvas.create_text(200, 20, text=robot.name, font=("Helvetica", 16, "bold"), fill="darkblue")

        elif isinstance(robot, HeavyRobot):
            # Голова: вариант "Dome" или "Rectangle"
            head_style = robot.components.get("head_style", "Rectangle").lower()
            if head_style == "dome":
                self.canvas.create_arc(150, 40, 250, 90, start=0, extent=180, fill="dimgray", outline="black", width=3)
                self.canvas.create_line(150, 65, 250, 65, fill="black", width=2)
            else:
                self.canvas.create_rectangle(150, 40, 250, 90, fill="dimgray", outline="black", width=3)
            for x in range(160, 240, 20):
                self.canvas.create_oval(x, 45, x + 10, 55, fill="black")
            # Торс: если "Armored", прорисовка с панелями
            torso_style = robot.components.get("torso_style", "Standard").lower()
            if torso_style == "armored":
                self.canvas.create_rectangle(140, 90, 260, 180, fill="gray", outline="black", width=4)
                self.canvas.create_line(140, 130, 260, 130, fill="black", width=2)
                self.canvas.create_line(200, 90, 200, 180, fill="black", width=2)
            else:
                self.canvas.create_rectangle(140, 90, 260, 180, fill="gray", outline="black", width=3)
            # Руки: если "Robotic", прорисовка механических деталей
            arm_style = robot.components.get("arm_style", "Standard").lower()
            if arm_style == "robotic":
                self.canvas.create_rectangle(110, 90, 140, 150, fill="dimgray", outline="black", width=3)
                self.canvas.create_rectangle(260, 90, 290, 150, fill="dimgray", outline="black", width=3)
                self.canvas.create_line(125, 90, 125, 70, fill="black", width=2)
                self.canvas.create_line(275, 90, 275, 70, fill="black", width=2)
                self.canvas.create_oval(120, 70, 130, 80, fill="black", outline="gray")
                self.canvas.create_oval(270, 70, 280, 80, fill="black", outline="gray")
            else:
                self.canvas.create_rectangle(110, 90, 140, 150, fill="dimgray", outline="black", width=3)
                self.canvas.create_rectangle(260, 90, 290, 150, fill="dimgray", outline="black", width=3)
            # Ноги: если "Wide" – прорисовка широких ног с суставами
            if robot.components.get("legs", "Standard").lower() == "wide":
                self.canvas.create_rectangle(160, 180, 190, 260, fill="black", outline="black")
                self.canvas.create_rectangle(210, 180, 240, 260, fill="black", outline="black")
                self.canvas.create_oval(170, 255, 180, 265, fill="gray", outline="black")
                self.canvas.create_oval(220, 255, 230, 265, fill="gray", outline="black")
            else:
                self.canvas.create_rectangle(170, 180, 190, 260, fill="black", outline="black")
                self.canvas.create_rectangle(210, 180, 230, 260, fill="black", outline="black")
            # Антенна
            if robot.components.get("antenna", "None").lower() != "none":
                self.canvas.create_line(200, 40, 200, 15, fill="green", width=2)
                self.canvas.create_oval(195, 10, 205, 20, fill="green", outline="black")
                self.canvas.create_oval(197, 12, 203, 18, fill="lightgreen", outline="green")
            self.canvas.create_text(200, 20, text=robot.name, font=("Helvetica", 16, "bold"), fill="darkred")
        else:
            self.canvas.create_text(200, 200, text="Unknown Robot Type", font=("Helvetica", 16))

    def create_humanoid_robot(self):
        name = self.name_entry.get().strip() or f"Humanoid-{len(self.robots) + 1}"
        robot = self.humanoid_factory.create_robot(name)
        self.last_robot = robot
        self.robots.append(robot)
        self.logger.log(f"Created humanoid robot: {robot}")
        self.update_robot_list()
        self.draw_robot(robot)

    def create_heavy_robot(self):
        name = self.name_entry.get().strip() or f"Heavy-{len(self.robots) + 1}"
        robot = self.heavy_factory.create_robot(name)
        self.last_robot = robot
        self.robots.append(robot)
        self.logger.log(f"Created heavy robot: {robot}")
        self.update_robot_list()
        self.draw_robot(robot)

    def clone_robot(self):
        if self.last_robot:
            new_robot = self.last_robot.clone()
            new_robot.name = f"{new_robot.name}_clone"
            self.robots.append(new_robot)
            self.last_robot = new_robot
            self.logger.log(f"Cloned robot: {new_robot}")
            self.update_robot_list()
            self.draw_robot(new_robot)
            self.open_edit_dialog(new_robot)
        else:
            self.logger.log("No robot to clone.")

    def open_edit_dialog(self, robot):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Cloned Robot")

        # Имя робота
        tk.Label(edit_window, text="New Robot Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_var = tk.StringVar(value=robot.name)
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        # Антенна
        tk.Label(edit_window, text="Antenna:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        antenna_options = ["None", "Small", "Large"]
        antenna_var = tk.StringVar(value=robot.components.get("antenna", "None"))
        tk.OptionMenu(edit_window, antenna_var, *antenna_options).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Legs style
        tk.Label(edit_window, text="Legs style:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        legs_options = ["Standard", "Wide"]
        legs_var = tk.StringVar(value=robot.components.get("legs", "Standard"))
        tk.OptionMenu(edit_window, legs_var, *legs_options).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Head style
        tk.Label(edit_window, text="Head Style:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        if isinstance(robot, HumanoidRobot):
            head_options = ["Oval", "Square"]
        else:
            head_options = ["Rectangle", "Dome"]
        head_var = tk.StringVar(value=robot.components.get("head_style", head_options[0]))
        tk.OptionMenu(edit_window, head_var, *head_options).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Torso style
        tk.Label(edit_window, text="Torso Style:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        if isinstance(robot, HumanoidRobot):
            torso_options = ["Standard", "Muscular"]
        else:
            torso_options = ["Standard", "Armored"]
        torso_var = tk.StringVar(value=robot.components.get("torso_style", "Standard"))
        tk.OptionMenu(edit_window, torso_var, *torso_options).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Arm style
        tk.Label(edit_window, text="Arm Style:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        if isinstance(robot, HumanoidRobot):
            arm_options = ["Standard", "Hydraulic"]
        else:
            arm_options = ["Standard", "Robotic"]
        arm_var = tk.StringVar(value=robot.components.get("arm_style", "Standard"))
        tk.OptionMenu(edit_window, arm_var, *arm_options).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Eye color (только для Humanoid)
        if isinstance(robot, HumanoidRobot):
            tk.Label(edit_window, text="Eye Color:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
            eye_options = ["Black", "Blue", "Green", "Brown", "Hazel"]
            eye_var = tk.StringVar(value=robot.components.get("eye_color", "Black"))
            tk.OptionMenu(edit_window, eye_var, *eye_options).grid(row=6, column=1, padx=5, pady=5, sticky="ew")
            row_offset = 1
        else:
            row_offset = 0

        def apply_changes():
            new_name = name_var.get().strip()
            if new_name:
                robot.name = new_name
            robot.components["antenna"] = antenna_var.get()
            robot.components["legs"] = legs_var.get()
            robot.components["head_style"] = head_var.get()
            robot.components["torso_style"] = torso_var.get()
            robot.components["arm_style"] = arm_var.get()
            if isinstance(robot, HumanoidRobot):
                robot.components["eye_color"] = eye_var.get()
            self.logger.log(f"Modified cloned robot: {robot}")
            self.update_robot_list()
            self.draw_robot(robot)
            edit_window.destroy()

        tk.Button(edit_window, text="Apply Changes", command=apply_changes).grid(row=7 + row_offset, column=0,
                                                                                 columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotFactoryApp(root)
    root.mainloop()
