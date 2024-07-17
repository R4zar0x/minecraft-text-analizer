import os
import time

import cv2
import keyboard
import pyautogui
import pytesseract

import numpy as np

from analiser import addiction

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

run = False


def handle(image):
    cv2_image = addiction(image)

    config = r'--tessdata-dir "traineddata/" --oem 3 --psm 6'
    # config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_string(cv2_image, lang='min', config=config)

    data = data.lower()

    if "решите" in data or "пример" in data:
        first_index = data.find("решите пример")
        last_index = data.find("кто")
        # last_index = data.find("\n")

        substring = data[first_index:last_index]
        substring = substring.split()

        summ = 0

        for element in substring:
            if element.isdigit():
                print(element)
                summ += int(element)
        print("сумма: ", summ)

        return summ
    else:
        return None


def enter_summ(value, chat_is_open=False):
    if not chat_is_open:
        keyboard.press_and_release('t')
        time.sleep(0.8)

    number_str = str(value)
    for digit in number_str:
        if digit.isdigit():
            keyboard.press_and_release(digit)
            time.sleep(0.2)
    time.sleep(0.2)
    keyboard.press_and_release('enter')


def make_screenshot():
    screenshot = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Определяем координаты обрезки (например, сверху слева (x1, y1) до снизу справа (x2, y2))
    x1, y1, x2, y2 = 0, 700, 700, 1000

    # Обрезаем изображение
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image


def save_clipboard_image():
    # Получаем скриншот из буфера обмена
    cropped_image = make_screenshot()

    if cropped_image is not None:
        # Определяем имя файла для сохранения с учетом порядкового номера
        num = 1
        while os.path.exists(f"test{num}.png"):
            num += 1
        filename = f"test{num}.png"

        # Сохраняем скриншот в файл
        cv2.imwrite(filename, cropped_image)
        print(f"Скриншот сохранен как {filename}")
        return filename
    else:
        print("Буфер обмена не содержит изображения")
        return None


def handle_data(chat_is_open=False):
    saved_filename = save_clipboard_image()
    if not saved_filename:
        print("В буфере обмена нет изображения")
        return

    summ = handle(cv2.imread(saved_filename))

    if summ:
        enter_summ(summ, chat_is_open)
    else:
        print("не найден пример")

    print("конец")


def ctrl_tab():
    handle_data(False)


def shift_tab():
    handle_data(True)


def end_run():
    global run
    run = False


def main():
    global run
    run = True

    print("анализирует экран с игрой, и если найдет там пример, посчитает его;\n"
          "shift+tab - чат уже открыт\n"
          "ctrl+tab - чат закрыт\n"
          "alt+q - выход")

    keyboard.add_hotkey('shift+tab', shift_tab)
    keyboard.add_hotkey('ctrl+tab', ctrl_tab)
    keyboard.add_hotkey('alt+q', end_run)

    while run:
        # pass
        time.sleep(0.1)  # Задержка в 0.1 секунды


if __name__ == "__main__":
    main()
