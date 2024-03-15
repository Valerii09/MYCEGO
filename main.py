import os
from PIL import Image

class ImageCollageCreator:
    def __init__(self, folder_name, padding=70, border_size=100, border_color=(255, 255, 255)):
        """
        Создает экземпляр класса ImageCollageCreator.

        :param folder_name: Имя папки с изображениями.
        :param padding: Отступ между изображениями в коллаже (по умолчанию 70 пикселей).
        :param border_size: Размер рамки вокруг изображений (по умолчанию 100 пикселей).
        :param border_color: Цвет рамки в формате RGB (по умолчанию белый).
        """
        self.folder_name = folder_name
        self.padding = padding
        self.border_size = border_size
        self.border_color = border_color

    def _get_images_from_folder(self, folder_path):
        """
        Получает список изображений из указанной папки.

        :param folder_path: Путь к папке с изображениями.
        :return: Список объектов изображений PIL.Image.
        """
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                img = Image.open(os.path.join(folder_path, filename))
                images.append(img)
                print(f"Processed file: {filename}")
        return images

    def _create_bordered_image(self, img):
        """
        Создает изображение с рамкой вокруг указанного изображения.

        :param img: Объект изображения PIL.Image.
        :return: Изображение с рамкой.
        """
        bordered_img = Image.new('RGB', (img.width + 2 * self.border_size, img.height + 2 * self.border_size), self.border_color)
        bordered_img.paste(img, (self.border_size, self.border_size))
        return bordered_img

    def create_collage(self, images, output_file):
        """
        Создает коллаж из списка изображений и сохраняет его в файл.

        :param images: Список объектов изображений PIL.Image.
        :param output_file: Путь для сохранения коллажа.
        """
        num_images = len(images)
        num_rows = 2
        num_cols = (num_images + num_rows - 1) // num_rows

        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)

        collage_width = max_width * num_cols + (num_cols - 1) * self.padding + 5 * self.border_size
        collage_height = max_height * num_rows + (num_rows - 1) * self.padding + 5 * self.border_size

        collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

        for i, img in enumerate(images):
            col = i % num_cols
            row = i // num_cols

            x = col * (max_width + self.padding) + self.border_size
            y = row * (max_height + self.padding) + self.border_size

            bordered_img = self._create_bordered_image(img)

            collage.paste(bordered_img, (x, y))

        collage.save(output_file)
        print(f"Collage successfully saved to: {output_file}")

    def process_folders(self):
        """
        Обрабатывает все папки внутри указанной папки и создает коллажи для каждой папки.
        """
        for folder in os.listdir(self.folder_name):
            folder_path = os.path.join(self.folder_name, folder)
            if os.path.isdir(folder_path):
                result_folder = os.path.join(folder_path, f"{folder}_results")
                os.makedirs(result_folder, exist_ok=True)

                images = self._get_images_from_folder(folder_path)
                if images:
                    result_file = os.path.join(result_folder, "result.tif")
                    self.create_collage(images, result_file)

# Image folder (using relative path)
folder_name = 'image_pack'

# Создаем экземпляр класса и выполняем объединение и создание коллажей для всех папок внутри image_pack
collage_creator = ImageCollageCreator(folder_name)
collage_creator.process_folders()