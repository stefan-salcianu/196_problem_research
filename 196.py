import multiprocessing
import database196
from math import log10
import time
import sys
import logging 

sys.set_int_max_str_digits(0)  # Dezactivează limita pentru reprezentarea string a numerelor mari

logging.basicConfig(
    filename='lychrel_progress.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

fout = open("history.txt", "a")

def reverse_number(n):
    return n[::-1]

def addNumberWithReverse(a):
    a_reverse = reverse_number(a)
    resulted_number = []
    carry = 0

    for i in range(len(a)):
        sum_digits = int(a[i]) + int(a_reverse[i]) + carry
        resulted_number.append(str(sum_digits % 10))
        carry = sum_digits // 10

    if carry:
        resulted_number.append(str(carry))

    return reverse_number(''.join(resulted_number))

def possibleLychrelNumber(a):
    iterations = 0
    sum_a = a
    max_iteration=600
    history = []

    if len(a) > 30:  
        print(f"Warning: Number {a} is very large ({len(a)} digits). Processing may take a long time.")
    
    while iterations < max_iteration:
        iterations += 1
        try:
            sum_a = addNumberWithReverse(sum_a)
            if sum_a == reverse_number(sum_a):
                history.append((a, iterations, sum_a))
                return True, sum_a, iterations, history
        except Exception as e:
            print(f"Error processing {a} at iteration {iterations}: {str(e)}")
            return False, a, iterations, history

    return False, a, iterations, history

def allPossibleLychrelNumbers(start, end):
    database196.delete_table('lychrel3')
    database196.create_table('lychrel3')
    
    numbers = [str(i) for i in range(int(start), int(end) + 1)]
    total = len(numbers)
    history_data = []
    
    print(f"Starting processing {total} numbers from {start} to {end}")
    start_time = time.time()    
    processed_count = 0
    log_interval = max(1, total // 100)  # Log la fiecare 1% din progres, minim 1

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(possibleLychrelNumber, numbers)

    for i, result in enumerate(results):
        processed_count += 1
        if processed_count % log_interval == 0:
            elapsed = time.time() - start_time
            percent = (processed_count / total) * 100
            est_total = elapsed / (percent / 100) if percent > 0 else 0
            remaining = est_total - elapsed
            
            logging.info(f"Progress: {percent:.2f}% ({processed_count}/{total})")
            logging.info(f"Time elapsed: {elapsed/60:.2f} minutes, Est. remaining: {remaining/60:.2f} minutes")

        result_val, number, steps, history = result
        if result_val:
            history_data.extend(history)
        else:
            print(f"{number} - could be a possible Lychrel number (tested {steps} iterations)", file=fout)
    
    print(file=fout)

    for i, (number, iterations, palindrome) in enumerate(history_data):
        database196.insert_row(
            number,
            True,
            iterations,
            palindrome,
            log10(int(number)).__ceil__(),
            time.strftime("%Y-%m-%d %H:%M:%S"),
            'lychrel3'
        )
    
    database196.show_all_where(20, 'lychrel3')

if __name__ == "__main__":
    while True:
        try:
            start = int(input("Enter start: "))
            end = int(input("Enter end: "))
            if start > end:
                print("Start must be less than or equal to End. Try again.")
                continue
            if start < 1:
                print("Start must be at least 1.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    print("The program is working, please wait...")
    allPossibleLychrelNumbers(start, end)
    fout.close()
