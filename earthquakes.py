# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

import matplotlib.pyplot as plt
import numpy as np
from datetime import date

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )


    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open('quakesinfo.json', 'w') as json_file:
        json.dump(json.loads(text), json_file, indent=4)
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    coordinates = earthquake["geometry"]["coordinates"]
    # There are three coordinates, but we don't care about the third (altitude)
    return (coordinates[0], coordinates[1])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    current_max_magnitude = get_magnitude(data["features"][0])
    current_max_location = get_location(data["features"][0])
    for item in data["features"]:
        magnitude = get_magnitude(item)
        # Note: what happens if there are two earthquakes with the same magnitude?
        if magnitude > current_max_magnitude:
            current_max_magnitude = magnitude
            current_max_location = get_location(item)
    return current_max_magnitude, current_max_location
    # There are other ways of doing this too:
    # biggest_earthquake = sorted(data["features"], key=get_magnitude)[0]
    # return get_magnitude(biggest_earthquake), get_location(biggest_earthquake)
    # Or...
    # biggest_earthquake = max(
    #     ({"mag": get_magnitude(item), "location": get_location(item)}
    #     for item in data["features"]),
    #     key=lambda x: x["mag"]
    # )
    # return biggest_earthquake["mag"], biggest_earthquake["location"]

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year

def get_magnitudes_per_year(earthquakes):

    year_dict={}
    for quake in earthquakes:
        if get_year(quake) in year_dict:
            year_dict[get_year(quake)].append(get_magnitude(quake))
        else:
            year_dict[get_year(quake)] = [get_magnitude(quake)]
    return year_dict

def plot_average_magnitude_per_year(earthquakes):
    dict = get_magnitudes_per_year(earthquakes)
    year_list =[]
    avg_list=[]
    for item in dict:
        year_list.append(item)

    year_list.sort()

    for year in year_list:
        mag_list = dict[year]
        value = 0
        for mag in mag_list:
            value += mag
        avg_list.append(value / len(mag_list))

    plt.title('Average Magnitude per Year')
    plt.plot(year_list, avg_list)
    plt.xlabel('Year')
    plt.xticks(year_list, rotation=45)
    plt.ylabel('Average Magnitutde')
    plt.show()

def plot_number_per_year(earthquakes):
    dict = get_magnitudes_per_year(earthquakes)
    year_list =[]
    num_list=[]
    for item in dict:
        year_list.append(item)

    year_list.sort()
    for year in year_list:
        num_list.append(len(dict[year]))

    plt.title('Number of Earthquakes per Year')

    plt.bar(year_list , num_list)
    plt.legend()
    plt.xlabel('Year')
    plt.xticks(year_list , rotation=45)
    plt.ylabel('Number')
    plt.show()
    plt.clf()
    plt.plot(year_list , num_list)
    plt.xlabel('Year')
    plt.xticks(year_list , rotation=45)
    plt.ylabel('Number')
    plt.show()

# With all the above functions defined, we can now call them and get the result
# data = get_data()
# print(f"Loaded {count_earthquakes(data)}")
# max_magnitude, max_location = get_maximum(data)
# print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

# quakes = get_data()['features']
# plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
# plot_average_magnitude_per_year(quakes)