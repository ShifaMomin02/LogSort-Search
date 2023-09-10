import os
from datetime import datetime

def get_all_files_in_directory(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        return content

def write_sorted_logs(sorted_logs, output_file):
    with open(output_file, 'a') as file:
        for log in sorted_logs:
            file.write(log)

def binary_search(sorted_logs, start_date, end_date):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    start_index = 0
    end_index = len(sorted_logs) - 1

    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2
        mid_date_time = datetime.strptime(sorted_logs[mid_index].split('.')[0], '%Y-%m-%dT%H:%M:%S')

        if start_datetime <= mid_date_time <= end_datetime:
            # Mid date falls within the specified range, so search both sides
            start_date_index = mid_index
            end_date_index = mid_index
            while start_date_index > start_index and datetime.strptime(sorted_logs[start_date_index - 1].split('.')[0], '%Y-%m-%dT%H:%M:%S') >= start_datetime:
                start_date_index -= 1
            while end_date_index < end_index and datetime.strptime(sorted_logs[end_date_index + 1].split('.')[0], '%Y-%m-%dT%H:%M:%S') <= end_datetime:
                end_date_index += 1
            return sorted_logs[start_date_index:end_date_index + 1]

        elif mid_date_time < start_datetime:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1

    # If no matching logs found within the specified range, return None
    return None

def search_logs():
    # Get the directory from the user
    directory = input("Enter the directory path: ")
    
    # Get all the files in the directory
    all_files = get_all_files_in_directory(directory)

    # Read the contents of each file and count the logs
    logs = []
    file_log_counts = {}  # To store the log counts for each file
    total_logs_count = 0  # Total count of logs

    for file_path in all_files:
        file_logs = read_file(file_path)
        logs.extend(file_logs)
        file_log_counts[file_path] = len(file_logs)
        total_logs_count += len(file_logs)

    #Sort the logs by date and time
    logs.sort()
    sorted_logs = logs

    # Show number of logs in each file
    print("Number of logs in each file:")
    for file_path, log_count in file_log_counts.items():
        print(f"{file_path}: {log_count} logs")

    # Ask for the new file name for the sorted list
    sorted_file_name = input("\nEnter the new file name for the sorted list (without extension): ")
    default_file_name = "Sorted_Logs"

    if sorted_file_name:
        output_file_name = sorted_file_name
    else:
        output_file_name = default_file_name

    output_file = os.path.join(directory, "../", f"{output_file_name}.txt")

    # Write the sorted logs to the output file
    write_sorted_logs(sorted_logs, output_file)
    print("\nLogs have been sorted and saved in", output_file)

    # Show the new sorted file
    print("\nSorted Logs:")
    for log in sorted_logs:
        print(log)

    with open(output_file, 'r') as file:
        num_logs_in_sorted_file = len(file.readlines())  # Count the number of lines (logs)

    print(f"Total number of logs in the sorted file are: {num_logs_in_sorted_file}")

    while True:
        # Search option for sorted logs
        print("\nSearch option for sorted logs:")
        default_start_date = datetime.strptime(sorted_logs[0].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        default_end_date = datetime.strptime(sorted_logs[-1].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        start_date = input("Enter the start date and time (YYYY-MM-DD HH:mm:ss): ")
        
        # Use the default start date if the user input is empty
        if not start_date:
            start_date = default_start_date.strftime('%Y-%m-%d %H:%M:%S')

        end_date = input("Enter the end date and time (YYYY-MM-DD HH:mm:ss): ")
        if not end_date:
            end_date = default_end_date.strftime('%Y-%m-%d %H:%M:%S')

        # Perform Binary search on the sorted logs
        matching_logs = binary_search(sorted_logs, start_date, end_date)

        if matching_logs is None:
            print("No matching logs found.")
        else:
            print("Matching Logs:")
        for log in matching_logs:
            print(log)

        # Ask if the user wants to search again
        search_again = input("Do you want to search again? (yes/no): ")
        if search_again.lower() != 'yes':
            break

search_logs()