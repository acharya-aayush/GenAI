#TASK 1
name = input("Enter your name: ")
age = int(input("Enter your age: "))
skills = input("Enter your skills: ").split(", ")
print(f"Name: {name}, Age: {age}, Skills: {', '.join(skills)}")

#TASK 2: Create a program that checks if a student has passed a test and gives feedback.
marks = int(input("Enter your marks: "))
if marks >= 40:print("You have passed the test")
else: print("You have failed the test")

# TASK 3: Create a pogram to:
# Take input: Scores of 10 students or just create a your own list.
# Add 5 bonus points to every score below 50.
# Print each score with a label: "Pass" if 50 or above, else "Fail".
# Finally, print the updated list of scores.
scores=input("Enter scores of 10 students (comma separated): ").split(", ")
for i in range(len(scores)):
    scores[i] = int(scores[i])
    if scores[i] < 50:
        scores[i] += 5
    status = "Pass" if scores[i] >= 50 else "Fail"
    print(f"Score: {scores[i]}, Status: {status}")  

#TASK4: Complete the methods to add a book, display available books, and borrow a book from the library.
class lib:
    def __init__(self):
        self.books = []
        
        