import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # Plot midterm/final scores as points
    plt.figure(figsize=(10, 5))
    plt.scatter(midterm_kr, final_kr, color='red', label='Korean Class', marker='o')
    plt.scatter(midterm_en, final_en, color='blue', label='English Class', marker='+')
    plt.xlabel('Midterm Scores')
    plt.ylabel('Final Scores')
    plt.title('Midterm vs Final Scores')
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    plt.legend()
    plt.savefig('class_score_scatter.png')
    plt.show()  # Show the scatter plot
    plt.close()

    # Plot total scores as a histogram
    plt.figure(figsize=(10, 5))
    plt.hist(total_kr, bins=range(0, 105, 5), alpha=0.5, label='Korean Class', color='red')
    plt.hist(total_en, bins=range(0, 105, 5), alpha=0.5, label='English Class', color='blue')
    plt.xlabel('Total Scores')
    plt.ylabel('Number of Students')
    plt.title('Total Scores Distribution')
    plt.xlim(0, 100)
    plt.legend()
    plt.savefig('class_score_hist.png')
    plt.show()  # Show the histogram
    plt.close()
