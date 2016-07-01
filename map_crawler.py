import requests
import MySQLdb
import simplejson as json

cnxn = MySQLdb.connect(host="localhost", user="root", passwd="harshit@123", db="college_info", charset="utf8",
                       use_unicode=True)
cursor = cnxn.cursor()
cnxn.autocommit(True)

query = "select pub.college_name from pub_college_aspects_ranking pub left join pvt_college_aspects_ranking pvt " \
        "on pub.id = pvt.id union select pvt.college_name from pub_college_aspects_ranking pub right join pvt_college_aspects_ranking pvt " \
        "on pub.id = pvt.id"
cursor.execute(query)
collect_data = cursor.fetchall()

query1 = "select college_name from bounding_box_details"
cursor.execute(query1)
bb_data = cursor.fetchall()

check_data = []

for item in bb_data:
    check_data.append(str(item[0]))

for row in collect_data:

    try:
        input_val = str(row[0])

        if input_val not in check_data:

            map_url = "https://maps.googleapis.com/maps/api/geocode/json"
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
            parameters = {'address': input_val, 'key': 'AIzaSyCvpWn0CSxjr1CI4tJAIzwuKc3HftGZIA0'}

            bb_data = requests.get(url=map_url, params=parameters)
            coordinates = bb_data.json()

            bb = coordinates['results'][0]['geometry']['viewport']

            lng_ne = bb['northeast']['lng']
            lat_ne = bb['northeast']['lat']
            lng_sw = bb['southwest']['lng']
            lat_sw = bb['southwest']['lat']

            box = ','.join((str(lng_sw), str(lat_sw), str(lng_ne), str(lat_ne)))

            query1 = "insert into bounding_box_details (college_name,bounding_box) values (%s,%s)"
            data1 = (input_val, box)
            cursor.execute(query1, data1)

    except Exception as e:
        print "Error in  ", row, " : coords_collection", e
        continue
