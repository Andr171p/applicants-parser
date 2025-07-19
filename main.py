

education_price = "199\xa0127\xa0\xa0₽/год"

print(float("".join(filter(str.isdigit, education_price.strip()))))
