import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os  # added to handle file paths and names dynamically


# enter the file path to be analyzed here.
# make sure this is an Excel file (.xlsx)
# when you change this, all output files and titles will update automatically.
FILE_PATH = 'GBPUSD_1_Year_4H_Data.xlsx'
SMA_PERIOD = 50  # Moving Average period to define "Trend Continuation"

def check_mitigation(fvg_type, gap_top, gap_bottom, future_data):
    """
    checking if an FVG is mitigated by future price action.
    returns (True, mitigation_time) if mitigated, else (False, None).
    """
    for _, row in future_data.iterrows():
        if fvg_type == 'Bullish':
            # bullish FVG (Support): price is above. mitigated if Low drops into gap.
            if row['low'] <= gap_top:
                return True, row['datetime']
        
        elif fvg_type == 'Bearish':
            # bearish FVG (Resistance): price is below. mitigated if High rises into gap.
            if row['high'] >= gap_bottom:
                return True, row['datetime']
                
    return False, None

def plot_fvgs(df, fvgs, file_name, num_candles=150):
    """
    plotting the last 'num_candles' of price data with FVG rectangles overlayed.
    uses 'file_name' to dynamically name the chart title and output file.
    """
    print(f"\n--- Generating Plot for last {num_candles} candles ---")
    
    # slice the data for better visibility (plotting 6 months is too compclicated)
    subset = df.tail(num_candles).copy()
    subset = subset.reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # plot Close Price
    ax.plot(subset.index, subset['close'], color='black', label='Close Price', linewidth=1)
    
    # plot SMA (Trend Line) if it exists in the subset
    if 'sma' in subset.columns:
        ax.plot(subset.index, subset['sma'], color='blue', label=f'{SMA_PERIOD} SMA (Trend)', linestyle='--', alpha=0.7)
    
    
    date_to_idx = {date: idx for idx, date in enumerate(subset['datetime'])}
    
    # plot FVGs
    for fvg in fvgs:
        # only plot if the FVG start time is visible in our current subset
        if fvg['datetime'] in date_to_idx:
            start_idx = date_to_idx[fvg['datetime']]
            
            # determine end index (mitigation time or end of chart)
            if fvg['mitigated'] and fvg['mitigation_time'] in date_to_idx:
                end_idx = date_to_idx[fvg['mitigation_time']]
            else:
                end_idx = subset.index[-1] # extend to end of chart if not mitigated (or mitigated in future)
            
            width = max(1, end_idx - start_idx) # ensure at least 1 width
            
            # determine color based on trend context
            # lighter/solid for continuation, darker/hatched for counter-trend
            if fvg['context'] == 'Trend Continuation':
                alpha_val = 0.3
                hatch_style = None 
            else:
                alpha_val = 0.15
                hatch_style = '///' 
            
            # draw rectangle
            # xy is the bottom-left corner.
            if fvg['type'] == 'Bullish':
                rect = mpatches.Rectangle(
                    (start_idx, fvg['gap_bottom']), 
                    width, 
                    fvg['gap_size'], 
                    alpha=alpha_val, 
                    color='green',
                    hatch=hatch_style
                )
                ax.add_patch(rect)
                
            elif fvg['type'] == 'Bearish':
                rect = mpatches.Rectangle(
                    (start_idx, fvg['gap_bottom']), 
                    width, 
                    fvg['gap_size'], 
                    alpha=alpha_val, 
                    color='red',
                    hatch=hatch_style
                )
                ax.add_patch(rect)

    # formatting: Dynamic Title based on file name
    ax.set_title(f"{file_name} - Price Action & FVGs (Last {num_candles} Hours)")
    ax.set_xlabel("Candles (Time)")
    ax.set_ylabel("Price")
    ax.grid(True, alpha=0.3)
    
    # custom legend
    green_patch = mpatches.Patch(color='green', alpha=0.3, label='Bullish FVG')
    red_patch = mpatches.Patch(color='red', alpha=0.3, label='Bearish FVG')
    sma_line = plt.Line2D([0], [0], color='blue', linestyle='--', label=f'{SMA_PERIOD} SMA')
    ax.legend(handles=[green_patch, red_patch, sma_line])
    
    # save and show: Dynamic Filename
    output_img = f'{file_name}_chart.png'
    plt.savefig(output_img)
    print(f"Chart saved to {output_img}")
    plt.show()

def analyze_gbpusd_data(file_path):
    print("--- Loading and Cleaning Data ---")
    
    # extract the base name of the file (e.g., 'GBPUSD_Data' from 'path/to/GBPUSD_Data.xlsx')
    # this will be used for naming output files dynamically.
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    try:
        # load the dataset
        df = pd.read_excel(file_path, header=0)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
        return
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # clean the dataframe: Drop the first two rows (metadata garbage)
    df = df.iloc[2:].reset_index(drop=True)

    # rename columns
    df.columns = ['datetime', 'close', 'high', 'low', 'open']

    # convert types
    df['datetime'] = pd.to_datetime(df['datetime'])
    cols_to_numeric = ['open', 'high', 'low', 'close']
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col])

    print(f"Data successfully loaded from '{base_name}'. Total rows: {len(df)}")
    
    
    # PART 0: calculate Indicators (Trend)
    
    # calculate Simple Moving Average
    df['sma'] = df['close'].rolling(window=SMA_PERIOD).mean()
    print(f"Calculated {SMA_PERIOD}-period SMA for Trend detection.")
    print("-" * 30)

 
    # PART 1: detailed Statistics
   
    print(f"\n--- Detailed Price Statistics ({base_name}) ---")
    
    # calculate stats using describe() and transpose for better reading
    stats = df[cols_to_numeric].describe().T[['mean', 'std', 'min', '50%', 'max']]
    stats.rename(columns={'50%': 'median'}, inplace=True)
    
    # formatting for display
    print(stats.round(5))
    

    # PART 2: detect Fair Value Gaps (FVG) & Mitigation
    
    print("\n--- Detecting Fair Value Gaps & Trend Context ---")
    print("Scanning...")

    df['prev_2_high'] = df['high'].shift(2)
    df['prev_2_low'] = df['low'].shift(2)
    
    fvgs = []

    for i in range(2, len(df)):
        current_row = df.iloc[i]
        prev_2_high = df.iloc[i-2]['high']
        prev_2_low = df.iloc[i-2]['low']
        
        # get Trend Context (SMA) at this specific time
        # if price is above SMA -> Uptrend, else Downtrend
        current_sma = current_row['sma']
        trend_status = "Neutral" # default if SMA is NaN (start of data)
        
        if not pd.isna(current_sma):
            if current_row['close'] > current_sma:
                trend_status = "Uptrend"
            else:
                trend_status = "Downtrend"
        
        fvg_data = None

        # check Bullish FVG
        if current_row['low'] > prev_2_high:
            fvg_context = "Counter-Trend / Reversal"
            if trend_status == "Uptrend":
                fvg_context = "Trend Continuation"
                
            fvg_data = {
                'datetime': current_row['datetime'],
                'type': 'Bullish',
                'gap_top': current_row['low'],
                'gap_bottom': prev_2_high,
                'gap_size': current_row['low'] - prev_2_high,
                'mitigated': False,
                'mitigation_time': None,
                'trend_at_creation': trend_status,
                'context': fvg_context
            }

        # check Bearish FVG
        elif current_row['high'] < prev_2_low:
            fvg_context = "Counter-Trend / Reversal"
            if trend_status == "Downtrend":
                fvg_context = "Trend Continuation"

            fvg_data = {
                'datetime': current_row['datetime'],
                'type': 'Bearish',
                'gap_top': prev_2_low,
                'gap_bottom': current_row['high'],
                'gap_size': prev_2_low - current_row['high'],
                'mitigated': False,
                'mitigation_time': None,
                'trend_at_creation': trend_status,
                'context': fvg_context
            }

        # if an FVG was found, check for mitigation
        if fvg_data:
            future_data = df.iloc[i+1:]
            is_mitigated, mit_time = check_mitigation(
                fvg_data['type'], 
                fvg_data['gap_top'], 
                fvg_data['gap_bottom'], 
                future_data
            )
            fvg_data['mitigated'] = is_mitigated
            fvg_data['mitigation_time'] = mit_time
            fvgs.append(fvg_data)

    # results
    fvg_df = pd.DataFrame(fvgs)

    if not fvg_df.empty:
        total = len(fvg_df)
        continuation = len(fvg_df[fvg_df['context'] == 'Trend Continuation'])
        counter = len(fvg_df[fvg_df['context'] == 'Counter-Trend / Reversal'])

        print(f"Total FVGs detected: {total}")
        print(f"Trend Continuation FVGs: {continuation} ({(continuation/total)*100:.1f}%)")
        print(f"Counter-Trend FVGs:      {counter} ({(counter/total)*100:.1f}%)")
        
        # save to CSV using dynamic filename
        output_filename = f'{base_name}_detailed_fvgs.csv'
        fvg_df.to_csv(output_filename, index=False)
        print(f"\nDetailed FVG list (with trend context) saved to: {output_filename}")
        
       
        # PART 3: Visualization
       
        # Pass base_name to the plotting function
        plot_fvgs(df, fvgs, base_name, num_candles=150)
        
    else:
        print("No Fair Value Gaps detected.")

if __name__ == "__main__":
    analyze_gbpusd_data(FILE_PATH)