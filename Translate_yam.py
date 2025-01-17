import yaml
from deep_translator import GoogleTranslator
import ruamel.yaml

def translate_to_russian(text):
    try:
        return GoogleTranslator(source='en', target='ru').translate(text)
    except Exception as e:
        print(f"Ошибка перевода текста: {text}. Ошибка: {e}")
        return text


# Рекурсивная функция для обхода всех элементов YAML
def traverse_yaml(data, level=1):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {'description', 'event_name'} and isinstance(value, str):
                #transl = translator.translate(value, src="en", dest="ru").text
                data[key] = translate_to_russian(value) 
                #print("  " * level + f"Ключ: {key}, Значение: {translate_to_russian(value)}")
            traverse_yaml(value, level + 1)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            traverse_yaml(item, level + 1)

# Кастомный Dumper для сохранения строк с одиночными кавычками
class CustomDumper(yaml.SafeDumper):
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style="'")

# Чтение YAML файла
file_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\Zabbix_Server_Health.yaml"
output_file_path = r"d:\Clouds\OneDrive - AVECTIS CJSC\Desktop\Test_Translate_Text\Zabbix_Server_Health_translate.yaml"

# Создание объекта YAML для настройки
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True  # Сохранять кавычки

# Открываем исходный YAML файл для чтения
with open(file_path, "r", encoding="utf-8") as file:
    yaml_data = yaml.load(file)

# Обход всех элементов
traverse_yaml(yaml_data)

#print(yaml_data)
# Открываем файл для записи
with open(output_file_path, "w", encoding="utf-8") as file:
    yaml.dump(yaml_data, file)

print(f"Переведённый файл сохранён по пути: {output_file_path}")