from flask import Flask, render_template, request, jsonify
import multiprocessing
from math import log10
import time
import database196
from datetime import datetime

app = Flask(__name__)

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
    history = []

    while iterations < 1000:
        iterations += 1
        sum_a = addNumberWithReverse(sum_a)
        if sum_a == reverse_number(sum_a):
            history.append((a,iterations, sum_a))
            return True, sum_a, iterations, history

    return False, a, iterations, history

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start = int(request.form['start'])
    end = int(request.form['end'])
    
    if start > end:
        return jsonify({'error': 'Start must be less than end'})
    
    if start < 1:
        return jsonify({'error': 'Start must be at least 1'})

    database196.delete_table('lychrel3')
    database196.create_table('lychrel3')
    
    numbers = [str(i) for i in range(start, end + 1)]
    
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(possibleLychrelNumber, numbers)

    lychrel_numbers = []
    palindromes = []
    palindrome_groups = {}
    
    for result, number, steps, history in results:
        if result:
            final_palindrome = history[-1][2]  
            initial_number = history[0][0]    
            
            palindromes.append({
                'initial_number': initial_number,
                'steps': steps,
                'palindrome': final_palindrome
            })
            if final_palindrome not in palindrome_groups:
                palindrome_groups[final_palindrome] = []
            palindrome_groups[final_palindrome].append({
                'initial_number': initial_number,
                'steps': steps
            })            
            database196.insert_row(
                initial_number, 
                True, 
                steps, 
                final_palindrome,
                log10(int(initial_number)).__ceil__(), 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'lychrel3'
            )
        else:
            lychrel_numbers.append({
                'number': number,
                'steps': steps
            })
    sorted_groups = sorted(
        palindrome_groups.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    interesting_groups = {
        pal: nums for pal, nums in sorted_groups 
        if len(nums) >= 2
    }
    return jsonify({
        'lychrel_numbers': lychrel_numbers,
        'palindromes': palindromes,
        'palindrome_groups': interesting_groups,
        'total_numbers': len(numbers),
        'total_lychrel': len(lychrel_numbers),
        'total_palindromes': len(palindromes)
    })

if __name__ == '__main__':
    app.run(debug=True)





