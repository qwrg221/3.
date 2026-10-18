import os#данный файл взаимодействует с юаем + имеет строки с функционалом и проверками
import logging
from PIL import Image, ImageFilter # ИМПОРТ БИБЛИОТЕК (в качестве пометок, отображаю все совершенные в строках(блоках строк) действия для дальнейших проектов, приоритетно для собственного пользования и дальнейшего понимания сути)
#данный код разделен на блоки, которые зачастую работают по разному функционалу, для моего собственного лучшего понимания
class imgproc:
    def __init__(self): #проверка формата + загрузка файла
        self.current_image = None #текущая картинка
        self.previous_image = None #действие для отмены
        self.original_format = "PNG" # записываемая картинка
    def validate_file(self, file_path: str): #путь к файлу
        """Проверка файла"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")#остановка процесса, при ошибке
        valid_extensions = ('.jpg', '.jpeg', '.png')#поддерживаемый формат файлов
        if not file_path.lower().endswith(valid_extensions):#нижний регистр + проверка формата
            raise ValueError("Неподдерживаемый формат, разрешены только JPEG и PNG.")
    
    #функциональный блок для дальнейших действий, загрузка картинки, ее проверка, откат
    def load_image(self, file_path: str):#для развертывания картинки
        """Загрузка изображения в память приложения."""
        self.validate_file(file_path)#проверка
        self.current_image = Image.open(file_path)#происходит при успешной проверке, загружает картинку
        self.original_format = self.current_image.format or "PNG"#приравнивание формата к png как основному, если файл принимет не считываемый формат для библиотеки Pil
        self.previous_image = None # Сброс отката
        logging.info(f"Изображение загружено. Начальный формат: {self.original_format}")#для лога
    
    #получение характеристик
    def get_info(self) -> dict:#для получения характеристик избрж и собственно вывода этого элемента в графическую часть
        """Получение текущих характеристик изображения."""
        if not self.current_image:#проверка на то, загружена ли картинка вообще
            return {"width": 0, "height": 0, "format": "Нет данных"}#коли картинка не загружена. Крайне важная строка, т.к. чуть ли не аварийно выставляет 0 для дальнейшей работы программы
        return {#при условии наличии картинки 
            "width": self.current_image.width,
            "height": self.current_image.height,
            "format": self.original_format
        }#последние три строки для получения информации от пил о картинке
    
    #блок отката
    def _save_for_undo(self):#блок для отмены, вызывает только сам класс, перед любой операцией
        """Внутренний метод для сохранения копии перед изменением."""
        if self.current_image:
            self.previous_image = self.current_image.copy()#две строки для копирования в буфер картинки
    def undo(self) -> bool:#при "отмене"
        """Откат на 1 шаг назад.True в случае успеха."""
        if self.previous_image:#при наличии копии в буфере
            self.current_image = self.previous_image.copy()#откат на копию в буфере
            self.previous_image = None#отчиска буфера для дальнейших копий
            logging.info("Действие отменено пользователем.")
            return True#отмена успешна и снизу соответственно неуспешна 
        return False
   
    #блок по изменению палитры
    def apply_grayscale(self):
        """Фильтр Проекта 2: Преобразование в Черно-белый режим."""
        if not self.current_image:#проверка на то, загружен ли файл в целом
            raise RuntimeError("Изображение не загружено.")
        self._save_for_undo()#сохранение в буфер
        self.current_image = self.current_image.convert("L")#опция опять пил, позволяет перекрасить картинку в серый 
        logging.info("Применен фильтр: Ч/Б")
   
    #блок с блюром
    def apply_blur(self):
        """Фильтр Проекта 2: Легкое размытие (фиксированный радиус = 2)."""
        if not self.current_image:#та же самая проверка на загрузку картинки
            raise RuntimeError("Изображение не загружено.")
        self._save_for_undo()
        self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(radius=2))#интересный как по мне метод по гаусу, но данная строка отвечает за размытие, забавный факт, по гауссу в майнкрафте нашли легендарный заставочный фон, не знаю зачем проверяющим или мне в дальнейшем данная информация, пусть будет
        logging.info("Применено фиксированное легкое размытие.")
    
    #блок с ресайзом
    def resize_image(self, width: int, height: int):
        """Изменение размера изображения."""
        if not self.current_image:
            raise RuntimeError("Изображение не загружено.")#очередная проверка на загрузку избр
        if width <= 0 or height <= 0:#ратник чтобы заразить чей то комп ( проверяет размеры, параметры не могут быть меньше 1)
            raise ValueError("Размеры картинки должны быть строго больше 0.")
        self._save_for_undo()
        self.current_image = self.current_image.resize((width, height), Image.Resampling.LANCZOS)#очередная функция пил, растягивает - сжимает пнгшку
        logging.info(f"Размер изменен на: {width}x{height}")#собственно значения сжатия
   
    #блок для сохранения итогового файла
    def save_image(self, output_path: str):
        """Сохранение итогового файла."""
        if not self.current_image:
            raise RuntimeError("Нечего сохранять.")#проверка на то загружен ли файл, теперь я понимаю что чувствуют разработчкики когда прописывают похожие строки в играх/приложениях, унылая картина, но ТЫ делай это, т.к. это реально важно, вспоминая свои-то практические ёмае
        ext = os.path.splitext(output_path)[1].lower()#разбиение файла на две части 
        if ext not in ['.jpg', '.jpeg', '.png']:#проверка формата
            raise ValueError("Сохранять можно только в форматы JPEG или PNG.")
        # Если картинка в чб или пнгшка имела прозрачность, а сохраняем в жпг то убирается прозрачность
        out_img = self.current_image#ссылка на картинку для сохранения
        if ext in ['.jpg', '.jpeg'] and out_img.mode in ('RGBA', 'LA'):#проверка, плохо когда жпег с прозрачносью потому что
            out_img = out_img.convert("RGB")#насильное убирание прозрачности
            
        out_img.save(output_path)#запись на итога
        logging.info(f"Файл успешно сохранен: {output_path}")