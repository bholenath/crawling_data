import requests
from lxml.html import parse
import MySQLdb
import sys

cnxn = MySQLdb.connect(host="localhost", user="root", passwd="harshit@123", db="college_info", charset="utf8", use_unicode=True)
cursor = cnxn.cursor()
cnxn.autocommit(True)

try:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'}
    url = requests.get(url='https://colleges.niche.com/rankings/top-public-universities', headers=headers)
    url1 = requests.get(url='https://colleges.niche.com/rankings/top-private-universities', headers=headers)

    file_pub = open('public_univ_niche.html', 'w')
    file_pvt = open('private_univ_niche.html', 'w')

    file_pub.write(url.text.encode('utf-8', 'ignore'))
    file_pvt.write(url1.text.encode('utf-8', 'ignore'))

    doc = parse('public_univ_niche.html').getroot()
    doc.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)
    college_link = []

    for data in doc.cssselect('div.name a'):
        college_link.append(data.get('href'))

    for i, val in enumerate(college_link):

        file_college = open('public_univ_niche_colleges_data.html', 'w')
        url_col = requests.get(url=val, headers=headers)
        file_college.write(url_col.text.encode('utf-8', 'ignore'))

        doc1 = parse('public_univ_niche_colleges_data.html').getroot()
        doc1.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)

        overall_val = ""
        college_act_name = ""

        for data in doc1.cssselect('h1 a'):
            college_act_name = data.text_content()
            break

        for div in doc1.cssselect('li.grade a'):
            main_grade_class = div[0].get('class')
            main_grade_arr = main_grade_class.split(' ')
            main_grade = main_grade_arr[2].split('-')
            overall_val = (str(round(float(main_grade[1]) / 100, 2)))
            break

        query = "insert into pub_college_overall_rank(college_name, overall_grade) values(%s,%s)"
        cursor.execute(query, (college_act_name, overall_val))

    doc = parse('private_univ_niche.html').getroot()
    doc.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)
    college_link1 = []

    for data in doc.cssselect('div.name a'):
        college_link1.append(data.get('href'))

    for j, val1 in enumerate(college_link1):

        file_college = open('private_univ_niche_colleges_data.html', 'w')
        url_col = requests.get(url=val1, headers=headers)
        file_college.write(url_col.text.encode('utf-8', 'ignore'))

        doc1 = parse('private_univ_niche_colleges_data.html').getroot()
        doc1.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)

        overall_val = ""
        college_act_name = ""

        for data in doc1.cssselect('h1 a'):
            college_act_name = data.text_content()
            break

        for div in doc1.cssselect('li.grade a'):
            main_grade_class = div[0].get('class')
            main_grade_arr = main_grade_class.split(' ')
            main_grade = main_grade_arr[2].split('-')
            overall_val = friendly_info = (str(round(float(main_grade[1]) / 100, 2)))
            break

        query1 = "insert into pvt_college_overall_rank(college_name, overall_grade) values(%s,%s)"
        cursor.execute(query1, (college_act_name, overall_val))


except Exception, e:
    print "Can't get data : ", e
    sys.exit()
