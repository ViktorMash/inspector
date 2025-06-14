import json
from pathlib import Path


def format_json_for_env(json_file, var_name="GOOGLE__SERVICE_ACCOUNT"):
    """Форматирует JSON-файл для использования в .env"""
    path = Path(json_file)

    if not path.exists():
        print(f"Ошибка: Файл не найден - {json_file}")
        return

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        # Преобразуем JSON в однострочный формат
        json_str = json.dumps(data, separators=(',', ':'))

        # Формируем строку для .env файла
        env_line = f"{var_name}={json_str}"

        print(env_line)

    except json.JSONDecodeError:
        print(f"Ошибка: Файл {json_file} не является валидным JSON")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    file_path = "../../service_acc/riki_intalev_google_sheets.json"
    var_name = "GOOGLE__SERVICE_ACCOUNT"

    format_json_for_env(file_path, var_name)