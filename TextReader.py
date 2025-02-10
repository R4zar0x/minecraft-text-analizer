import os
import cv2
import pyautogui
import pytesseract
import numpy as np

from processor import addiction

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class TextReader:
    def __init__(self, directory_for_screenshots: str = "data", screenshot_name: str = "test",
                 config: str = r'--tessdata-dir "traineddata/" --oem 3 --psm 6',
                 save_screenshots: bool = True, use_only_lover_letters: bool = True,
                 raw_data_function=None, processed_data_function=None, apply_data_function=None,
                 visibility_area: (int, int, int, int) = (0, 700, 700, 1000)
                 ):
        self.__directory_for_screenshots = directory_for_screenshots
        self.__screenshot_name = screenshot_name
        self.__config = config

        self.__save_screenshots = save_screenshots
        self.__use_only_lover_letters = use_only_lover_letters

        self.__raw_data_function = None
        if raw_data_function is not None:
            self.set_raw_data_function(raw_data_function)
        self.__processed_data_function = None
        if processed_data_function is not None:
            self.set_processed_data_function(processed_data_function)

        self.__visibility_area = visibility_area

    def __raw_data_processor(self, data):
        if self.__raw_data_function is not None:
            result = self.__raw_data_function(data)
            return result
        else:
            return None

    def __processed_data_processor(self, data):
        if self.__processed_data_function is not None:
            result = self.__processed_data_function(data)
            return result
        else:
            return None

    def __add_result_to_file(self, name, result):
        with open(f"{self.__directory_for_screenshots}/out.txt", 'a') as f:
            f.write(f"{name} {result}\n")

    @staticmethod
    def __make_screenshot():
        screenshot = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        return image

    def __crop_screenshot(self, image):
        x1, y1, x2, y2 = self.__visibility_area
        cropped_image = image[y1:y2, x1:x2]

        return cropped_image

    def __save_screenshot(self, image):

        if image is None:
            return "Error: image not exist"

        path = f"{self.__directory_for_screenshots}"
        if not os.path.exists(path):
            os.makedirs(path)

        num = 1
        while os.path.exists(f"{self.__directory_for_screenshots}/{self.__screenshot_name}{num}.png"):
            num += 1
        filename = f"{self.__directory_for_screenshots}/{self.__screenshot_name}{num}.png"

        cv2.imwrite(filename, image)
        print(f"Скриншот сохранен: {filename}")
        return f"{self.__screenshot_name}{num}.png"

    def __handle(self, image):
        cv2_image = addiction(image)

        data = pytesseract.image_to_string(cv2_image, lang='min', config=self.__config)
        if self.__use_only_lover_letters:
            data = data.lower()

        return data

    def __main(self):
        raw_image = self.__make_screenshot()
        crop_image = self.__crop_screenshot(raw_image)

        crop_image_copy = crop_image.copy()

        raw_data = self.__handle(crop_image)
        proc_data = self.__raw_data_processor(raw_data)
        end_status = self.__processed_data_processor(proc_data)
        print(end_status)

        if self.__save_screenshots:
            file_name = self.__save_screenshot(crop_image_copy)
            self.__add_result_to_file(file_name, proc_data)

    def run(self):
        self.__main()

    def set_raw_data_function(self, function):
        if function.__code__.co_argcount == 1:
            self.__raw_data_function = function
            return "Success"
        else:
            return f"Error: function \"{function.__name__}\" must have only 1 argument"

    def set_processed_data_function(self, function):
        if function.__code__.co_argcount == 1:
            self.__processed_data_function = function
            return "Success"
        else:
            return f"Error: function \"{function.__name__}\" must have only 1 argument"

    def set_default_directory(self):
        self.__directory_for_screenshots = "data"

    def set_defaults_screenshot_name(self):
        self.__screenshot_name = "test"

    def set_defaults_config(self):
        self.__config = r'--tessdata-dir "traineddata/" --oem 3 --psm 6'

    def set_directory(self, path: str):
        self.__directory_for_screenshots = path.rstrip('\\/')

    def set_screenshot_name(self, name: str):
        self.__screenshot_name = name

    def set_config(self, config: str):
        self.__config = config

    def set_visibility_area(self, values: (int, int, int, int)):
        self.__visibility_area = values

    def save_screenshots(self):
        self.__save_screenshots = True

    def dont_save_screenshots(self):
        self.__save_screenshots = False

    def use_only_lower_letters(self):
        self.__use_only_lover_letters = True

    def dont_use_only_lower_letters(self):
        self.__use_only_lover_letters = False

