import logging
import os
from PyQt6.QtWidgets import QFileDialog
from imgproc.hist import log_action_to_json
from uiproc.config_manager import ConfigManager
class ImagePresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.config = ConfigManager()
        self.view.btn_open.clicked.connect(self.open_file)
        self.view.btn_apply_filter.clicked.connect(self.apply_selected_filter)
        self.view.btn_resize.clicked.connect(self.resize_image)
        self.view.btn_undo.clicked.connect(self.undo_action)
        self.view.btn_save.clicked.connect(self.save_file)
        self.load_saved_session()

    def load_saved_session(self):
        geom = self.config.get_geometry()
        if geom:
            self.view.restoreGeometry(geom)
        self.view.combo_filters.setCurrentIndex(self.config.get_last_filter())

    def save_session(self):
        self.config.save_settings(
            self.config.get_last_path(),
            self.view.combo_filters.currentIndex(),
            self.view.saveGeometry()
        )

    def open_file(self):
        last_dir = self.config.get_last_path()
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Открыть файл", last_dir, "Изображения (*.png *.jpg *.jpeg)"
        )
        if file_path:
            try:
                self.model.load_image(file_path)
                self.config.save_settings(os.path.dirname(file_path), self.view.combo_filters.currentIndex(), self.view.saveGeometry())
                self.view.display_image(self.model.current_image)
                self.view.update_info(self.model.get_info())
                log_action_to_json("open_file", {"path": file_path})
            except Exception as e:
                logging.error(f"Ошибка открытия файла: {e}", exc_info=True)
                self.view.show_error(f"Не удалось открыть файл:\n{str(e)}")

    def apply_selected_filter(self):
        filter_index = self.view.combo_filters.currentIndex()
        try:
            if filter_index == 1:
                self.model.apply_grayscale()
                log_action_to_json("apply_filter", {"type": "grayscale"})
            elif filter_index == 2:
                self.model.apply_blur()
                log_action_to_json("apply_filter", {"type": "blur"})
            else:
                return
            self.view.display_image(self.model.current_image)
            self.view.update_info(self.model.get_info())
        except Exception as e:
            logging.error(f"Ошибка фильтрации: {e}", exc_info=True)
            self.view.show_error(str(e))

    def resize_image(self):
        try:
            w = self.view.spin_width.value()
            h = self.view.spin_height.value()
            self.model.resize_image(w, h)
            
            self.view.display_image(self.model.current_image)
            self.view.update_info(self.model.get_info())
            log_action_to_json("resize", {"width": w, "height": h})
        except Exception as e:
            logging.error(f"Ошибка масштабирования: {e}", exc_info=True)
            self.view.show_error(str(e))

    def undo_action(self):
        if self.model.undo():
            self.view.display_image(self.model.current_image)
            self.view.update_info(self.model.get_info())
            log_action_to_json("undo")
            self.view.show_info("Действие отменено.")
        else:
            self.view.show_error("Нет сохраненных действий для отмены.")

    def save_file(self):
        last_dir = self.config.get_last_path()
        file_path, _ = QFileDialog.getSaveFileName(
            self.view, "Сохранить файл", last_dir, "JPEG (*.jpg);;PNG (*.png)"
        )
        if file_path:
            try:
                self.model.save_image(file_path)
                log_action_to_json("save_file", {"path": file_path})
                self.view.show_info("Файл успешно сохранен!")
            except Exception as e:
                logging.error(f"Ошибка сохранения: {e}", exc_info=True)
                self.view.show_error(str(e))