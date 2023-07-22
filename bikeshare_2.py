import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday']


def check_input(input_str, input_type):
    while True:
        input_read = input(input_str)
        try:
            if input_read in ['chicago', 'new york city', 'washington'] and input_type == CITY_DATA:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == MONTHS:
                break
            elif input_read in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                                'all'] and input_type == DAYS:
                break
            else:
                if input_type == CITY_DATA:
                    print("Sorry, your input is wrong, make sure that you wrote it correctly")
                if input_type == MONTHS:
                    print("Sorry, your input is wrong, make sure that you wrote it correctly")
                if input_type == DAYS:
                    print("Sorry, your input is wrong, make sure that you wrote it correctly")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_read


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
    city = check_input("pleas chosse from chicago, new york city or washington?", CITY_DATA).lower()
    # get user input for month (all, january, february, ... , june)
    month = check_input("Which Month (all, january, ... june)?", MONTHS).lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("Which day? (all, monday, tuesday, ... sunday)", DAYS).lower()
    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print('Most Day Of Week:', popular_day_of_week)

    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]

    print('Most Common Start Hour:', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station: ({})\n".format(most_common_start))

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("Most Commonly Used End Station: ({})\n".format(most_common_end))

    # display most frequent combination of start station and end station trip
    most_freq_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(
        "Most Frequent Combination Of Start Station And End Station Trip: ({}) TO ({})\n".format(most_freq_start_end[0],
                                                                                                 most_freq_start_end[
                                                                                                     1]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    # iteratively print out the total numbers of user types
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)
    else:
        print("Gender Information not Available\n")
    if 'Birth Year' in df.columns:
        user_stats_birth(df)
    else:
        print("birthday Information not Available\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("Counts Of Gender:\n{}\n".format(gender_counts))


def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)


def table_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating Dataset Stats...\n')

    # counts the number of missing values in the entire dataset
    number_of_missing_values = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city, number_of_missing_values))

    # counts the number of missing values in the User Type column
    number_of_nonzero = np.count_nonzero(df['User Type'].isnull())
    print("The number of missing values in the \'User Type\' column: {}".format(number_of_missing_values))


def display_data(df):
    """Asks if the user would like to see 5 rows of the data."""

    view_data = str(input("\nWould you like to view 5 rows of individual trip data? Enter yes or no: \n")).lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = str(input("\nWould you like to view 5 more rows? Enter yes or no: \n")).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
