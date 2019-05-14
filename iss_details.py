#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import requests

from datetime import datetime


LOC_URL = 'http://api.open-notify.org/iss-now.json'
PAS_URL = 'http://api.open-notify.org/iss-pass.json?lat={0}&lon={1}'
PPL_URL = 'http://api.open-notify.org/astros.json'


class ParsingError(Exception):
    """ Custom exception in the event that the data format changed and we cannot parse it correctly. """
    pass


def convert_unixtime_to_str(unix_ts):
    """ Helper function to convert a unix timestamp to string (YYYY/MM/DD hr:mn:sc). """
    try:
        unix_ts = int(unix_ts)
        date_str = datetime.utcfromtimestamp(unix_ts).strftime('%Y/%m/%d %H:%M:%S')
    except ValueError, TypeError:
        print('Could not convert unix_timestamp value {0}'.format(unix_ts))
        raise

    return date_str


def validate_latitude(lat):
    """ Validate that the given latitude value is between -90 and 90. """

    if lat < -90 or lat > 90:
        # None evaluates to < -90 so will be caught here
        return False

    return True


def validate_longitude(lon):
    """ Validate that the given longitude value is between -90 and 90. """

    if lon < -180 or lon > 180:
        # None evaluates to < -180 so will be caught here
        return False

    return True


def get_current_iss_loc(*args, **kwargs):
    """ Print details regarding the current location of the ISS. """

    # Make call to API via requests
    res = requests.get(LOC_URL)

    # Parse response obj via json
    data = json.loads(res.content)

    # Get timestamp and latitude/longitude and print the output
    try:
        time = convert_unixtime_to_str(data['timestamp'])
        lat = data['iss_position']['latitude']
        lon = data['iss_position']['longitude']

        print('The current location of the ISS, at time {0}, is ({1}, {2})'.format(
                time, lat, lon))

    except KeyError as e:
        raise ParsingError('Something went wrong when parsing the returned data: {0}'.format(e))


def get_iss_passing_details(*args, **kwargs):
    """ Print details regarding when the ISS will pass a given location (lat, lon). """

    # Pull the lat and lon values from kwargs, raise ValueError if not present
    lat = kwargs.get('lat')
    lon = kwargs.get('lon')

    # Validate both latitude and longitude values
    if not validate_latitude(lat):
        raise ValueError('Latitude (-lat) must be of a value between -90 and 90')

    if not validate_longitude(lon):
        raise ValueError('Longitude (-lon) must be of a value between -180 and 180')

    # Make call to API via requests qith lat and lon formatted into the url
    res = requests.get(PAS_URL.format(lat, lon))

    # Parse response obj via json
    data = json.loads(res.content)

    # Get list of passes and print them out
    try:
        passes = data['response']
        print("There are {0} upcoming passes for location ({1}, {2}):".format(len(passes), lat, lon))
        for upcoming_passes in passes:
            time = convert_unixtime_to_str(upcoming_passes['risetime'])
            duration = upcoming_passes['duration']

            print('The ISS will be overhead location ({0}, {1}) at time {2} for {3} seconds'.format(
                lat, lon, time, duration))

    except KeyError as e:
        raise ParsingError('Something went wrong when parsing the returned data: {0}'.format(e))


def get_num_people_in_space_and_craft(*args, **kwargs):
    """ Print details regarding the number of people in space and the craft they are on. """

    # Make call to API via requests
    res = requests.get(PPL_URL)

    # Parse response obj via json
    data = json.loads(res.content)

    # Get list of people in space and the craft they are on and print the details
    try:
        total_num_ppl = data['number']
        people = data['people']

        # Reformat the returned data['people'] to get a list of people per craft
        crafts = {i['craft']:[] for i in people}
        for person in people:
            craft = person['craft']
            name = person['name']

            crafts[craft].append(name)

        # Print out the list of people aboard per craft
        for craft in crafts:
            num_ppl = len(crafts[craft])
            ppl = ', '.join(crafts[craft])
            print('There are {0} people aboard the {1}. They are: {2}'.format(
                num_ppl, craft, ppl))

    except KeyError as e:
        raise ParsingError('Something went wrong when parsing the returned data: {0}'.format(e))


# Dict to store functions associated with primary command line arguments
COMMANDS = { #TODO The above functions and this dict would ideally be in a separate script
    'loc': get_current_iss_loc,
    'pass': get_iss_passing_details,
    'people': get_num_people_in_space_and_craft,
}


def parse_cl_args():
    """ Parses command line arguments and returns them as a dictionary """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process input arguments')

    # Add command line arguments
    parser.add_argument('primary_command', metavar='Input', type=str, nargs=1,
            help='Expects a single argument of "loc", "pass", or "people"')
    parser.add_argument('-lat', metavar='Latitude', type=float,
            help='Required only for pass command, expects a latitude value as a number between -90 and 90', default=None)
    parser.add_argument('-lon', metavar='Longitude', type=float,
            help='Required only for pass command, expects a longitude value as a number between -180 and 180', default=None)

    # Send command line arguments to dict
    cl_args = vars(parser.parse_args())

    # Since nargs puts this arg in a list, need to pull it out
    cl_args['primary_command'] = cl_args['primary_command'][0]

    return cl_args


def run(cl_args):
    """ Primary run function. expects cl_args as a dict object. """
    # Extract primary_command argument
    primary_command = cl_args.pop('primary_command')

    # Try to run function associated with primary_command argument
    try:
        func = COMMANDS[primary_command]
        func(**cl_args) # Send with unpacked cl_args dict
    except KeyError:
        print('Argument "{0}" not recognized'.format(primary_command))
    except ParsingError as e:
        print(e)


if __name__ == '__main__':
    cl_args = parse_cl_args()
    run(cl_args)
