

import pandas as pd
from datetime import datetime
from time import time
import constants
from PIL import ImageFont


def fetch_tourney_data():
    return(pd.read_csv(constants.DATASHEET_LINK))

def get_timestamp(date_string):
    date = datetime.strptime(date_string, constants.RECIEVED_DATETIME_FORMAT)
    date = date.replace(tzinfo = constants.SANTIAGO_TIMEZONE)
    timestamp = date.timestamp()
    return(timestamp)

def get_formatted_datetime(timestamp):
    date = datetime.fromtimestamp(timestamp, tz = constants.SANTIAGO_TIMEZONE)
    if date.hour == 0:
        date = f'{constants.DAYS_IN_SPANISH[date.weekday()]} {date.day}/{date.month}'
    else:
        date = f'{constants.DAYS_IN_SPANISH[date.weekday()]} {date.day}/{date.month}, {date.hour}:{date:%M}'
    return(date)

def get_formatted_expansions(expansions_string):
    expansions = [expansion.strip() for expansion in expansions_string.split(',')]
    formatted_expansions = []
    for expansion in expansions:
        if len(expansions) > 1:
            formatted_expansion = constants.EXPANSION_SHORT[expansion]
        else:
            formatted_expansion = constants.EXPANSION[expansion]
        formatted_expansions.append(formatted_expansion)
    all_formatted = ', '.join(formatted_expansions)
    return(all_formatted)

def process_row(tourney, processed_data):
    if tourney.show != 'y':
        return
    
    timestamp = get_timestamp(tourney.date)
    if time() > timestamp + constants.TIME_TOURNAMENTS_ARE_SHOWN_AFTER_STARTING:
        return

    date = get_formatted_datetime(timestamp)
    expansions = get_formatted_expansions(tourney.expansion)
    organization = f'{constants.ORGANIZATION_LINK[tourney.organization]}#{constants.ORGANIZATION_NAME[tourney.organization]}'
    price = pd.NA if pd.isna(tourney.price) else f'${float(tourney.price):,.0f}'.replace(',', '.')
    processed_data.loc[tourney.Index] = [date, 
                                         tourney.region, 
                                         expansions, 
                                         tourney.name, 
                                         organization, 
                                         price, 
                                         tourney.capacity, 
                                         tourney.info_image_link, 
                                         tourney.signup_link, 
                                         tourney.address, 
                                         timestamp, 
                                         tourney.format, 
                                         tourney.info_image_link]

def get_processed_dataframe(tourney_data):
    processed_data = pd.DataFrame(columns = constants.DISPLAYED_TOURNEY_INFO_COLUMNS + ['timestamp', 'format', 'info_image_link'])

    for tourney in tourney_data.itertuples():
        if constants.IS_LIVE_BUILD:
            try:
                process_row(tourney, processed_data)
            except:   #If the data processing throws an exception, the tournament just isn't added
                continue
        else:
            process_row(tourney, processed_data)
    
    processed_data.sort_index(inplace = True)
    if constants.ALWAYS_SHOW_ONLINE_AFTER_PRESENCIAL:
        processed_data['format'] = pd.Categorical(processed_data['format'], categories = ['presencial', 'online'], ordered = True)
        processed_data.sort_values(by = ['format', 'timestamp'], inplace = True)
    else:
        processed_data.sort_values(by = ['timestamp'], inplace = True)
    
    return(processed_data)

def get_display_dataframe(processed_dataframe, show_online):
    display_dataframe = processed_dataframe.copy()
    if not show_online:
        display_dataframe = display_dataframe[display_dataframe['Región'] != 'Online']
    display_dataframe = display_dataframe[constants.DISPLAYED_TOURNEY_INFO_COLUMNS]
    return(display_dataframe)

def get_column_width(column):
    font = ImageFont.truetype(constants.SOURCE_SANS_PATH, 16)
    entries = [str(entry) for entry in column if not pd.isna(entry)]
    if not entries:
        return(None)
    widths = [font.getlength(entry) for entry in entries]
    column_width = round(max(widths))
    return(column_width)

def get_month_start_timestamp(delay = 0):
    now = time() + delay
    now = datetime.fromtimestamp(now)
    month_start = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
    month_start_ts = month_start.timestamp()
    return(month_start_ts)

def get_cropped_dataframe(processed_dataframe):
    cropped_data = processed_dataframe.copy()
    current_timestamp = time()
    to_drop = []

    for tourney in cropped_data.itertuples():
        if current_timestamp > tourney.timestamp + constants.TIME_TOURNAMENTS_ARE_SHOWN_AFTER_STARTING:
            to_drop.append(tourney.Index)
        if tourney.timestamp > current_timestamp + constants.TOURNAMENT_DOWNLOAD_LIMIT:
            to_drop.append(tourney.Index)
        cropped_data.at[tourney.Index, 'Organiza'] = tourney.Organización.split('#')[1]
    
    cropped_data = cropped_data[constants.IMAGE_TOURNEY_INFO_COLUMNS].copy()
    cropped_data.drop(index = to_drop, inplace = True)
    return(cropped_data)

def get_current_month_string(delay = 0):
    month_start = datetime.fromtimestamp(get_month_start_timestamp(delay))
    current_month_string = constants.MONTHS_IN_SPANISH[month_start.month - 1]
    return(current_month_string)














