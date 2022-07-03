import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input('Please select from the following cities : chicago, new york city, washington \n> ').lower()
        if city in cities :
            break
        else:
            print('Input error, invalid city') 

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
          month = input('Select a month you would like to explore \n> {} \n>'.format(months)).lower()
          if month in months :
              break
          else:
              print('Input error, invalid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday','thursday','friday','saturday','all']
    while True:
        day = input('Now, select the day \n> {} \n>'.format(days)).lower()
        if day in days :
            break
        else:
            print('Input error, invalid day')

    print('-'*40)
    return city, month, day


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
    
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is : {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day is : {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour is : {}'.format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is : {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is : {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['route']=df['Start Station']+","+df['End Station']
    print('The most common route is :{}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time : ',(df['Trip Duration'].sum()).round())

    # display mean travel time
    print('The average travel time : ',(df['Trip Duration'].mean()).round())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender
    
    if city != 'washington':
        print(df['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
        print('The most common year of birth is : ',int(df['Birth Year'].mode()[0]))
        print('The most recent year of birth is : ',int(df['Birth Year'].max()))
        print('The earliest year of birth is : ',int(df['Birth Year'].min()))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    # Check whether user would like to view raw data.
    print('\nPreparing raw data analysis...\n')
    
    r = 0 
    customer_query = input('5 rows of raw data is ready for analysis, would you like to proceed? yes or no ').lower()
    if customer_query not in ['yes', 'no']:
        print('Input error, please try again')
        customer_query = input('5 rows of raw data is ready for analysis, would you like to proceed? yes or no ').lower()
    elif customer_query != 'yes':
        print('Program will now exit')
        
    else:
        while r+5 < df.shape[0]:
            print(df.iloc[r:r+5])
            r += 5 
            customer_query = input('Would you like view the next 5 rows? ').lower()
            if customer_query != 'yes':
                print('Program will now exit')
                break
                


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Program will now exit')
            break


if __name__ == "__main__":
	main()
