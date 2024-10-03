import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('student_scores_random_names.csv')

subjects = df.columns.tolist()[2:]


average_scores = df[subjects].mean()

# Create a bar plot
plt.figure(figsize=(10, 6))
average_scores.plot(kind='bar', color='skyblue')

# Adding title and labels
plt.title('Average Scores for Each Subject Across All Semesters')
plt.xlabel('Subjects')
plt.ylabel('Average Score')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.ylim(0, 100)  # Set y-axis limits if scores are between 0 and 100
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a grid for better visualization

# Show the plot
plt.tight_layout()
plt.show()


average_scores_by_semester = df.groupby('Semester')[subjects].mean().reset_index()

# Calculate the overall average score for all subjects for each semester
average_scores_by_semester['Overall Average'] = average_scores_by_semester[subjects].mean(axis=1)

# Set the semester as the index for better plotting
average_scores_by_semester.set_index('Semester', inplace=True)

# Create a line plot for the overall average score
plt.figure(figsize=(12, 6))
plt.plot(average_scores_by_semester.index, average_scores_by_semester['Overall Average'], marker='o', label='Overall Average Score', color='blue')

plt.title('Overall Average Scores by Semester')
plt.xlabel('Semester')
plt.ylabel('Overall Average Score')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.ylim(0, 100)  # Set y-axis limits if scores are between 0 and 100
plt.grid()  # Add a grid for better visualization
plt.legend()  # Add a legend

# Show the plot
plt.tight_layout()
plt.show()