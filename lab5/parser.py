import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d[\d ]*,\d{2}", text)

m_total = re.search(r"ИТОГО:\s*\n?\s*([\d ]+,\d{2})", text)
total = m_total.group(1) if m_total else None

m_time = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = m_time.group(1) if m_time else None
time = m_time.group(2) if m_time else None

m_pay = re.search(r"(Банковская карта|Наличные|Карта)", text)
payment_method = m_pay.group(1) if m_pay else None

data = {
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))
