"""
 Comments.
"""

import json


def read_file(file):
    """ . """
    json_data = open(file)
    data = json.load(json_data)
    json_data.close()
    return data


if __name__ == "__main__":
    data = read_file('../../models.json')
    print data["states"][0]
