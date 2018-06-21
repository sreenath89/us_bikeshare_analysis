
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np

# Mapping cities with correspondinfg csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Setting the Available Month list
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june']

# Setting the Day List
DAY_LIST   = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

# Setting the available filter options 
FILTER_OPTIONS = ['month', 'day', 'both', 'none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            # Fetch the City value entered by the user
            city = str(input('Which City would you like to see the data for - chicago, new york city or washington \n')).lower()
        except Exception as e:
            print('\nPlease check the input that you have entered\n')
            continue
        else:
            # Validate if the value entered by user is available in our city data
            if city in CITY_DATA:
                filter_option = get_filter_option()
                if filter_option == 'both':
                    # Need to provide the option to filter by month as well as day
                    month = get_month()
                    day   = get_day()
                elif filter_option == 'month':
                    # Need to provide only the option to filter by month
                    month = get_month()
                    day = 'all'
                elif filter_option == 'day':
                    # Need to provide only the option to filter by day
                    month = 'all'
                    day   = get_day()
                elif filter_option == 'none':
                    # No specific filter has been requested by user
                    month = 'all'
                    day   = 'all' 
                else:
                    print('\nPlease enter "month" to filter by month, "day" to filter by day, "both" to filter by month and day or "none" if no filters are needed\n')
                break
            else:
                print('\nPlease enter one among any of the 3 cities given here\n')
                continue
    print('-'*40)
    return city, month, day

def get_filter_option():
    """Fetch the input from user for filtering data - month, day, both or none"""
    while True:
        # Get user input for filter option and validate it - month, day, both or none
        filter_option = str(input('\nWould you like to filter the data by "month", "day", "both" or not at all? Type "none" for no filter\n')).lower()
        if filter_option in FILTER_OPTIONS:
            break
        else:
            print('\nPlease enter a correct value!\n')
    return filter_option
    
def get_month():
    """Fetch the value of month entered by user"""
    
    # Creating a single item list for appending to global list of months
    all_filter = ['all']
    while True:
        # Get user input for month (all, january, february, ... , june)
        month = str(input('\nSelect the month - january, february, march, april, may, or June. Enter "all" if no specifc month filter is needed''\n')).lower()
        
        # Validate if the provided month is either 'all' or a value from our global month list
        if month in MONTH_LIST + all_filter:
            break
        else:
            print('\nPlease enter correct value for month \n')
    return month

def get_day():
    """Fetch the value of day entered by user"""
    
    # Creating a single item list for appending to global list of days
    all_filter = ['all']
    while True:
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input('\nSelect the day of week - monday, tuesday, wednesday, thursday, friday, saturday or sunday. Enter all if no specific day filter is needed\n')).lower()
        
        # Validate if the provided value is either 'all' or a value from our day list
        if day in DAY_LIST + all_filter:
            break
        else:
            print('\nPlease enter day value correctly!\n')
    return day


def get_raw_data(df):
    """Displays raw data"""
    #Find the size of the dataframe
    df_size = len(df.index)
    raw_data_query = str(input('\n Would you like to view the raw data - 5 lines at a time? Enter Yes or No .\n')).lower()
    
    #Check if user wants to see raw data
    if raw_data_query == "yes":
        # Looping over the data with 5 steps at a time
        for i in range(5, df_size, 5):
            
            # Printing by 5 lines
            print(df.head(i))
            next_set_data_query = input('\n Would you like to see 5 more lines of raw data? Enter Yes or No.\n')
            if next_set_data_query.lower() != 'yes':
                break

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Fetch the csv file name from the CITY_DATA dict defined at the top of the script
    # Here, city name is the key and csv filename will be given as value, Return None if csv file is not present
    filename = CITY_DATA.get(city)
    
    # Load the data file into dataframe
    df = pd.read_csv(filename)
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract Year, month, day, hour, weeday name from Start Time column to create new Year, month, day, hour and weekday columns
    df['Year']        = df['Start Time'].dt.year
    df['month']       = df['Start Time'].dt.month
    df['day']         = df['Start Time'].dt.day
    df['hour']        = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filter by month if applicable
    if month != 'all':
        month_val  = MONTH_LIST.index(month) + 1
        df = df[df['month'] == month_val]
    
    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\n\n' + '-'*40)
    print('Calculating The Most Frequent Times of Travel...')
    print('-'*40)
    
    # For calculating the execution time for this section
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print("Most Popular month: {}\n".format(common_month))

    # Display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
    print("Most Popular Week of the Day: {}\n".format(common_week_day))

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour: {}\n".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\n\n' + '-'*40)
    print('Calculating The Most Popular Stations and Trip...')
    print('-'*40)
    
    #For calculating the execution time for this section
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most Popular Start Station: {}\n".format(common_start_station))

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most Popular End Station: {}\n".format(common_end_station))
    
    # Display most frequent combination of start station and end station trip
    common_start_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most Frequent Combination of Start Station and End Station Trip: \n{} to {}\n".format(common_start_end_station[0], common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\n\n'+ '-'*40)
    print('Calculating Trip Duration...')
    print('-'*40)
    
    # For calculating the execution time for this section
    start_time = time.time()

    # Fetch the total travel duration time
    total_time_sec = df['Trip Duration'].sum()
    
    # Convert the time and display it
    if total_time_sec < 60:
        # Case when value is less than 1min
        total_time = total_time_sec
        print("Total Trip Duration Time: {} seconds\n".format(total_time))
    elif total_time_sec < 3600:
        # Case when value is less than 1hr
        minutes = total_time_sec // 60
        seconds = total_time_sec - 60*minutes
        print("Total Trip Duration Time: {} mins {} secs\n".format(minutes, seconds))
    else:
        # Case when value is more than 1hr
        hours = round(total_time_sec // 3600, 2)
        minutes = round((total_time_sec - 3600*hours) // 60, 2)
        seconds = round(total_time_sec - 3600*hours - 60*minutes, 2)
        print("Total Trip Duration Time: {}hours {}mins and {}sec \n".format(hours, minutes, seconds))

    # Display mean travel time
    mean_time = round(df['Trip Duration'].mean(), 2)
    print("Mean time of Travel: {} sec".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\n\n' + '-'*40)
    print('Calculating User Stats...')
    print('-'*40)
    
    #For calculating the execution time for this section
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Type Wise Counts are: \n{}\n".format(user_types))

    # Gender Validation
    # Gender data is only present in chicago and new york city's files. So, this needs to be handled for washington
    if 'Gender' in df.columns:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("Gender Wise Counts are: \n{}\n".format(gender))
    
    # Birth Year Validation
    # Birth Year is only present in chicago and new york city's files. So, this needs to be handled for washington
    if 'Birth Year' in df.columns:
        # Fetch the earliest year of birth and display it
        earliest_birth_year = df['Birth Year'].min()
        print("Oldest user was born on : {}\n".format(int(earliest_birth_year)))
    
        # Fetch the most recent year of birth and display it
        recent_birth_year   = df['Birth Year'].max()
        print("Youngest user was born on : {}\n".format(int(recent_birth_year)))
    
        # Fetch the most common year of birth and display it
        common_birth_year   = df['Birth Year'].mode()[0]
        print("Most Common Year of Birth is : {}\n".format(int(common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        get_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

