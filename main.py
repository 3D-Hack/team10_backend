import os
import requests
import datetime
import json


def get_average_kilometerage(vrm, average=10000):
    headers = {
        "x-api-key": os.getenv('MOT_API_KEY'),
        "Content-Type": "application/json",
    }
    response = requests.get(
        os.getenv('MOT_API_URL'), params={"registration": vrm}, headers=headers
    )

    if response.status_code != 200:
        raise Exception("OMG. Not 200.")

    response_json = response.json()[0]

    if "motTests" not in response_json:
        return average

    year = datetime.datetime.today().year
    lasttest = response_json["motTests"][0]
    distance = int(lasttest["odometerValue"])
    if lasttest["odometerUnit"] == "mi":
        distance = distance / 0.62137119
    regyear = datetime.datetime.strptime(
        response_json["registrationDate"], "%Y.%m.%d"
    ).year
    apart = year - regyear
    return distance / apart


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def get_vehicle_info(vrm):
    headers = {
        "x-api-key": os.getenv('DVLA_API_KEY'),
        "Content-Type": "application/json",
    }
    response = requests.post(
        os.getenv('DVLA_API_URL'),
        json={"registrationNumber": vrm},
        headers=headers,
    )

    if response.status_code != 200:
        raise Exception("OMG. Not 200.")

    motStatus = response.json()["motStatus"] in ("Valid", "Not valid")

    average = 10000
    if motStatus:
        average = get_average_kilometerage(vrm)

    convert_co2_result = convert_co2(response.json()["co2Emissions"], average)

    removed = convert_co2_result.popitem()

    return {
        "co2": response.json()["co2Emissions"],
        "make": response.json()["make"],
        "colour": response.json()["colour"],
        "averageKilometersYear": round(average),
        "convertCo2": convert_co2_result,
        "text_string": removed[1]
    }


def format_reponse_string(num_item, item):
    """
    Hackathon level string formating. 
    """

    return (
        str(int(num_item)) + (" " + item + "s" if num_item > 1 else " " + item)
        if num_item > 0
        else ""
    )


def convert_co2(co2, mileage):
    """
    Convert emmissions to some other stats
    co2 in g/km
    mileage in km
    """

    co2_target = 90  # gCO2/km target from the eu.
    total_co2 = (co2 - co2_target) * mileage

    # set some co2 grams equivalent
    trees, steaks, cheese, avocado = 9999, 4000, 3000, 200

    num_trees, rem = divmod(total_co2, trees)
    num_steak, rem = divmod(rem, steaks)
    num_cheese, rem = divmod(rem, cheese)
    num_avocado, rem = divmod(rem, avocado)

    # 100*long_haul_flight*passengers
    rocket_equivalents = round(100 * 2000000 * 4 / total_co2)

    # Dont judge me! i think it works
    tree_string = format_reponse_string(num_trees, "tree")
    steak_string = format_reponse_string(num_steak, "steak")
    avo_string = format_reponse_string(num_avocado, "avo")
    cheese_string = format_reponse_string(num_cheese, "cheesey kilo")

    msg = (
        f"Your car is producing {total_co2/1000:.1f} kg CO2 per year over the EU target (90 g/km). "
        + f"You can offset that by planting or saving {tree_string} and "
        + f"avoiding {steak_string}, {cheese_string}, {avo_string}."
        + f" Or we could forgo 1 of Branson/Bezos rocket trips and drive for {rocket_equivalents} years."
    )

    msg = msg.replace(" , ", " ").replace(", ,", ",").replace(", .", ".")
    if msg.count(",") > 1:
        msg = ".".join(msg.rsplit(",", 1))

    if msg.count(",") > 0:
        msg = " and".join(msg.rsplit(",", 1))

    msg = msg.replace("  ", " ")

    return {
        "trees": num_trees,
        "avocado": num_avocado,
        "steaks": num_steak,
        "cheese": num_cheese,
        "text_string": msg,
    }


def lambda_function(event, context):
    vrm = event["queryStringParameters"]["vrm"]
    print(event)
    myvar = get_vehicle_info(vrm)
    response = {
        "statusCode": 200,
        "body": json.dumps(myvar),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }

    return response


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print(get_vehicle_info(input('Enter VRM: ')))
