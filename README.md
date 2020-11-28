# salary_increment
performs yearly salary increments based on their performance and base wage

---
# Configuration instructions

1. Enter configuration name (name to end with config advised)
2. Enter the starting and ending ranges with their complementary Increment Amount (in percent) and the offset amount (in birr)
3. When you reach the the maximum salary bracket, enter the maximum salary amount in the Starting Range and leave Ending Range 0.00, then enter the remaining fields as before 

Example
```
if salary > 1000:
    increment = salary * 0.15 + 20
elif 1000 <= salary < 2000:
    increment = salary * 0.14 + 30
elif 2000 <= salary < 3000:
    increment = salary * 0.13 + 40
elif 3000 <= salary < 4000:
    increment = salary * 0.12 + 50
elif 4000 <= salary < 5000:
    increment = salary * 0.11 + 60
elif 5000 <= salary < 6000:
    increment = salary * 0.10 + 70
elif 6000 <= salary < 7000:
    increment = salary * 0.09 + 80
elif 7000 <= salary:
    increment = salary * 0.08 + 90
```