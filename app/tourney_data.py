

import streamlit as st
import pandas as pd
from datetime import datetime
import dataframe_image as dfi
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

def get_cropped_dataframe(tourney_data):
    display_data = get_display_dataframe(tourney_data)
    cropped_data = display_data[constants.IMAGE_TOURNEY_INFO_COLUMNS] #chequear cambiar org al final
    return(cropped_data)

def get_as_image(dataframe):
    return(dfi.export(dataframe, 'Torneos_catan_Chile.png'))

























