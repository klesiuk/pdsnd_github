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
    while True:
        try:
            city = str(input("Enter the name of the city: chicago / new york city / washington: ").lower())
            if city in CITY_DATA.keys():
                break
            print("This is not a valid city name, try again.")
        except Exception as e:
            print(e)

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
            month = input("Enter the name of the month you would like to explore: {} :".format(' / '.join(months))).lower()
            if month in months:
                break
            print("This is not a valid month name, try again.")
        except Exception as e:
            print(e)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day = input("Enter the name of the weekday you would like to explore: {} :".format(' / '.join(days))).lower()
            if day in days:
                break
            print("This is not a valid weekday name, try again.")
        except Exception as e:
            print(e)

    print("\nYou will see data filteredy by:\ncity name: {}\nmonth: {}\nweekday: {}\n".format(city.title(), month.title(), day.title()))
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
    file = CITY_DATA[city]
    df = pd.read_csv(file)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel ...\n')
    start_time = time.time()

    # display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common = df['month'].mode()[0]
    most_common_name = months[most_common - 1]
    print('The most common month of rental was: {}'.format(most_common_name.title()))

    # display the most common day of week
    print('The most common day of rental was: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour

    print('The most common hour of rental was: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station was: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station was: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start and end station was: {}'.format(df.groupby(['Start Station', 'End Station']).size().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time was: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time was: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCount of user types:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCount of users by gender:\n', df['Gender'].value_counts())
    else:
        print('\nNo gender data available for the chosen city\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest birth year for user:\n', df['Birth Year'].min())
        print('Latest birth year for user:\n', df['Birth Year'].max())
        print('Most common birth year for user:\n', df['Birth Year'].mode()[0])
    else:
        print('\nNo birth year data available for the chosen city\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        trip_duration_stats(df)
        station_stats(df)
        user_stats(df)

        # Print raw output data (5 rows at a time)
        raw_data = input('\n Would you like to see raw output data? Enter yes or no.\n')
        rows_count = 0
        while True:
            if raw_data.lower() != 'yes':
                break
            print(df.iloc[rows_count:rows_count+5])
            rows_count += 5
            raw_data = input('\n Would you like to see more raw output data? Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
