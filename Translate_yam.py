import yaml
import re
import asyncio
from aiogoogletrans import Translator  # Используем асинхронный форк библиотеки googletrans

# Функция для асинхронного перевода текста с учётом исключений для {$...}
async def translate_to_russian(text, translator):
    # Асинхронная функция для замены текста
    async def replace_func(match):
        if match.group(0).startswith("{$"):
            return match.group(0)  # Оставляем макросы без изменений
        else:
            translated = await translator.translate(match.group(0), src="en", dest="ru")
            return translated.text

    # Перебираем все совпадения и переводим
    tasks = [replace_func(match) for match in re.finditer(r'\{[^}]+\}|\b.*?\b', text)]
    translated_parts = await asyncio.gather(*tasks)  # Асинхронно ждём выполнения всех переводов

    # Соединяем переведённый текст
    return ''.join(translated_parts)

# Асинхронная рекурсивная обработка YAML-данных
async def process_dict_with_translation(data, translator):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {"name", "description", "expression", "event_name"} and isinstance(value, str):
                data[key] = await translate_to_russian(value, translator)
            elif isinstance(value, (dict, list)):
                await process_dict_with_translation(value, translator)
    elif isinstance(data, list):
        for item in data:
            await process_dict_with_translation(item, translator)

# Основная функция для обработки файла
async def main():
    input_file_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\zbx_export_templates.yaml"
    output_file_translated_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\zbx_export_templates_translate.yaml"

    # Инициализация переводчика
    translator = Translator(timeout=10)

    # Чтение YAML файла
    with open(input_file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    # Перевод данных
    await process_dict_with_translation(yaml_data, translator)

    # Запись переведённого YAML в файл
    with open(output_file_translated_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(yaml_data, file, allow_unicode=True)

    print(f"Переведённый файл сохранён по пути: {output_file_translated_path}")

# Запуск программы
asyncio.run(main())

