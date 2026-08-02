

import pandas as pd
from datetime import datetime, timedelta
from time import time
import constants


def fetch_tourney_data():
    return(pd.read_csv(constants.DATASHEET_LINK))

def get_timestamp(date_string):
    date = datetime.strptime(date_string, constants.RECIEVED_DATETIME_FORMAT)
    date = date.replace(tzinfo = constants.SANTIAGO_TIMEZONE)
    timestamp = date.timestamp()
    return(timestamp)

def get_formatted_datetime(timestamp):
    date = datetime.fromtimestamp(timestamp, tz = constants.SANTIAGO_TIMEZONE)
    date = f'{constants.DAYS_IN_SPANISH[date.weekday()]} {date.day}/{date.month}, {date:%H:%M}'
    return(date)

def get_display_dataframe(tourney_data):
    display_data = pd.DataFrame(columns = constants.DISPLAYED_TOURNEY_INFO_COLUMNS + ['timestamp', 'format', 'info_image_link'])
    display_data['format'] = pd.Categorical(display_data['format'], categories = ['presencial', 'online'], ordered = True)
    
    for tourney in tourney_data.itertuples():

        timestamp = get_timestamp(tourney.date)
        if time() > timestamp + 12 * 3600:   #Don't show tournaments after 12h of their start
            continue

        date = get_formatted_datetime(timestamp)
        expansion = constants.EXPANSION[tourney.expansion]
        organization = f'{constants.ORGANIZATION_LINK[tourney.organization]}#{constants.ORGANIZATION_NAME[tourney.organization]}'
        address = tourney.address if tourney.format == 'presencial' else 'Online'
        display_data.loc[tourney.Index] = [date, 
                                           tourney.region, 
                                           expansion, 
                                           tourney.name, 
                                           organization, 
                                           tourney.price, 
                                           tourney.capacity, 
                                           tourney.info_image_link, 
                                           tourney.signup_link, 
                                           address, 
                                           timestamp, 
                                           tourney.format, 
                                           tourney.info_image_link]

    display_data.sort_index(inplace = True)
    display_data.sort_values(by = ['timestamp', 'format'], inplace = True)

    return(display_data)

def get_last_monday_timestamp():
    now = datetime.now()
    last_monday = (now - timedelta(days = now.weekday()))
    last_monday = last_monday.replace(hour = 0,
                                      minute = 0,
                                      second = 0,
                                      microsecond = 0)
    last_monday_ts = last_monday.timestamp()
    return(last_monday_ts)

def get_cropped_dataframe(tourney_data):
    display_data = get_display_dataframe(tourney_data)
    to_drop = []

    for tourney in display_data.itertuples():
        if time() > tourney.timestamp:   #Don't download tournaments that already started
            to_drop.append(tourney.Index)
        if tourney.timestamp > get_last_monday_timestamp() + 14 * 24 * 3600:
            to_drop.append(tourney.Index)   #Don't download tournaments that are more than 2 weeks from now
        display_data.at[tourney.Index, 'Precio'] = f'${tourney.Precio:,.0f}'.replace(',', '.')
        display_data.at[tourney.Index, 'Organiza'] = tourney.Organización.split('#')[1]
    
    cropped_data = display_data[constants.IMAGE_TOURNEY_INFO_COLUMNS]
    cropped_data.drop(index = to_drop, inplace = True)
    return(cropped_data)

def get_last_monday_string():
    last_monday = datetime.fromtimestamp(get_last_monday_timestamp())
    last_monday_string = f'{last_monday.day} de {constants.MONTHS_IN_SPANISH[last_monday.month - 1]}'
    return(last_monday_string)




















