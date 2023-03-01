import openai
import csv
from urllib.parse import quote

# Устанавливаем ключи аутентификации
openai.api_key = "API_KEY"

# Функция для оценки тональности отзыва
def rate_review(review_text):
    model_engine = "text-davinci-002"
    prompt = (f"Please rate the following review on a scale of 1 to 10, where 1 is the most negative and 10 is the most positive.\n"
              f"Review: {quote(review_text)}\n"
              f"Rating:")
    response = openai.Completion.create(
      engine=model_engine,
      prompt=prompt,
      max_tokens=1,
      n=1,
      stop=None,
      temperature=0.5,
    )
    rating = int(response.choices[0].text.strip())
    return rating



# Имя файла с данными
filename = "reviews.csv"

# Открываем файл с данными
with open(filename, "r") as f:
    reader = csv.reader(f)
    header = next(reader)

    # Извлекаем данные из файла
    rows = list(reader)

    # Добавляем оценку к каждому отзыву
    for row in rows:
        review_text = row[1]
        rating = rate_review(review_text)
        row.append(str(rating))

    # Сортируем отзывы по убыванию оценки
    sorted_rows = sorted(rows, key=lambda x: int(x[4]), reverse=True)

    # Создаем новый файл для записи результатов
    new_filename = filename.split(".")[0] + "_analyzed.csv"
    with open(new_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in sorted_rows:
            writer.writerow([row[0], row[1], row[2], row[4]])

    print(f"Результаты анализа сохранены в файле {new_filename} в той же директории, что и исходный файл.")
