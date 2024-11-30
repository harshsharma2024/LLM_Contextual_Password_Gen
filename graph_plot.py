import matplotlib.pyplot as plt
from collections import defaultdict
import ast

def draw_train_password_variation():
    # Open and read the data file
    file = open("dict.txt", "r")
    password_length_counts = defaultdict(int)
    cnt = 0
    
    # Reading lines and counting password lengths
    for line in file:
        if cnt > 1000:
            break
        email, password = line.strip().split(" : ")
        # print(type(password))
        password = ast.literal_eval(password)
        length = len(password)
        # if(length == 3):
        #     print(password)
        password_length_counts[length] += 1
        cnt += 1

    # Prepare data for binning
    # remove entries from dictionary where length is greater than 100
    password_length_counts = {k: v for k, v in password_length_counts.items() if k <= 100}
    # print(password_length_counts[49]) 
    print(password_length_counts)
    bins = range(0, max(password_length_counts.keys()) + 10, 10)  # Binning in steps of 10
    binned_counts = defaultdict(int)

    # Bin the password lengths
    for length, count in password_length_counts.items():
        # Determine the correct bin for each length
        bin_start = (length // 10) * 10
        binned_counts[bin_start] += count

    # Prepare x and y for plotting
    x = list(binned_counts.keys())  # Binned ranges
    y = list(binned_counts.values())  # Frequencies of password lengths in those bins

    # Draw the bar chart
    plt.bar(x, y, width=8, color="skyblue", align='edge')
    plt.xlabel("Number of Passwords")
    plt.ylabel("Frequency")
    plt.title("Contextual Password Length Distribution")

    # Set labels for X-axis
    plt.xticks(x, [f"{i}-{i+9}" for i in x])  # Create labels like 0-9, 10-19, etc.

    # Add grid and limits
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(min(x)-1, max(x)+9)  # Adjust the X-axis range for better visibility
    plt.ylim(0, max(y) + 5)  # Extend the Y-axis slightly beyond the highest bar

    # Show the plot
    plt.show()

def read_and_process_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            # Remove the "defaultdict(None," part and closing parenthesis
            line = line.strip()
            line = line.replace("defaultdict(None, ", "").rstrip(")")

            # Parse the line into a Python dictionary
            try:
                data.append(ast.literal_eval(line))
            except Exception as e:
                print(f"Error parsing line: {line}")
                continue
        return data


def final_res_plot():
    # file = open("final_res.txt", "r")
    password_length_counts = defaultdict(int)
    file = read_and_process_file("final_res.txt")
    for line in file:
        # print(line)
        # print(type(line))
        # data = ast.literal_eval(line.strip())
        password_length_counts[len(line["passwords"])] += 1

    password_length_counts = {k: v for k, v in password_length_counts.items() if k <= 100}
    bins = range(0, max(password_length_counts.keys()) + 10, 10)
    binned_counts = defaultdict(int)

    for length, count in password_length_counts.items():
        bin_start = (length // 10) * 10
        binned_counts[bin_start] += count

    x = list(binned_counts.keys())
    y = list(binned_counts.values())

    plt.bar(x, y, width=8, color="skyblue", align='edge')
    plt.xlabel("Number of Passwords")
    plt.ylabel("Frequency")
    plt.title("Contextual Password Length Distribution(Guessed Passwords)")

    plt.xticks(x, [f"{i}-{i+9}" for i in x])

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xlim(min(x)-1, max(x)+9)
    plt.ylim(0, max(y) + 5)

    plt.show()



if __name__ == "__main__":
    draw_train_password_variation()

    # final_res_plot()
