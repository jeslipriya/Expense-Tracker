import pandas as pd

# Function to calculate the total expenses
def total_expenses(df):
    return df['Amount'].sum()

# Function to give expense recommendations
def expense_recommendations(expenses):
    # Assuming expenses is a list of tuples or lists like [(category, amount), ...]
    df = pd.DataFrame(expenses, columns=['category', 'amount'])

    # Now you can use groupby to aggregate data
    category_expenses = df.groupby('category')['amount'].sum()

    # Generate recommendations based on the aggregated expenses
    recommendations = []
    for category, total in category_expenses.items():
        if total > 1000:  # Example condition for recommendation
            recommendations.append(f"Consider reducing your spending on {category}.")

    return recommendations
