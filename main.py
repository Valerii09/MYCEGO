import os
from PIL import Image


def merge_images_from_folder(folder_name, output_file):
    images = []
    for filename in os.listdir(folder_name):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(folder_name, filename))
            images.append(img)
            print(f"Обработан файл: {filename}")

    if not images:
        print("Нет изображений для объединения")
        return

    try:
        images[0].save(output_file, save_all=True, append_images=images[1:])
        print(f"Изображения успешно объединены в файл {output_file}")
        return images  # Возвращаем список изображений
    except Exception as e:
        print(f"Ошибка при объединении изображений: {e}")
        return None


def create_collage(images, output_file, collage_size=(800, 800)):
    """
    Создает коллаж из списка изображений и сохраняет его в файл.

    :param images: Список объектов изображений PIL.Image
    :param output_file: Путь для сохранения коллажа
    :param collage_size: Размеры коллажа (ширина, высота)
    """
    # Определяем количество изображений
    num_images = len(images)

    # Вычисляем количество столбцов и строк в коллаже
    num_cols = int(num_images ** 0.5)
    num_rows = (num_images + num_cols - 1) // num_cols

    # Создаем пустое изображение для коллажа
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Рассчитываем размер каждого мини-изображения в коллаже
    mini_image_width = collage_size[0] // num_cols
    mini_image_height = collage_size[1] // num_rows

    # Ресайзим и добавляем каждое изображение в коллаж
    for i, img in enumerate(images):
        resized_img = img.resize((mini_image_width, mini_image_height), Image.LANCZOS)
        collage.paste(resized_img, (i % num_cols * mini_image_width, i // num_cols * mini_image_height))

    # Сохраняем коллаж
    collage.save(output_file)
    print(f"Коллаж успешно сохранен в файле: {output_file}")


# Папка с изображениями (используем относительный путь)
folder_name = 'image_pack/1369_12_Наклейки 3-D_3'

# Выходной файл
output_file = 'Result.tif'

# Объединяем изображения
images = merge_images_from_folder(folder_name, output_file)

# Проверяем, что изображения были успешно объединены
if images:
    # Создаем коллаж
    create_collage(images, "result2.tif")
