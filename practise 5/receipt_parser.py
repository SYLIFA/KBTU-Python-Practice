import re
import json

def parse_receipt(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Дата и Время (более гибкий поиск цифр через точки и двоеточия)
        date_time = re.search(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", content)
        
        # 2. ИТОГО (ищем число после слова ИТОГО, учитывая возможные пробелы и запятые)
        total = re.search(r"ИТОГО:?\s*[\n\s]*([\d\s]+[.,]\d{2})", content, re.IGNORECASE)
        
        # 3. Тип оплаты (ищем любые слова перед двоеточием в конце чека)
        # Если "банковских карт" нет, этот паттерн найдет то, что стоит на месте оплаты
        payment = re.search(r"([А-Яа-я\s]+):\s*\n?[\d\s]+[.,]\d{2}\s*\n?ИТОГО", content)

        # 4. Товары (универсальный паттерн: №. название \n кол-во x цена \n сумма)
        # Ищем паттерн: Число. Название [перенос] Цифры x Цифры [перенос] Сумма
        items = re.findall(r"\d+\.\n(.*?)\n[\d\s,]+x[\d\s,]+\n([\d\s,]+)", content, re.MULTILINE)

        result = {
            "Date": date_time.group(1) if date_time else "Not found",
            "Time": date_time.group(2) if date_time else "Not found",
            "Total_Sum": total.group(1).replace(" ", "").replace(",", ".") if total else "0.00",
            "Payment_Type": payment.group(1).strip() if payment else "Check raw text",
            "Items": []
        }

        for name, price in items:
            result["Items"].append({
                "Name": name.strip(),
                "Price": price.strip().replace(" ", "").replace(",", ".")
            })

        print(json.dumps(result, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Ошибка при чтении или парсинге: {e}")

parse_receipt("raw.txt")