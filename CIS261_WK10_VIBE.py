# Kimberli Shinkle
# CIS261
# WK10 VIBE Coding

import os
from typing import List

DATA_FILE = "student_grades.txt"


class Student:
	def __init__(self, name: str, sid: str, test1: float, test2: float, test3: float):
		self.name = name
		self.id = sid
		self.test1 = float(test1)
		self.test2 = float(test2)
		self.test3 = float(test3)
		self.average = 0.0
		self.grade = ""
		self.calculate()

	def calculate(self):
		self.average = round((self.test1 + self.test2 + self.test3) / 3.0, 2)
		self.grade = self._letter_grade()

	def _letter_grade(self) -> str:
		a = self.average
		if a >= 90:
			return "A"
		if a >= 80:
			return "B"
		if a >= 70:
			return "C"
		if a >= 60:
			return "D"
		return "F"

	def to_pipe(self) -> str:
		return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"

	@classmethod
	def from_pipe(cls, line: str):
		parts = line.strip().split("|")
		if len(parts) < 7:
			raise ValueError("Malformed record")
		name, sid = parts[0], parts[1]
		test1, test2, test3 = map(float, parts[2:5])
		# average and grade in file are ignored and recalculated to ensure consistency
		return cls(name, sid, test1, test2, test3)


def load_records(filename: str) -> List[Student]:
	students: List[Student] = []
	if not os.path.exists(filename):
		return students
	try:
		with open(filename, "r", encoding="utf-8") as f:
			for line in f:
				line = line.strip()
				if not line:
					continue
				try:
					s = Student.from_pipe(line)
					students.append(s)
				except Exception:
					# skip malformed lines but continue loading others
					continue
	except Exception as e:
		print(f"Error loading records: {e}")
	return students


def save_records(filename: str, students: List[Student]) -> None:
	try:
		with open(filename, "w", encoding="utf-8") as f:
			for s in students:
				f.write(s.to_pipe())
		print(f"Saved {len(students)} record(s) to {filename}.")
	except Exception as e:
		print(f"Error saving records: {e}")


def input_float(prompt: str) -> float:
	while True:
		val = input(prompt).strip()
		if val.upper() == "ESC":
			raise KeyboardInterrupt
		try:
			return round(float(val), 2)
		except ValueError:
			print("Please enter a valid number (or type ESC to cancel).")


def add_student(students: List[Student]) -> None:
	try:
		name = input("Student name (or type ESC to cancel): ").strip()
		if name.upper() == "ESC":
			return
		sid = input("Student ID: ").strip()
		if sid.upper() == "ESC":
			return
		t1 = input_float("Test 1 score: ")
		t2 = input_float("Test 2 score: ")
		t3 = input_float("Test 3 score: ")
		s = Student(name, sid, t1, t2, t3)
		students.append(s)
		print(f"Added student {s.name} (Avg: {s.average:.2f}, Grade: {s.grade}).")
	except KeyboardInterrupt:
		print("Add student cancelled.")


def display_students(students: List[Student]) -> None:
	if not students:
		print("No student records to display.")
		return
	header = f"{'Name':20} {'ID':10} {'T1':>6} {'T2':>6} {'T3':>6} {'Avg':>7} {'Grade':>6}"
	print(header)
	print("-" * len(header))
	for s in students:
		print(f"{s.name:20} {s.id:10} {s.test1:6.2f} {s.test2:6.2f} {s.test3:6.2f} {s.average:7.2f} {s.grade:6}")


def display_statistics(students: List[Student]) -> None:
	if not students:
		print("No records - no statistics available.")
		return
	averages = [s.average for s in students]
	highest = max(averages)
	lowest = min(averages)
	class_avg = round(sum(averages) / len(averages), 2)
	print(f"Highest average: {highest:.2f}")
	print(f"Lowest average:  {lowest:.2f}")
	print(f"Class average:   {class_avg:.2f}")


def search_student(students: List[Student]) -> None:
	q = input("Enter student name to search (or type ESC to cancel): ").strip()
	if q.upper() == "ESC":
		return
	qlow = q.lower()
	results = [s for s in students if qlow in s.name.lower()]
	if not results:
		print("No matching students found.")
		return
	display_students(results)


def main():
	students = load_records(DATA_FILE)
	print("Student Grade Calculator")
	print("Type ESC at any main prompt to exit (enter ESC then press Enter).")
	try:
		while True:
			print("\nMenu:\n1) Add new student\n2) Display all students\n3) Search by name\n4) Class statistics\n5) Save records\nType ESC to exit")
			choice = input("Select an option: ").strip()
			if not choice:
				continue
			if choice.upper() == "ESC":
				break
			if choice == "1":
				add_student(students)
			elif choice == "2":
				display_students(students)
			elif choice == "3":
				search_student(students)
			elif choice == "4":
				display_statistics(students)
			elif choice == "5":
				save_records(DATA_FILE, students)
			else:
				print("Invalid option. Choose 1-5 or type ESC to exit.")
	except KeyboardInterrupt:
		print("\nExiting program.")
	# auto-save on exit
	try:
		save_records(DATA_FILE, students)
	except Exception:
		pass


if __name__ == "__main__":
	main()
