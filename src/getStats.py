import pandas as pd
import matplotlib.pyplot as plt

def getPlasticlevel(plastic_datafile):   
    # Step 1: Load the data from the CSV file
    df = pd.read_csv(plastic_datafile)

    # Step 2: Convert the 'Timestamp' column to a pandas datetime object
    df['Timestamp'] = pd.to_datetime(df['Date'])
    # print(df['Timestamp'])

    # Step 3: Set the 'Timestamp' column as the index
    df.set_index('Timestamp', inplace=True)

    # Step 4: Resample the data to get daily, monthly, and yearly averages
    daily_plastic = df['PRED_CT'].resample('D')
    monthly_plastic = df['PRED_CT'].resample('M')
    yearly_plastic = df['PRED_CT'].resample('Y')

    daily_plastic_mean = daily_plastic.mean()
    monthly_plastic_mean = monthly_plastic.mean()
    yearly_plastic_mean = yearly_plastic.mean()
    
    daily_plastic_sum = daily_plastic.sum()
    monthly_plastic_sum = monthly_plastic.sum()
    yearly_plastic_sum = yearly_plastic.sum()
    plt.figure(figsize=(12, 6))
    plt.subplot(3, 2, 1)
    plt.plot(daily_plastic_mean.index, daily_plastic_mean.values, marker='o')
    plt.title('Average Daily Plastic Levels')
    plt.xlabel('Date')
    plt.ylabel('Plastic Level')

    plt.subplot(3, 2, 2)
    plt.plot(daily_plastic_sum.index, daily_plastic_sum.values, marker='o')
    plt.title('Daily Plastic Levels')
    plt.xlabel('Date')
    plt.ylabel('Plastic Level')

    # Monthly Line Chart
    plt.subplot(3, 2, 3)
    plt.plot(monthly_plastic_mean.index, monthly_plastic_mean.values, marker='o')
    plt.title('Average Monthly Plastic Levels')
    plt.xlabel('Month')
    plt.ylabel('Plastic Level')

    plt.subplot(3, 2, 4)
    plt.plot(monthly_plastic_sum.index, monthly_plastic_sum.values, marker='o')
    plt.title('Monthly Plastic Levels')
    plt.xlabel('Month')
    plt.ylabel('Plastic Level')

    # Yearly Line Chart
    plt.subplot(3, 2, 5)
    plt.plot(yearly_plastic_mean.index, yearly_plastic_mean.values, marker='o')
    plt.title('Average Yearly Plastic Levels')
    plt.xlabel('Year')
    plt.ylabel('Plastic Level')
    plt.subplot(3, 2, 6)
    plt.plot(yearly_plastic_sum.index, yearly_plastic_sum.values, marker='o')
    plt.title('Yearly Plastic Levels')
    plt.xlabel('Year')
    plt.ylabel('Plastic Level')
    plt.tight_layout()
    plt.savefig('static/public/graphs.png')

# input_file = "merged_allimg_predictions_withoutduplicates.csv"

# getPlasticlevel(input_file)
