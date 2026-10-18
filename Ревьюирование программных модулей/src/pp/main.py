import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from uiproc.ui import MainWindow
from uiproc.mainui import ImagePresenter
from imgproc.keypart import imgproc
def initialize_environment():
    for folder in ['logs', 'configs', 'output']:
        os.makedirs(folder, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info("Окружение настроено. Служебные каталоги созданы.")

if __name__ == "__main__":
    initialize_environment()
    base_app = QApplication(sys.argv)
    view = MainWindow()
    model = imgproc()
    presenter = ImagePresenter(view, model)
    view.show()
    exit_code = base_app.exec()
    presenter.save_session()
    sys.exit(exit_code)