from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QSpinBox, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PIL import Image
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("РЕДАКТОР")
        self.resize(800, 550)
        self.btn_open = QPushButton("Открыть файл")
        self.btn_save = QPushButton("Сохранить как...")
        self.btn_undo = QPushButton("Отмена")
        self.label_filter = QLabel("Выбор фильтра:")
        self.combo_filters = QComboBox()
        self.combo_filters.addItems(["Без фильтра", "Черно-белый (Ч/Б)", "Легкое размытие"])
        self.btn_apply_filter = QPushButton("Применить фильтр")
        self.label_size = QLabel("Изменить размер:")
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 10000)
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 10000)
        self.btn_resize = QPushButton("Изменить размер")
        self.info_panel = QLabel("Характеристики: Файл не загружен")
        self.info_panel.setStyleSheet("font-weight: bold; color: #333;")
        self.preview_label = QLabel("Предпросмотр изображения")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 2px dashed #aaa; background-color: #f0f0f0;")
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.btn_open)
        control_layout.addWidget(self.label_filter)
        control_layout.addWidget(self.combo_filters)
        control_layout.addWidget(self.btn_apply_filter)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.spin_width)
        size_layout.addWidget(self.spin_height)
        control_layout.addWidget(self.label_size)
        control_layout.addLayout(size_layout)
        control_layout.addWidget(self.btn_resize)
        control_layout.addWidget(self.btn_undo)
        control_layout.addWidget(self.btn_save)
        control_layout.addStretch()
        main_layout = QHBoxLayout()
        main_layout.addLayout(control_layout, 1)
        preview_container = QVBoxLayout()
        preview_container.addWidget(self.info_panel)
        preview_container.addWidget(self.preview_label, 4)
        main_layout.addLayout(preview_container, 3)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def display_image(self, pil_image: Image.Image):
        if pil_image is None:
            return
        rgba_img = pil_image.convert("RGBA")
        data = rgba_img.tobytes("raw", "RGBA")
        qimg = QImage(data, rgba_img.width, rgba_img.height, QImage.Format.Format_RGBA8888)
        
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaled(self.preview_label.size(), 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        self.preview_label.setPixmap(scaled_pixmap)

    def update_info(self, info: dict):
        self.info_panel.setText(f"Ширина: {info['width']}px | Высота: {info['height']}px | Формат: {info['format']}")
        self.spin_width.setValue(info['width'])
        self.spin_height.setValue(info['height'])

    def show_error(self, message: str):
        QMessageBox.critical(self, "Ошибка", message)

    def show_info(self, message: str):
        QMessageBox.information(self, "Успешно", message)