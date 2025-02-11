# I investigated whether a wage premium exists associated with marriage for individuals with the same number of years of education. 
# I grouped data by Education and Marital Status (marital status: 1 for married, 0 for single). In the next step, 
# I Generated a scatter plot with education on the x-axis and lwage (logarithmic wage) on the y-axis.
# Finally, I Estimated the regression model: lwage = a + a1sfemale + a2mfemale + a3mmale + b1educ + b2exper + b3tenure + u, where "u" represents the error term.
# -*- coding: utf-8 -*-
"""Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/119WVSFjpT34lb6OlAcMrOQszzsUAm4Ai
"""
from google.colab import drive                     # Import drive from Google Colab
drive.mount('/content/drive')

import pandas as pd
file_path = '/content/drive/My Drive/Data.csv'     # Path to your file in Google Drive
df = pd.read_csv(file_path)                        # Read the CSV file using pandas
print(df.shape)                                    # Display the first few rows of the DataFrame to verify
df.head()

grouped_df = df.groupby(['educ', 'married']).agg({'wage': 'mean'}).reset_index()     # Group the data by education and marital status
print(grouped_df)                                                                    # Display the grouped DataFrame

import matplotlib.pyplot as plt                                                      # Plot wage vs education, differentiated by marital status
sns.lineplot(data=grouped_df, x='educ', y='wage', hue='married', markers=True, style='married')
plt.title('Wage vs Education, Grouped by Marital Status')
plt.xlabel('Years of Education')
plt.ylabel('Average Wage')
plt.show()
df['lwage'] = np.log(df['wage'])
print(df[['wage', 'lwage']].head())                                                   # Check the first few rows of the DataFrame
plt.figure(figsize=(10, 6))                                                           # Set the size of the figure
# Create scatter plot with regression lines for each group
sns.lmplot(data=df, x='educ', y='lwage', hue='marrstat_label', markers=['o', 's', 'D', '^'], ci=None, palette='Set1')
plt.title('Education vs Log Wage by Marital Status')
plt.xlabel('Years of Education')
plt.ylabel('Log(Wage)')
plt.show()
# Create indicator variables for married men, married women, and single women
df['mmale'] = np.where((df['female'] == 0) & (df['married'] == 1), 1, 0)
df['mfemale'] = np.where((df['female'] == 1) & (df['married'] == 1), 1, 0)
df['sfemale'] = np.where((df['female'] == 1) & (df['married'] == 0), 1, 0)
print(df[['mmale', 'mfemale', 'sfemale']].head())                                     # Check if the variables are created correctly
import statsmodels.api as sm
X = df[['sfemale', 'mfemale', 'mmale', 'educ', 'exper', 'tenure']]                    # Define the independent variables (including a constant term for intercept)
X = sm.add_constant(X)  # Add the intercept term
y = df['lwage']                                                                       # Define the dependent variable
model = sm.OLS(y, X)                                                                  # Fit the regression model
results = model.fit()
print(results.summary())                                                              # Print the summary of the regression results
