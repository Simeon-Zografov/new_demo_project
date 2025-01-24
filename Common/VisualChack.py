import math
import os
from io import BytesIO
import allure
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from pytest_check import check


def visual_comparison(driver, path, name):
    skip_mark = False
    driver.set_window_size(1280, 800)
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_iterations = math.ceil(full_page_height / 800) + 1
    for i in range(1, scroll_iterations):
        reference_image_path = os.path.join(project_folder, 'Visual', path, f'reference_screenshot_{name}_{i*800}.png')
        current_image_path = os.path.join(project_folder, 'Visual', path, f'current_screenshot_{name}_{i*800}.png')
        error_image_path = os.path.join(project_folder, 'Visual', path, f'error_screenshot_{name}_{i*800}.png')
        if os.path.exists(reference_image_path):
            driver.save_screenshot(current_image_path)
            current_image = Image.open(current_image_path)
            reference_image = Image.open(reference_image_path)
            img_diff = Image.new("RGBA", reference_image.size)
            mismatch = pixelmatch(reference_image, current_image, img_diff, includeAA=True)
            with check, allure.step(f"Visual check for {path} in {i} iteration"):
                if mismatch > 0:
                    img_diff.save(error_image_path)
                    buffer = BytesIO()
                    img_diff.save(buffer, format="PNG")
                    buffer.seek(0)
                    allure.attach(
                        buffer.getvalue(),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                assert mismatch == 0
        else:
            driver.save_screenshot(reference_image_path)
            skip_mark = True
        driver.execute_script("window.scrollBy(0, 800);")
    if skip_mark:
        pytest.skip("No reference screenshots found, skipping visual comparison test.")

