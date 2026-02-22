import pandas as pd
import numpy as np

# Setting seed for unique but consistent data
np.random.seed(99)

# 1. Faculty and Sections (Modified for uniqueness)
teachers = ['Dr. Ananya Rao', 'Prof. Sameer Khan', 'Ms. Clara Oswald', 'Mr. David Miller', 'Dr. Sunita Gupta']
sections = ['Elite-A', 'Mainstream-B', 'Foundational-C']

data = []

# 2. Generating 300 rows of data (Requirement: Robust Dataset)
for i in range(1001, 1301):
    t = np.random.choice(teachers)
    s = np.random.choice(sections)
    
    # Performance Score (Normal distribution around 75)
    score = int(np.random.normal(72, 15))
    score = max(0, min(100, score)) # Keep between 0-100
    
    # Late Count (Poisson distribution for realism)
    late = np.random.poisson(3)
    
    # Attendance Rate
    attendance = round(np.random.uniform(60, 99), 2)
    
    # Attrition Risk Logic (Custom for this project)
    # Flagged if score is very low OR lateness is very high
    risk = 1 if (score < 50 or late > 8) else 0
    
    # Satisfaction Feedback (1 to 5)
    feedback = np.random.randint(2, 6) if score > 60 else np.random.randint(1, 4)

    data.append([i, t, s, score, late, attendance, risk, feedback])

# 3. Create DataFrame
df = pd.DataFrame(data, columns=[
    'Student_ID', 'Teacher_Name', 'Section', 'Performance_Score', 
    'Late_Count', 'Attendance_Rate', 'Risk_Status', 'Feedback_Rating'
])

# 4. Save to CSV
df.to_csv('academic_data.csv', index=False)

print("✅ Success! 'academic_data.csv' has been generated in your folder.")