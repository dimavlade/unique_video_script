import subprocess
import sys
import argparse
import random
import os
from moviepy.editor import VideoFileClip, vfx


def adjust_video(input_path, output_path):
    # Случайные значения для параметров от 1 до 2%
    speed_factor = 1 + random.uniform(0.01, 0.1)
    brightness_factor = 1 + random.uniform(0.01, 0.1)
    contrast_factor = random.uniform(0.01, 0.1)
    volume_factor = 1 + random.uniform(0.01, 0.1)

    # Процентные значения для лога
    speed_percentage = (speed_factor - 1) * 100
    brightness_percentage = (brightness_factor - 1) * 100
    contrast_percentage = contrast_factor * 100
    volume_percentage = (volume_factor - 1) * 100

    # Вывод сгенерированных параметров
    print(f"Сгенерированные параметры для {os.path.basename(input_path)}:")
    print(f"Коэффициент ускорения видео: {speed_percentage:.0f}%")
    print(f"Коэффициент увеличения яркости: {brightness_percentage:.0f}%")
    print(f"Коэффициент увеличения контрастности: {contrast_percentage:.0f}%")
    print(f"Коэффициент увеличения громкости: {volume_percentage:.0f}%")

    try:
        # Загрузка видеофайла
        video = VideoFileClip(input_path)

        # Ускорение видео
        video = video.fx(vfx.speedx, speed_factor)

        # Регулировка яркости и контрастности
        video = video.fx(vfx.colorx, brightness_factor)
        video = video.fx(vfx.lum_contrast, lum=0, contrast=contrast_factor)

        # Ускорение и увеличение громкости аудио
        if video.audio is not None:
            video.audio = video.audio.fx(vfx.speedx, speed_factor)
            video.audio = video.audio.volumex(volume_factor)

        # Сохранение результата в выходной файл
        video.write_videofile(output_path, threads=64, verbose=False, codec="h264_nvenc")
        # Закрытие видео для освобождения ресурсов
        video.close()
        
        return True
    except Exception as e:
        print(f"Ошибка при обработке видео {input_path}: {str(e)}")
        return False


def extract_video_names(video_files, output_txt):
    """Извлекает имена видеофайлов и сохраняет их в текстовый файл"""
    try:
        with open(output_txt, 'w', encoding='utf-8') as f:
            for video_file in video_files:
                # Получаем имя файла без расширения
                video_name = os.path.splitext(os.path.basename(video_file))[0]
                f.write(f"{video_name}\n")
        print(f"Имена видео сохранены в {output_txt}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении имен видео: {str(e)}")
        return False


def process_video_folder(input_folder, output_folder, txt_file):
    """Обрабатывает все видеофайлы в указанной папке"""
    # Создаем выходную папку, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Создана папка для выходных файлов: {output_folder}")
    
    # Список поддерживаемых расширений видеофайлов
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    
    # Получаем список всех видеофайлов в папке
    video_files = []
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in video_extensions:
            video_files.append(file_path)
    
    if not video_files:
        print(f"В папке {input_folder} не найдено видеофайлов")
        return
    
    print(f"Найдено {len(video_files)} видеофайлов для обработки")
    
    # Сохраняем имена видео в текстовый файл
    extract_video_names(video_files, txt_file)
    
    # Обрабатываем каждый видеофайл
    successful = 0
    for video_file in video_files:
        filename = os.path.basename(video_file)
        output_path = os.path.join(output_folder, filename)
        
        print(f"\nОбработка файла: {filename}")
        if adjust_video(video_file, output_path):
            successful += 1
    
    print(f"\nОбработка завершена. Успешно обработано {successful} из {len(video_files)} файлов.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Уникализация видео через изменение скорости, яркости, контрастности и громкости видео."
    )
    parser.add_argument("input_path", type=str, 
                        help="Путь к входной папке с видеофайлами или к отдельному видеофайлу.")
    parser.add_argument("--output_folder", type=str, default=None,
                        help="Путь к выходной папке для обработанных видео. По умолчанию создается папка 'processed' в текущей директории.")
    parser.add_argument("--txt_file", type=str, default="video_names.txt",
                        help="Путь к текстовому файлу для сохранения имен видео. По умолчанию 'video_names.txt'.")

    args = parser.parse_args()

    # Проверяем, является ли входной путь файлом или папкой
    if os.path.isfile(args.input_path):
        # Если это файл, обрабатываем его как раньше
        if args.output_folder is None:
            output_dir = "processed"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            output_dir = args.output_folder
            
        output_file = os.path.join(output_dir, os.path.basename(args.input_path))
        
        # Сохраняем имя видео в текстовый файл
        with open(args.txt_file, 'w', encoding='utf-8') as f:
            video_name = os.path.splitext(os.path.basename(args.input_path))[0]
            f.write(f"{video_name}\n")
            
        print(f"Обработка одиночного файла: {args.input_path}")
        adjust_video(args.input_path, output_file)
    else:
        # Если это папка, обрабатываем все видео в ней
        if args.output_folder is None:
            output_dir = os.path.join(os.path.dirname(args.input_path), "processed")
        else:
            output_dir = args.output_folder
            
        process_video_folder(args.input_path, output_dir, args.txt_file)
