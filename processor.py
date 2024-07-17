import numpy as np
import cv2


def binary_activation_rgb(image):
    # Создаем маску, где белые пиксели будут True, а все остальные False
    white_mask = np.all(image == [255, 255, 255], axis=-1)

    # Создаем новое изображение, полностью черное
    result = np.zeros_like(image)

    # Применяем маску: где True (белые пиксели), оставляем белый цвет
    result[white_mask] = [255, 255, 255]

    return result


def make_red_mask(hsv, lover_Saturation, upper_Saturation, lover_Value, upper_Value):
    lower_red = np.array([0, lover_Value, lover_Saturation])  # [0, 200, 150]
    upper_red = np.array([10, upper_Value, upper_Saturation])  # [10, 255, 255]
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, lover_Value, lover_Saturation])  # [170, 200, 150]
    upper_red = np.array([180, upper_Value, upper_Saturation])  # [180, 255, 255]
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    return mask1 + mask2


def replace_red_with_white(image):
    # Преобразование изображения из BGR в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = make_red_mask(hsv, 230, 255, 160, 255)

    # Замена красного на белый
    image[mask > 0] = [255, 255, 255]

    return image


def replace_yellow_with_white(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 150, 200])
    upper_yellow = np.array([45, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    image[mask > 0] = [255, 255, 255]

    return image


def addiction(image):
    image = replace_red_with_white(image)
    image = replace_yellow_with_white(image)
    image = binary_activation_rgb(image)
    return image