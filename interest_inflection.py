import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve

def inflection_equation(t, P_s, r_s, P_c, r_c):
    return P_s * (1 + r_s * t) - P_c * (1 + r_c) ** t

# Example values
P_s = 1000 #Capital da proposta de juros simples
r_s = 0.15 #Taxa da proposta de juros simples
P_c = 1000 #Capital da proposta de juros composto
r_c = 0.1  #Taxa da proposta de juros composto

# Determine a reasonable range of years to search for inflection points
years_range = np.arange(0, 1000, 1)

# Initialize a list to store inflection points
inflection_points = []

# Initialize a variable to store the previous inflection point
previous_inflection = 0.0

for initial_guess in years_range:
    t_inflection = fsolve(inflection_equation, x0=initial_guess, args=(P_s, r_s, P_c, r_c))
    t_inflection = round(t_inflection[0], 10)  # Round to two decimal places for better presentation
    
    # If the newly found inflection point is the same as the previous one, stop the loop
    if previous_inflection != 0.0 and t_inflection == previous_inflection:
        break

    inflection_points.append(t_inflection)
    previous_inflection = t_inflection

# Calculate amounts for simple and compound interest over time
max_time = np.ceil(max(inflection_points))+1
years = np.arange(0, np.ceil(max(inflection_points))+1, 1)
simple_interest = P_s * (1 + r_s * years)
compound_interest = P_c * (1 + r_c) ** years

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(years, simple_interest, label="Juros simples")
plt.plot(years, compound_interest, label="Juros composto")
axes = plt.gca()
axes.set_xlim([-5e-1, 1.001*max_time])
axes.set_ylim([0.9*np.min([simple_interest,compound_interest]), 1.1*np.max([simple_interest,compound_interest])])
plt.scatter(inflection_points, [P_s * (1 + r_s * t) for t in inflection_points], color='red', label="Inflection Points")
plt.xlabel("Tempo (em anos)")
plt.ylabel("Montante")
plt.legend()
plt.title("Comparação de proposta de juros simples e composto")
plt.grid(True)
plt.tight_layout()

plt.show()

# Create a table using Pandas
data = {
    "Anos": years,
    "Juros Simples": simple_interest,
    "Juros Composto": compound_interest
}
df = pd.DataFrame(data)

# Print the table
print(df)

# Print inflection points
print("Pontos de inflecção:", inflection_points)