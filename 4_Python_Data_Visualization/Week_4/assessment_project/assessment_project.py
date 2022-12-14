"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal
# import os


def dict_reader(file, keyfield, separator=',', quote="'"):
    """
    Inputs:
      file  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    with open(file, newline = '', encoding = 'utf-8') as csv_file:
        data = csv.DictReader(csv_file, delimiter = separator, quotechar = quote)
        my_data = {row[keyfield]: row for row in data}

    return my_data

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    with open(codeinfo['codefile'], newline = '', encoding = 'utf-8') as csv_file:
        data = csv.DictReader(csv_file, delimiter = codeinfo['separator'], 
                              quotechar = codeinfo['quote'])
        my_data = {row[codeinfo['plot_codes']]: row[codeinfo['data_codes']] for row in data}
    
    return my_data


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    my_dict, my_set = {}, set()
    countries = {gdp_countries[key]['Country Name']: key for key in gdp_countries}
    
    for key in plot_countries:
        if plot_countries[key] in countries:
            my_dict[key] = countries[plot_countries[key]]
        else:
            my_set.add(key)
            
    return my_dict, my_set

def select(plot_countries, my_dict):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      my_dict - Dictionary whose keys are country codes used in code data

    Output:
      A dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.
    """
    countries, set_one = {}, set()
    for key in plot_countries:
        if plot_countries[key] in my_dict:
            countries[key] = my_dict[plot_countries[key]]
        else:
            set_one.add(key)
    return countries, set_one


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_dict = dict_reader(file=gdpinfo['gdpfile'],
                           keyfield= gdpinfo['country_code'],
                           separator=gdpinfo['separator'],
                           quote=gdpinfo['quote'])
    
    gdp_dict = {key.upper(): gdp_dict[key] for key in gdp_dict}

    code_dict = dict_reader(file=codeinfo['codefile'],
                            keyfield=codeinfo['plot_codes'],
                            separator=codeinfo['separator'],
                            quote=codeinfo['quote'])
    # map the countries that apper in the gdp_dict and code_dict
    countries = {}
    for key in code_dict:
        if code_dict[key][codeinfo['data_codes']].upper() in gdp_dict:
            countries[key] = code_dict[key]
    
    # change countries keys that match plot_countries and save plot_countries 
    # keys that don't match in a set
    countries2, set_one = select(plot_countries, countries)
    
    # compute the log (base 10) of the GDP for the associated country in the given year
    result, set_two = {}, set()
    for key, value in countries2.items():
        try:
            result[key] = math.log10(
                float(gdp_dict[value[codeinfo['data_codes']].upper()][year])
                )
        except ValueError:
            set_two.add(key)
            
    return result, set_one, set_two

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
