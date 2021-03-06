__author__ = 'kamil'

import requests
import configparser

def get_key():
    global api_key
    config = configparser.ConfigParser()
    config.read("key.ini")
    api_key = config["KEY"]["api_key"]


def transform(name):
    ret = name.replace(" ", "+")
    ret = ret.replace(",", "+")
    return ret


def get_code(name):
    global r
    postal_code = ""
    url_city = "https://maps.googleapis.com/maps/api/geocode/json?address=" + str(name) + "&key=" + api_key
    r = requests.get(url_city)
    for i in range(len(r.json()["results"][0]["address_components"])):
        if r.json()["results"][0]["address_components"][i]["types"] == ["postal_code"]:
            postal_code = r.json()["results"][0]["address_components"][i]["long_name"]
    if postal_code:
        return postal_code
    else:
        return False


def get_coordinates(name):
    global r    # no need of repeated request (geolocation API limits)
    lng = r.json()["results"][0]["geometry"]["location"]["lng"]
    lat = r.json()["results"][0]["geometry"]["location"]["lat"]
    return lat, lng


def get_code_from_coord(lat, lng):
    url_loc = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng) + "&key="\
        + api_key
    s = requests.get(url_loc)
    postal_codes = []

    for i in range(len(s.json()["results"])):
        for j in range(len(s.json()["results"][i]["address_components"])):
            values = s.json()["results"][i]["address_components"][j].values()
            for k in range(len(values)):
                if ["postal_code"] in values and list(values)[k] not in postal_codes and list(values)[k]\
                != ['postal_code']:    # in 3. cond. 'is not' doesn't work
                    postal_codes.append(list(s.json()["results"][i]["address_components"][j].values())[k])

    if len(postal_codes) > 1:
        print(resp["more_codes"])

    return postal_codes[0]


def choose_language():
    print("Choose language:\n\tEN - English\n\tPL - Polish\n")
    lng = input()
    global resp
    if lng.lower() == "pl":
        resp = {"put_city": "Wprowadź lokalizację: ",
                "city_postal": "Kod pocztowy miasta",
                "not_found": "Nie znaleziono",
                "iis": "to:",
                "more_codes": "Ta lokalizacja posiada więcej kodów pocztowych, istnieje ryzyko,\
                                że kod może być nieprawidłowy."
                }
    else:
        resp = {"put_city": "Type location: ",
                "city_postal": "Postal code of",
                "not_found": "Not found",
                "iis": "is:",
                "more_codes": "This location has more postal codes, this postal code may be incorrect"
                }

if __name__ == "__main__":
    get_key()
    choose_language()

    city_in = input(resp["put_city"])
    city = transform(city_in)

    try:
        postal_code = get_code(city)
        if not postal_code:
            lattitude, longtitude = get_coordinates(city)
            postal_code = get_code_from_coord(lattitude, longtitude)
        print(resp["city_postal"], city_in, resp["iis"], postal_code)

    except IndexError:
        print(resp["not_found"])

else:
    # deafult vaule of resp for testing
    resp = {"put_city": "Type location: ",
                "city_postal": "Postal code of",
                "not_found": "Not found",
                "iis": "is:",
                "more_codes": "This location has more postal codes, this postal code may be incorrect"
                }

