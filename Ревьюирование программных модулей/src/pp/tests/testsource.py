import pytest
import os
from PIL import Image
from imgproc.keypart import ImageProcessor
@pytest.fixture
#файл с тестами по вызову в кмд программы
def create_dummy_png(tmp_path):
    img_path = tmp_path / "source.png"
    img = Image.new("RGB", (300, 200), color="blue")
    img.save(img_path)
    return str(img_path)

def test_invalid_extension(tmp_path):
    invalid_file = tmp_path / "doc.pdf"
    invalid_file.write_text("dummy")
    proc = ImageProcessor()
    with pytest.raises(ValueError):
        proc.validate_file(str(invalid_file))

def test_load_and_info(create_dummy_png):
    proc = ImageProcessor()
    proc.load_image(create_dummy_png)
    info = proc.get_info()
    assert info["width"] == 300
    assert info["height"] == 200
    assert info["format"] == "PNG"

def test_filter_grayscale(create_dummy_png):
    proc = ImageProcessor()
    proc.load_image(create_dummy_png)
    proc.apply_grayscale()
    assert proc.current_image.mode == "L"

def test_resize_logic(create_dummy_png):
    proc = ImageProcessor()
    proc.load_image(create_dummy_png)
    proc.resize_image(150, 100)
    info = proc.get_info()
    assert info["width"] == 150
    assert info["height"] == 100

def test_undo_action(create_dummy_png):
    proc = ImageProcessor()
    proc.load_image(create_dummy_png)
    assert proc.undo() is False
    proc.apply_blur()
    assert proc.undo() is True
    assert proc.previous_image is None