def normalize_data(n_cases, n_people, scale):
    norm_cases = []
    for i in range(len(n_cases)):
        norm_cases.append(n_cases[i] / n_people[i] * scale)
    return norm_cases


regions = [
    "Seoul",
    "Gyeongi",
    "Busan",
    "Gyeongnam",
    "Incheon",
    "Gyeongbuk",
    "Daegu",
    "Chungnam",
    "Jeonnam",
    "Jeonbuk",
    "Chungbuk",
    "Gangwon",
    "Daejeon",
    "Gwangju",
    "Ulsan",
    "Jeju",
    "Sejong",
]
n_people = [
    9550227,
    13530519,
    3359527,
    3322373,
    2938429,
    2630254,
    2393626,
    2118183,
    1838353,
    1792476,
    1597179,
    1536270,
    1454679,
    1441970,
    1124459,
    675883,
    365309,
]  # 2021-08
n_covid = [
    644,
    529,
    38,
    29,
    148,
    28,
    41,
    62,
    23,
    27,
    27,
    33,
    16,
    40,
    20,
    5,
    4,
]  # 2021-09-21

sum_people = sum(n_people)  # The total number of people
sum_covid = sum(n_covid)  # The total number of new cases
norm_covid = normalize_data(
    n_covid, n_people, 1000000
)  # The new cases per 1 million people

# Print population by region
print("### Korean Population by Region")
print(f"* Total population: {sum_people}\n")
print("| Region | Population | Ratio (%) |")
print("| ------ | ---------- | --------- |")
for idx, pop in enumerate(n_people):
    ratio = pop / sum_people * 100
    print(f"| {regions[idx]} | {pop} | {ratio:.1f} |")
print("\n")

# Print COVID-19 new cases by region
print("### Korean COVID-19 New Cases by Region")
print(f"* Total new cases: {sum_covid}\n")
print("| Region | New Cases | Ratio (%) | New cases / 1M |")
print("| ------ | ---------- | --------- | -------------- |")
for idx, cases in enumerate(n_covid):
    ratio = cases / sum_covid * 100
    print(f"| {regions[idx]} | {cases} | {ratio:.1f} | {norm_covid[idx]:.1f} |")
print("\n")

try:
    with open('covid19_statistics.md', 'w', encoding='utf-8') as f:
        # Print population by region
        f.write("### Korean Population by Region\n")
        f.write(f"* Total population: {sum_people}\n\n")
        f.write("| Region | Population | Ratio (%) |\n")
        f.write("| ------ | ---------- | --------- |\n")
        for idx, pop in enumerate(n_people):
            ratio = pop / sum_people * 100
            f.write(f"| {regions[idx]} | {pop} | {ratio:.1f} |\n")
        f.write("\n")

        # Print COVID-19 new cases by region
        f.write("### Korean COVID-19 New Cases by Region\n")
        f.write(f"* Total new cases: {sum_covid}\n\n")
        f.write("| Region | New Cases | Ratio (%) | New cases / 1M |\n")
        f.write("| ------ | ---------- | --------- | -------------- |\n")
        for idx, cases in enumerate(n_covid):
            ratio = cases / sum_covid * 100
            f.write(
                f"| {regions[idx]} | {cases} | {ratio:.1f} | {norm_covid[idx]:.1f} |\n")
        f.write("\n")
except IOError as e:
    print(f"An error occurred while writing to the file: {e}")
else:
    print("The results are saved in covid19_statistics.md")
