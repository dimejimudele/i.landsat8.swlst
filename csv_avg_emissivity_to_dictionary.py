"""
Convert csv data to a dictionary with namedtuples as values

ToDo:
* Add usage examplesi!
* Clean up which test to use for which csv file!
* Clean up which transform function to use according to csv file!
* Clean again...
* Deduplication!
"""

# based on: <http://pastebin.com/tnyhmCJz>
# see: <http://stackoverflow.com/q/29141609/1172302>

# real data
csv = '''Emissivity Class|TIRS10|TIRS11
Cropland|0.971|0.968
Forest|0.995|0.996
Grasslands|0.97|0.971
Shrublands|0.969|0.97
Wetlands|0.992|0.998
Waterbodies|0.992|0.998
Tundra|0.98|0.984
Impervious|0.973|0.981
Barren Land|0.969|0.978
Snow and ice|0.992|0.998'''

# required librairies -------------------------------------------------------
import sys
import csv
import collections
import random

# set user defined csvfile, if any
if len(sys.argv) > 1:
    CSVFILE=sys.argv[1]
    print "User defined csv file:", CSVFILE
else:
    CSVFILE = ''


# helpers -------------------------------------------------------------------
def is_number(value):
    '''
    Check if input is a number
    '''
    try:
        float(value)  # for int, long and float
    except ValueError:
        try:
            complex(value)  # for complex
        except ValueError:
            return False
    return value


def replace_dot_comma_space(string):
    """
    Source: <http://stackoverflow.com/a/9479972/1172302>
    """
    replacements = ('.', ''), (', ', '_'), (',', '_'), (' ', '_'), ('(', ''), (')', ''), ('/', '_')
    return reduce(lambda alpha, omega: alpha.replace(*omega),
                  replacements, string)


def csv_reader(csv_file):
    '''
    Transforms csv from a file into a multiline string. For example,
    the following csv

    --%<---
    Emissivity Class|TIRS10|TIRS11
    Cropland|0.971|0.968
    Forest|0.995|0.996
    Grasslands|0.97|0.971
    Shrublands|0.969|0.97
    Wetlands|0.992|0.998
    Waterbodies|0.992|0.998
    Tundra|0.98|0.984
    Impervious|0.973|0.981
    Barren Land|0.969|0.978
    Snow and ice|0.992|0.998
    --->%--

    will be returned as:

    """Emissivity Class|TIRS10|TIRS11
    Cropland|0.971|0.968
    Forest|0.995|0.996
    Grasslands|0.97|0.971
    Shrublands|0.969|0.97
    Wetlands|0.992|0.998
    Waterbodies|0.992|0.998
    Tundra|0.98|0.984
    Impervious|0.973|0.981
    Barren Land|0.969|0.978
    Snow and ice|0.992|0.998"""
    '''
    with open(csv_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter="|")  # delimiter?
        string = str()
        for row in csvreader:
            string += '\n' + str('|'.join(row))
        string = string.strip('\n')  # remove first newline!
        return string


def csv_to_dictionary(csv):
    '''
    Transform input from csv into a python dictionary with namedtuples as
    values
    '''
    # split input in rows
    rows = csv.split('\n')
    print "Rows:", rows
    print

    dictionary = {}  # empty dictionary
    fields = rows.pop(0).split('|')[1:]  # header
    print "Fields:", fields
    print

    def transform(row):
        '''
        Transform an input row as follows
        '''
        elements = row.split('|')  # split row in elements
        key = replace_dot_comma_space(elements[0])  # key: 1st column, replace
        ect = collections.namedtuple(key, [fields[0], fields[1]])  # namedtuple

        # feed namedtuples
        ect.TIRS10, ect.TIRS11 = is_number(elements[1]), is_number(elements[2])
        dictionary[key] = dictionary.get(key, ect)  # feed dictionary

    def transform_cwv(row):
        '''
        Transform an input row as follows
        '''
        elements = row.split('|')  # split row in elements
        key = replace_dot_comma_space(elements[0])  # key: 1st column, replace
        cwv = collections.namedtuple(key,
                                     [replace_dot_comma_space(fields[0]),
                                      replace_dot_comma_space(fields[1]),
                                      replace_dot_comma_space(fields[2]),
                                      replace_dot_comma_space(fields[3]),
                                      replace_dot_comma_space(fields[4]),
                                      replace_dot_comma_space(fields[5]),
                                      replace_dot_comma_space(fields[6]),
                                      replace_dot_comma_space(fields[7]),
                                      replace_dot_comma_space(fields[8]),
                                      replace_dot_comma_space(fields[9])])  # named tuples

        # feed namedtuples
        cwv.subrange = is_number(elements[0])
        cwv.b0 = is_number(elements[1])
        cwv.b1 = is_number(elements[2])
        cwv.b2 = is_number(elements[3])
        cwv.b3 = is_number(elements[4])
        cwv.b4 = is_number(elements[5])
        cwv.b5 = is_number(elements[6])
        cwv.b6 = is_number(elements[7])
        cwv.b7 = is_number(elements[8])
        cwv.rmse = is_number(elements[9])
        dictionary[key] = dictionary.get(key, cwv)  # feed dictionary

    #map(transform, rows)
    map(transform_cwv, rows)
    return dictionary


# main
def main():
    """
    Main function:
    - reads a csv file (or a multi-line string)
    - converts and returns a dictionary which contains named tupples
    """
    global CSVFILE
    if CSVFILE == '':
        print '>>> No user-define csv file.'
        CSVFILE = "average_emissivity.csv"
        print '>>> Using the "default"', CSVFILE, 'file'
    else:
        print " * Using the file", CSVFILE
    csvstring = csv_reader(CSVFILE)
    emissivity_coefficients = csv_to_dictionary(csvstring)  # csv < from string
    print ("Emissivity coefficients (using named tupples):\n",
           emissivity_coefficients)
    return emissivity_coefficients


# Test data
def test_using_file(file):
    '''
    Test helper functions and main function using a csv file as an input.
    '''
    number = random.randint(1., 10.)
    print " * Testing 'is_number':", is_number(number)

    if not file:
        csvfile = "average_emissivity.csv"
    else:
        csvfile = file

    print " * Testing 'csv_reader' on", csvfile, ":\n\n", csv_reader(csvfile)
    print

    csvstring = csv_reader(csvfile)
    print " * Testing 'csv_to_dictionary':\n\n", csv_to_dictionary(csvstring)
    print

    d = csv_to_dictionary(csvstring)
    somekey = random.choice(d.keys())
    print "* Some random key:", somekey

    fields = d[somekey]._fields
    print "* Fields of namedtuple:", fields

    random_field = random.choice(fields)
    print "* Some random field:", random_field
    # print "* Return values (namedtuple):", d[somekey].TIRS10, d[somekey].TIRS11
    print "* Return values (namedtuple):", (d[somekey].b0,
                                            d[somekey].b1)

#test_using_file(CSVFILE)  # Ucomment to run test function!
CSVFILE = "cwv_coefficients.csv"
test_using_file("cwv_coefficients.csv")
CSVFILE = ''

def test(testdata):
    '''
    Test helper functions and main function using a multi-line string as an
    input.
    '''
    number = random.randint(1., 10.)
    print " * Testing 'is_number':", is_number(number)
    print

    '''
    Testing the process...
    '''
    d = csv_to_dictionary(testdata)
    print "Dictionary is:\n", d
    print

    somekey = random.choice(d.keys())
    print "Some random key:", somekey
    print

    fields = d[somekey]._fields
    print "Fields of namedtuple:", fields
    print

    random_field = random.choice(fields)
    print "Some random field:", random_field
    print "Return values (namedtuple):", d[somekey].TIRS10, d[somekey].TIRS11

testdata = '''LandCoverClass|TIRS10|TIRS11
Cropland|0.971|0.968
Forest|0.995|0.996
Grasslands|0.970|0.971
Shrublands|0.969|0.970
Wetlands|0.992|0.998
Waterbodies|0.992|0.998
Tundra|0.980|0.984
Impervious|0.973|0.981
Barren_Land|0.969|0.978
Snow_and_Ice|0.992|0.998'''

#test(testdata)  # Ucomment to run the test function!

''' Output ------------------------------
{'Wetlands': <class '__main__.Wetlands'>,
 'Snow_and_Ice': <class '__main__.Snow_and_Ice'>,
 'Impervious': <class '__main__.Impervious'>,
 'Grasslands': <class '__main__.Grasslands'>,
 'Shrublands': <class '__main__.Shrublands'>,
 'Cropland': <class '__main__.Cropland'>,
 'Tundra': <class '__main__.Tundra'>,
 'Barren_Land': <class '__main__.Barren_Land'>,
 'Forest': <class '__main__.Forest'>,
 'Waterbodies': <class '__main__.Waterbodies'>}
------------------------------------ '''

if __name__ == "__main__":
    main()