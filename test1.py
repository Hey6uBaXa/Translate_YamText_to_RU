import yaml
from deep_translator import GoogleTranslator

# Функция для перевода текста
def translate_to_russian(text):
    try:
        return GoogleTranslator(source='en', target='ru').translate(text)
    except Exception as e:
        print(f"Ошибка перевода текста: {text}. Ошибка: {e}")
        return text

# Рекурсивная функция для обработки YAML
def traverse_yaml(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {'name', 'description', 'expression', 'event_name'} and isinstance(value, str):
                data[key] = translate_to_russian(value)  # Переводим текст
            elif isinstance(value, (dict, list)):
                traverse_yaml(value)  # Рекурсивно обрабатываем вложенные структуры
    elif isinstance(data, list):
        for item in data:
            traverse_yaml(item)  # Рекурсивно обрабатываем элементы списка

# Кастомный Dumper для сохранения строк с одиночными кавычками
class CustomDumper(yaml.SafeDumper):
    def represent_str(self, data):
        # Принудительно используем одиночные кавычки для всех строк
        return self.represent_scalar('tag:yaml.org,2002:str', data, style="'")

# Пути к файлам
file_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\test.yaml"
output_file_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\test_translate.yaml"

# Чтение YAML файла
with open(file_path, "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)

# Обработка всех элементов
traverse_yaml(yaml_data)

# Сохранение переведённого YAML
with open(output_file_path, "w", encoding="utf-8") as file:
    yaml.dump(yaml_data, file, allow_unicode=True, Dumper=CustomDumper)

print(f"Переведённый файл сохранён по пути: {output_file_path}")
