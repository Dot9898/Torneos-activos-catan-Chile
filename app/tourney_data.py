

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from time import time
import constants
import urllib.request
import io


def fetch_tourney_data():
    response = urllib.request.urlopen(constants.DATASHEET_LINK)
    data = response.read().decode('utf-8')
    return(pd.read_csv(io.StringIO(data)))

def get_timestamp(date_string):
    date = datetime.strptime(date_string, constants.RECIEVED_DATETIME_FORMAT)
    date = date.replace(tzinfo = constants.SANTIAGO_TIMEZONE)
    timestamp = date.timestamp()
    return(timestamp)

def get_formatted_datetime(timestamp):
    date = datetime.fromtimestamp(timestamp, tz = constants.SANTIAGO_TIMEZONE)
    date = f'{constants.DAYS_IN_SPANISH[date.weekday()]} {date.day}/{date.month}, {date:%H:%M}'
    return(date)

def process_row(tourney, processed_data):
    timestamp = get_timestamp(tourney.date)
    if time() > timestamp + 12 * 3600:   #Don't show tournaments after 12h of their start
        return

    date = get_formatted_datetime(timestamp)
    expansion = constants.EXPANSION[tourney.expansion]
    organization = f'{constants.ORGANIZATION_LINK[tourney.organization]}#{constants.ORGANIZATION_NAME[tourney.organization]}'
    price = f'${float(tourney.price):,.0f}'.replace(',', '.')
    address = tourney.address if tourney.format == 'presencial' else 'Online'
    processed_data.loc[tourney.Index] = [date, 
                                        tourney.region, 
                                        expansion, 
                                        tourney.name, 
                                        organization, 
                                        price, 
                                        tourney.capacity, 
                                        tourney.info_image_link, 
                                        tourney.signup_link, 
                                        address, 
                                        timestamp, 
                                        tourney.format, 
                                        tourney.info_image_link]

def get_processed_dataframe(tourney_data):
    processed_data = pd.DataFrame(columns = constants.DISPLAYED_TOURNEY_INFO_COLUMNS + ['timestamp', 'format', 'info_image_link'])
    processed_data['format'] = pd.Categorical(processed_data['format'], categories = ['presencial', 'online'], ordered = True)

    for tourney in tourney_data.itertuples():
        if constants.IS_LIVE_BUILD:
            process_row(tourney, processed_data)
        else:
            try:
                process_row(tourney, processed_data)
            except:   #If the data processing throws an exception, the tournament just isn't added
                pass

    processed_data.sort_index(inplace = True)
    processed_data.sort_values(by = ['timestamp', 'format'], inplace = True)
    return(processed_data)

def get_display_dataframe(processed_dataframe):
    display_dataframe = processed_dataframe.copy()
    display_dataframe = display_dataframe[constants.DISPLAYED_TOURNEY_INFO_COLUMNS]
    return(display_dataframe)

def get_last_monday_timestamp(delay = 0):
    now = datetime.fromtimestamp(time() - delay)
    last_monday = (now - timedelta(days = now.weekday()))
    last_monday = last_monday.replace(hour = 0,
                                      minute = 0,
                                      second = 0,
                                      microsecond = 0)
    last_monday_ts = last_monday.timestamp()
    return(last_monday_ts)

def get_cropped_dataframe(processed_dataframe):
    cropped_data = processed_dataframe.copy()
    to_drop = []

    for tourney in cropped_data.itertuples():
        if time() > tourney.timestamp:   #Don't download tournaments that already started
            to_drop.append(tourney.Index)
        if tourney.timestamp > get_last_monday_timestamp(delay = constants.NEW_WEEK_DELAY) + 14 * 24 * 3600:
            to_drop.append(tourney.Index)   #Don't download tournaments that are more than 2 weeks from now
        cropped_data.at[tourney.Index, 'Organiza'] = tourney.Organización.split('#')[1]
    
    cropped_data = cropped_data[constants.IMAGE_TOURNEY_INFO_COLUMNS].copy()
    cropped_data.drop(index = to_drop, inplace = True)
    return(cropped_data)

def get_last_monday_string(delay = 0):
    last_monday = datetime.fromtimestamp(get_last_monday_timestamp(delay))
    last_monday_string = f'{last_monday.day} de {constants.MONTHS_IN_SPANISH[last_monday.month - 1]}'
    return(last_monday_string)




















