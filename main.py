import os
from PIL import Image

class ImageCollageCreator:
    def __init__(self, folder_name, padding=70, border_size=100, border_color=(255, 255, 255)):
        self.folder_name = folder_name
        self.padding = padding
        self.border_size = border_size
        self.border_color = border_color

    def merge_images_from_folder(self, folder_name):
        images = []
        for filename in os.listdir(folder_name):
            if filename.endswith(".png"):
                img = Image.open(os.path.join(folder_name, filename))
                images.append(img)
                print(f"Обработан файл: {filename}")

        if not images:
            print("Нет изображений для объединения")
            return None

        return images

    def create_collage(self, images, output_file):
        """
        Создает коллаж из списка изображений и сохраняет его в файл.

        :param images: Список объектов изображений PIL.Image
        :param output_file: Путь для сохранения коллажа
        """
        # Определяем количество изображений
        num_images = len(images)

        # Рассчитываем количество столбцов и строк в коллаже
        num_rows = 2  # Две строки
        num_cols = (num_images + num_rows - 1) // num_rows

        # Вычисляем общий размер коллажа
        collage_width = max(img.width for img in images) * num_cols + (num_cols - 1) * self.padding + 5 * self.border_size
        collage_height = max(img.height for img in images) * num_rows + (num_rows - 1) * self.padding + 5 * self.border_size

        # Создаем пустое изображение для коллажа
        collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

        # Добавляем изображения в коллаж
        for i, img in enumerate(images):
            col = i % num_cols
            row = i // num_cols

            x = col * (img.width + self.padding) + self.border_size
            y = row * (img.height + self.padding) + self.border_size

            # Создаем рамку вокруг изображения
            bordered_img = Image.new('RGB', (img.width + 2 * self.border_size, img.height + 2 * self.border_size), self.border_color)
            bordered_img.paste(img, (self.border_size, self.border_size))

            collage.paste(bordered_img, (x, y))

        # Сохраняем коллаж
        collage.save(output_file)
        print(f"Коллаж успешно сохранен в файле: {output_file}")

    def process_folders(self):
        for folder in os.listdir(self.folder_name):
            folder_path = os.path.join(self.folder_name, folder)
            if os.path.isdir(folder_path):
                result_folder = os.path.join(folder_path, f"{folder}_results")
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)  # Создаем папку, если ее нет
                images = self.merge_images_from_folder(folder_path)
                if images:
                    result_file = os.path.join(result_folder, "result.tif")
                    self.create_collage(images, result_file)


# Папка с изображениями (используем относительный путь)
folder_name = 'image_pack'

# Создаем экземпляр класса и выполняем объединение и создание коллажей для всех папок внутри image_pack
collage_creator = ImageCollageCreator(folder_name)
collage_creator.process_folders()
