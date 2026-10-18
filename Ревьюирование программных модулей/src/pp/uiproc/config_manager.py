from PyQt6.QtCore import QSettings
class ConfigManager:
    def __init__(self):
        self.settings = QSettings("configs/settings.ini", QSettings.Format.IniFormat)#по сути данный файл, просто инициализация настроек pyqt
        # все остальные строки это "удержание" настроек в нужном состоянии
    def save_settings(self, last_path: str, last_filter: int, geometry):
        self.settings.setValue("user/last_path", last_path)
        self.settings.setValue("user/last_filter", last_filter)
        self.settings.setValue("window/geometry", geometry)
#прошедшие строки служат как раз для сохранения настроек
    def get_last_path(self) -> str:
        return self.settings.value("user/last_path", "")
#считывает сохранненый путь
    def get_last_filter(self) -> int:
        val = self.settings.value("user/last_filter", 0)
        return int(val) if val else 0

    def get_geometry(self):
        return self.settings.value("window/geometry")
    # проверка на размеры интерфейса, если что-то пойдет не так, выдаст "стоковые" значения