import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels() 
#    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

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

    # Daily Line Chart
    fig = plt.figure(figsize=(12, 6))
    plt.subplot(3, 2, 1)
    plt.plot(daily_plastic_mean.index, daily_plastic_mean.values, marker='o')
    plt.title('Average Daily Plastic Levels')
    plt.xlabel('Date')
    plt.ylabel('Plastic Level')

    ax = plt.subplot(3, 2, 2)
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

    ax2 = plt.subplot(3, 2, 4)
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
    ax3 = plt.subplot(3, 2, 6)
    plt.plot(yearly_plastic_sum.index, yearly_plastic_sum.values, marker='o')
    plt.title('Yearly Plastic Levels')
    plt.xlabel('Year')
    plt.ylabel('Plastic Level')
    plt.tight_layout()

    extent = full_extent(ax).transformed(fig.dpi_scale_trans.inverted())
    plt.savefig('static/public/graphs_daily.png', bbox_inches=extent)
    extent = ax2.get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())
    # extent = plt.gca().get_tightbbox(fig.canvas.renderer).transformed(fig.dpi_scale_trans.inverted())
    plt.savefig('static/public/graphs_monthly.png', bbox_inches=extent)
    extent = full_extent(ax3).transformed(fig.dpi_scale_trans.inverted())
    plt.savefig('static/public/graphs_yearly.png', bbox_inches=extent)
    
    plt.savefig('static/public/graphs.png')
    


# input_file = "merged_allimg_predictions_withoutduplicates.csv"

# getPlasticlevel(input_file)
