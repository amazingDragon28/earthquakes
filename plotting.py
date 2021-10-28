from datetime import date

from matplotlib import pyplot as plt
import json
from numpy.core.defchararray import count
import requests 
import numpy as np

def get_data():
    """Retrieve the data we will be working with."""
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

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)


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


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes = [get_magnitude(earthquake) for earthquake in earthquakes]
    return magnitudes
    


def plot_average_magnitude_per_year(earthquakes, number_of_quakes, year):
    sort_quakes = sorted(earthquakes, key = lambda i:i['properties']['time'])
    avg = []
    for i in range(len(number_of_quakes)):
        if i == 0:
            magnitudes = get_magnitudes_per_year(sort_quakes[:number_of_quakes[i]])
            avg.append(np.mean(magnitudes))
        else:
            magnitudes = get_magnitudes_per_year(sort_quakes[np.sum(number_of_quakes[:i]):np.sum(number_of_quakes[:i+1])])
            avg.append(np.mean(magnitudes))

    avg = np.round(avg, decimals=4)

    plt.title("The average magnitude of earthquakes per year")
    plt.xlabel("Year")
    plt.ylabel("The average magnitude")
    for a, b in zip(range(len(year)), avg):
        plt.text(a, b, b, ha="center", va="bottom", fontsize=10)
    
    plt.xticks(range(len(year)), year, rotation=30)
    plt.plot(avg)
    plt.show()
        


def plot_number_per_year(earthquakes):
    years = [get_year(earthquake) for earthquake in earthquakes]
    year = sorted(set(years))
    number_of_quakes = [years.count(i) for i in year]
    plt.figure()
    plt.title("The number of earthquakes per year")
    plt.xlabel("Year")
    plt.ylabel("The number of earthquakes")
    plt.xticks(range(len(year)), year, rotation=30)
    plt.plot(number_of_quakes)

    for a, b in zip(range(len(year)), number_of_quakes):
        plt.text(a, b, b, ha="center", va="bottom", fontsize=10)
    
    plt.show()

    return number_of_quakes, year


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
number_of_quakes, year = plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes, number_of_quakes, year)