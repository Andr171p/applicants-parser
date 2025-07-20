

education_price = "199\xa0127\xa0\xa0₽/год"

total_places = "60\xa0мест"

print(float("".join(filter(str.isdigit, total_places.strip()))))
