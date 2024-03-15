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
    except Exception as e:
        print(f"Ошибка при объединении изображений: {e}")

# Папка с изображениями (используем относительный путь)
folder_name = 'image_pack/1369_12_Наклейки 3-D_3'

# Выходной файл
output_file = 'Result.tif'

# Объединяем изображения
merge_images_from_folder(folder_name, output_file)
