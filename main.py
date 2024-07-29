import time
import keyboard

import TextReader

run = True


def raw_processor(data):
    if "решите" in data or "пример" in data:
        first_index = data.find("решите пример")
        last_index = data.find("кто")

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


def post_processor_ctrl_tab(data):
    if data is None:
        return "postprocessor: No summ"

    if data == 0:
        return "postprocessor: Zero"

    keyboard.press_and_release('t')
    time.sleep(0.5)

    number_str = str(data)
    for digit in number_str:
        if digit.isdigit():
            keyboard.press_and_release(digit)
            time.sleep(0.1)
    time.sleep(0.2)
    keyboard.press_and_release('enter')

    return "postprocessor: Success"


def post_processor_shift_tab(data):
    if data is None:
        return "postprocessor: No summ"

    if data == 0:
        return "postprocessor: Zero"

    number_str = str(data)
    for digit in number_str:
        if digit.isdigit():
            keyboard.press_and_release(digit)
            time.sleep(0.1)
    time.sleep(0.2)
    keyboard.press_and_release('enter')

    return "postprocessor: Success"


def end_run():
    global run
    run = False


def main():
    print("анализирует экран с игрой, и если найдет там пример, посчитает его;\n"
          "ctrl+tab - чат закрыт\n"
          "shift+tab - чат уже открыт\n"
          "alt+q - выход")
    global run
    run = True

    analyzer_ctrl = TextReader.TextReader()
    analyzer_ctrl.set_directory("obj_data")
    analyzer_ctrl.set_raw_data_function(raw_processor)
    analyzer_ctrl.set_processed_data_function(post_processor_ctrl_tab)

    analyzer_shift = TextReader.TextReader()
    analyzer_shift.set_directory("obj_data")
    analyzer_shift.set_raw_data_function(raw_processor)
    analyzer_shift.set_processed_data_function(post_processor_shift_tab)

    keyboard.add_hotkey('ctrl+tab', analyzer_ctrl.run)
    keyboard.add_hotkey('shift+tab', analyzer_shift.run)
    keyboard.add_hotkey('alt+q', end_run)

    while run:
        time.sleep(0.1)  # Задержка в 0.1 секунды


if __name__ == "__main__":
    main()
