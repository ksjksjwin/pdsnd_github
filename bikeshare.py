#import libraries
import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please choose the city you would like to explore. (e.g chicago, new york city, washington): ").lower()
        if city in CITIES:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please choose the month you would like to explore. (e.g january, february, march ...) or type \'all\' to apply no month filter: ").lower()
        if month in MONTHS:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please choose the day you would like to explore. (e.g monday, tuesday, wednesday ...) or type \'all\' to apply no month filter: ").lower()
        if day in DAYS:
            break

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
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day'] == day.title()] #.title

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is \'{}\'".format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day_of_week = df['day'].value_counts().idxmax()
    print("The most common day of week is \'{}\'".format(most_common_day_of_week))

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is \'{}\'".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is \'{}\'".format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is \'{}\'".format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station is {} and {}".format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is \'{}\'".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is \'{}\'".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # TO DO: Display counts of user types
        user_types_counts = df['User Type'].value_counts()
        print("The counts of user types:\n {}".format(user_types_counts))

        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print("The counts of gender:\n {}".format(gender))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print("The Earliest birth is {}".format(earliest_birth))

        most_recent_birth = df['Birth Year'].max()
        print("The Most recent birth is \'{}\'".format(most_recent_birth))

        most_common_birth = df['Birth Year'].mode()[0]
        print("The Most common birth is \'{}\'".format(most_common_birth))
    except KeyError:
        print('Gender and year of birth dat is not available for washington city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Display raw data of bikeshare upon user request."""

    row_len = df.shape[0]

    #Will keep ask user for raw data
    for i in range(0, row_len, 5):
        ans = input('\nDo you want see 5 lines of raw data?  (e.g \'yes\' or \'no\'): ')
        if ans.lower() != 'yes':
            break

        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')

        #Data with jason format
        for row in row_data:
            print(row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
