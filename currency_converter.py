# Created By Parth Dani
# Date 01/05/2020

import json
import requests
import csv


# write your token in below access key
URL = "http://data.fixer.io/api/latest?access_key="


# list of currencies
def is_currency():
    currency_list = ["AFN","ARS","AWG","AUD","AZN","BSD","BBD","BYN","BZD","BMD","BOB","BAM","BWP","BGN","BRL","BND","KHR","CAD","KYD","CLP","CNY","COP","CRC","HRK","CUP","CZK","DKK","DOP","XCD","EGP","SVC","EUR","FKP","FJD","GHS","GIP","GTQ","GGP","GYD","HNL","HKD","HUF","ISK","INR","IDR","IRR","IMP","ILS","JMD","JPY","JEP","KZT","KPW","KRW","KGS","LAK","LBP","LRD","MKD","MYR","MUR","MXN","MNT","MZN","NAD","NPR","ANG","NZD","NIO","NGN","NOK","OMR","PKR","PAB","PYG","PEN","PHP","PLN","QAR","RON","RUB","SHP","SAR","RSD","SCR","SGD","SBD","SOS","ZAR","LKR","SEK","CHF","SRD","SYP","TWD","THB","TTD","TRY","TVD","UAH","GBP","USD","UYU","UZS","VEF","VND","YER","ZWD"]
    return currency_list


# main function for currency conversion
def convert_currency(user_input):
    currency_details = {}
    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_NONE,
                         skipinitialspace=True)
    with open('currency_details.csv') as f:
        reader = csv.reader(f, dialect='myDialect')
        for row in reader:
            currency_details[row[1]] = row[0]
    f.close()

    # if addon words like convert is there in the string -> it will be skipped
    if "convert" in user_input:
        without_convert_list = user_input.split("convert")
        for i in without_convert_list:
            if i != "":
                without_convert_string = i.strip()
    else:
        without_convert_string = user_input

    # remove prepostions from the string
    if "to" in without_convert_string:
        without_preposition_list = without_convert_string.split("to")
    elif "in" in without_convert_string:
        without_preposition_list = without_convert_string.split("in")

    to_currency = without_preposition_list[1].strip().upper()
    from_currency_amount = without_preposition_list[0].strip().split(" ")
    # if input is not in proper format then help user with input format
    if len(from_currency_amount) != 2:
        return "Please try in format '15 usd to inr' "
    if from_currency_amount[0].upper() == from_currency_amount[0]:
        from_currency = from_currency_amount[1].upper()
        amount = from_currency_amount[0]
    else:
        from_currency = from_currency_amount[0].upper()
        amount = from_currency_amount[1]

    # get the current rates of currencies for conversion
    response = requests.get(URL)
    json_format = json.loads(response.text)
    if from_currency not in json_format["rates"] or to_currency not in json_format["rates"]:

        return "Currency not found."
    from_currency_amount = json_format["rates"][from_currency]
    to_currency_amount = json_format["rates"][to_currency]
    conversion = (to_currency_amount / from_currency_amount) * float(amount)
    result = str(amount) + " " + currency_details[from_currency] + " is " + format(conversion, '.3f') + " " + currency_details[to_currency]
    return result


if __name__ == '__main__':
    input_string = input("Please enter the details of conversion as you type in Google Search : ")
    print(convert_currency(input_string))
