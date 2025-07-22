import polars as pl

file_path = r"C:\Users\andre\ApplicantEye\assets\applicants\Юриспруденция.2025-07-22_20-17-30.csv"

df = pl.read_csv(file_path)

'''for row in df.iter_rows():
    print(row)
    break'''

r = ('1;4380481;3;"—";0;"91 94 87";5;"Ожидаются результаты испытаний";"10.07.2025 в 09:30"',)

print(list(map(lambda x: x.replace('"', ''), r[0].split(";"))))
