import os
import pandas as pd
from last_dir import navigate_to_last_directory
from constants import confidence_threshold, a, b, c
from encryption_data import encrypt


def fail_case(question, barcode, bit, df):
    while True:
        print(f'Question {question} and Bit {bit} of barcode {barcode} are wrong!!!!')
        num = int(input("Enter the correct marks: "))
        user_input = input("Type OK to confirm.. ")
        if user_input == "OK":
            break
    if barcode in df['Barcode'].values:
        # If it is, update the corresponding cell with the confidence level
        df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num
    else:
        # If it's not, create a new row
        df._append({'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num},
                   ignore_index=True)
    return


def txt2excel(name):
    # Define the path to the labels folder
    start_path = "C:\\major-version1.0\\runs"
    labels_folder = navigate_to_last_directory(start_path)

    # Create a DataFrame to hold the data
    df = pd.DataFrame(
        columns=['S. No', 'Barcode'] + [f'Q{i}_Bit{j}' for i in range(1, 11) for j in range(1, 4)] + ['Sum'])

    filenames = sorted(os.listdir(labels_folder))

    # Iterate over the files in the labels folder
    for filename in filenames:
        # print("iter")
        if filename.endswith(".txt"):
            # print("iter1")
            # Extract the barcode and question info from the filename
            barcode = filename.split('_')[1].split("-")[0]
            # print(barcode)
            question_bit = filename.split('_')[2:4]
            print(question_bit)
            question = int(question_bit[0])
            print(question)
            bit = int(question_bit[1].split('.')[0])
            print(bit)

            # Read the label file and extract the confidence level
            with open(os.path.join(labels_folder, filename), 'r') as file:
                lines = file.readlines()
                line_count = len(lines)
                if line_count == 1:
                    for line in lines:
                        conf = float(line.split(" ")[5])
                        if conf >= confidence_threshold:
                            num = int(line.split(" ")[0])
                            # Check if the barcode is already in the DataFrame
                            if barcode in df['Barcode'].values:
                                # If it is, update the corresponding cell with the confidence level
                                df.loc[df['Barcode'] == barcode, f'Q{question}_Bit{bit}'] = num
                            else:
                                # If it's not, create a new row
                                df = df._append(
                                    {'S. No': len(df) + 1, 'Barcode': barcode, f'Q{question}_Bit{bit}': num},
                                    ignore_index=True)
                # elif line_count == 2:
                #     pass
                # class_id = float(file.read().split()[0])
                elif line_count >= 2:
                    # fail_case(question, barcode, bit, df=df)
                    pass

    df = df.fillna(0)
    # Calculate the sum for each row
    # for i in range(1, 11, 2):
    #     df['Sum'] = df[[f'Q{i}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
    #     df['Sum'] = df['Sum'].where(df['Sum'] > df[[f'Q{i+1}_Bit{j}' for j in range(1, 4)]].sum(axis=1), df[[f'Q{i+1}_Bit{j}' for j in range(1, 4)]].sum(axis=1))

    for i in range(1, 11, 2):
        sum1 = df[[f'Q{i}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
        sum2 = df[[f'Q{i + 1}_Bit{j}' for j in range(1, 4)]].sum(axis=1)
        df['Sum'] += sum1.where(sum1 > sum2, sum2)
    print(df)

    # Save the DataFrame to an Excel file that is created with excel
    df.to_excel(f'{name}.xlsx', index=False)

    # encrypt the code
    # encrypt(f'{name}.xlsx')
    # encrypt()

#  txt2excel("buhio")
