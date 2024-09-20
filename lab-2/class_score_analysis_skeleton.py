def read_data(filename):
    csv_data = []
    try:
        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                # Skip comment or header lines
                if line.startswith("#"):
                    continue
                try:
                    # Split the line by comma, strip whitespace, and convert to integers
                    midterm, final = map(int, line.strip().split(","))
                    csv_data.append((midterm, final))
                except ValueError:
                    print(f"Skipping invalid data: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return csv_data


def calc_weighted_average(data_2d, weight):
    weighted_average = []

    for row in data_2d:
        try:
            weighted_sum = (row[0] * weight[0]) + (row[1] * weight[1])
            weighted_average.append(weighted_sum)
        except Exception as e:
            print(f"An error occurred with data {row}: {e}")

    return weighted_average


def analyze_data(data_1d):
    mean_calculated = sum(data_1d) / len(data_1d)
    var_calculated = sum((x - mean_calculated) ** 2 for x in data_1d) / len(data_1d)
    sorted_data = sorted(data_1d)
    n = len(sorted_data)
    if n % 2 == 1:
        # If odd, take the middle element
        median_calculated = sorted_data[n // 2]
    else:
        # If even, take the average of the two middle elements
        median_calculated = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    return mean_calculated, var_calculated, median_calculated, min(data_1d), max(data_1d)


if __name__ == "__main__":
    data = read_data("./data/class_score_en.csv")
    if data and len(data[0]) == 2:  # Check 'data' is valid
        average = calc_weighted_average(data, [40 / 125, 60 / 100])

        # Write the analysis report as a markdown file
        with open("class_score_analysis.md", "w", encoding='utf-8') as report:
            report.write("### Individual Score\n\n")
            report.write("| Midterm | Final | Average |\n")
            report.write("| ------- | ----- | ----- |\n")
            for (m_score, f_score), a_score in zip(data, average):
                report.write(f"| {m_score} | {f_score} | {a_score:.3f} |\n")
            report.write("\n\n\n")

            report.write("### Examination Analysis\n")
            data_columns = {
                "Midterm": [m_score for m_score, _ in data],
                "Final": [f_score for _, f_score in data],
                "Average": average,
            }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f"* {name}\n")
                report.write(f"  * Mean: **{mean:.3f}**\n")
                report.write(f"  * Variance: {var:.3f}\n")
                report.write(f"  * Median: **{median:.3f}**\n")
                report.write(f"  * Min/Max: ({min_:.3f}, {max_:.3f})\n")
