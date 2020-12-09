# Overview
Apply machine learning and statistical analysis on g-force, linear acceleration and angular velocity data collected from phone sensors, to detect walking patterns of individuals and determine their physical characteristics.

# Data Collection

Data was collected using the Android app, PhysicsToolbox.The data can be found in the folder "Data". Data contains g-foce, linear acceleration & angular velocity data in csv form. 

# Instructions:
Required libraries: 

scipy 
matplotlib 
pandas 
numpy 
sklearn 
statsmodels

Please install them using the command below:

  pip install <library name>
  
Simply clone the repository and run the following command:

   python main.py 
   
# Idea:

First use ETL to clean data and the apply Butterworth Filter to get rid of noise from data. Then compute the Fourier Transform of the walking data and plot the frequency of the walking pattern. After that use Machine Learning models on the data and use satistical analysis to answer the following questions:
Q. predict the height, level of activity, and gender of an individual based on their walking pattern.
Q. How does walking pace (steps/minute or similar) differ between people? Does it vary by age, gender, height, …?
Q. If we compare right-foot vs left-foot, can we determine if someone's gait is asymmetrical? Perhaps this can be used to detect an injury.
