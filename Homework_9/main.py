import pandas as pd

df = pd.read_csv('student_scores_random_names.csv')

subjects = df.columns.tolist()[2:]

students_with_low_scores = df[df[subjects].lt(50, axis=1).any(axis=1)]

# Print students who got scores lower than 50
print(f"Here are students who got scores lower than 50:({len(students_with_low_scores['Student'].unique())})")

for student in students_with_low_scores['Student'].unique():
    print(student)

average_scores = df.groupby('Semester')[subjects].mean()
# Print average scores for each subject in each semester
print(f"\nHere is average scores for each subject in each semester:\n{average_scores}")

df['Average'] = df[subjects].mean(axis=1)
student_averages = df.groupby('Student')['Average'].mean()
max_average = student_averages.max()
top_students = student_averages[student_averages == max_average]

# Print students with the highest average score
print(f"\nStudent(s) with the highest average score:\n{top_students}")

subject_averages = df[subjects].mean()

lowest_average_subject = subject_averages.idxmin()
lowest_average_score = subject_averages.min()

# Print subject with the lowest average score
print(f"\nThe subject with the lowest average score is {lowest_average_subject} with an average score of {lowest_average_score:.2f}.")

average_scores_df = average_scores.reset_index()

output_file = 'average_scores_by_semester.xlsx'
average_scores_df.to_excel(output_file, index=False)

print(f"\nAverage scores by semester have been saved to {output_file}")

df_sorted = df.sort_values(by=['Student', 'Semester'])
improving_students = []

for student, group in df_sorted.groupby('Student'):
    group = group.sort_values('Semester')
    is_improving = True

    for subject in subjects:
        scores = group[subject].dropna()

        if not scores.is_monotonic_increasing:
            is_improving = False
            break

    if is_improving:
        improving_students.append(student)

print(f"\nHere are students who improved scores in all subjects({len(improving_students)}):")

for student in improving_students:
    print(student)