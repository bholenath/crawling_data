import requests
from lxml.html import parse
import MySQLdb
import sys

cnxn = MySQLdb.connect(host="localhost", user="root", passwd="harshit@123", db="college_info", charset="utf8", use_unicode=True)
cursor = cnxn.cursor()
cnxn.autocommit(True)


def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        url = requests.get(url='https://colleges.niche.com/rankings/top-public-universities', headers=headers)
        url1 = requests.get(url='https://colleges.niche.com/rankings/top-private-universities', headers=headers)
        # url_us_news_ug = requests.get(url='http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national'
        #                                   '-universities/data', headers=headers)
        # url_us_news_g = requests.get(url='http://grad-schools.usnews.rankingsandreviews.com/best-graduate-schools/top'
        #                                  '-engineering-schools/eng-rankings?int=a74509', headers=headers)

        file_pub = open('public_univ_niche.html', 'w')
        file_pvt = open('private_univ_niche.html', 'w')
        # file_pub1 = open('public_univ_us_news.html', 'w')
        # file_pvt1 = open('private_univ_us_news.html', 'w')

        file_pub.write(url.text.encode('utf-8', 'ignore'))
        file_pvt.write(url1.text.encode('utf-8', 'ignore'))
        # file_pub1.write(url_us_news_ug.text.encode('utf-8', 'ignore'))
        # file_pvt1.write(url_us_news_g.text.encode('utf-8', 'ignore'))

        doc = parse('public_univ_niche.html').getroot()
        doc.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)
        college_link = []

        for data in doc.cssselect('div.name a'):
            college_link.append(data.get('href'))

        aspects = ['Academics', 'Administration', 'Athletics', 'Campus Food', 'Campus Housing', 'Campus Quality', 'Diversity',
                   'Drug Safety', 'Greek Life', 'Guys & Girls', 'Health & Safety', 'Local Area', 'Off-Campus Dining',
                   'Off-Campus Housing', 'Parking', 'Party Scene', 'Technology', 'Transportation', 'Weather']
        aspects_ranking = []

        for i, val in enumerate(college_link):

            file_college = open('public_univ_niche_colleges_data.html', 'w')
            url_col = requests.get(url=val, headers=headers)
            file_college.write(url_col.text.encode('utf-8', 'ignore'))

            doc1 = parse('public_univ_niche_colleges_data.html').getroot()
            doc1.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)

            for link in doc1.cssselect('li.noChildren a'):

                if link.text_content() == 'Rankings':
                    file_ranking = open('public_univ_niche_ranking_details.html', 'w')
                    url_rank = requests.get(url=link.get('href'), headers=headers)
                    file_ranking.write(url_rank.text.encode('utf-8', 'ignore'))

                    doc2 = parse('public_univ_niche_ranking_details.html').getroot()
                    doc2.make_links_absolute('https://colleges.niche.com', resolve_base_href=True)

                    college_name = ''

                    for name in doc2.cssselect('div.school-header'):
                        for link1 in name.cssselect('h1 a'):
                            college_name = link1.text_content()
                            break
                        break

                    friendly_info = '0.00'

                    for label in doc2.cssselect('li.sub-ranking'):
                        for sub_rank in label.cssselect('div.label a'):
                            sub_rank_name = sub_rank.text_content()
                            if sub_rank_name == 'Friendliest Students':
                                for result1 in label.cssselect('div.grade'):
                                    classed1 = result1[0].get('class')
                                    get_multi1 = classed1.split(' ')
                                    get_rank1 = get_multi1[2].split('-')
                                    friendly_info = (str(round(float(get_rank1[1]) / 100, 2)))
                                    break
                                break
                            break

                    details_name = []
                    name_check = ''

                    for div in doc2.cssselect('li.ranking-cat'):

                        for name1 in div.cssselect('div.label a'):
                            name_check = name1.text_content()
                            details_name.append(name_check)
                            break

                        for result in div.cssselect('div.grade'):
                            if name_check == 'Guys & Girls':
                                aspects_ranking.append(friendly_info)
                                break
                            else:
                                classed = result[0].get('class')
                                get_multi = classed.split(' ')
                                get_rank = get_multi[2].split('-')
                                aspects_ranking.append(str(round(float(get_rank[1]) / 100, 2)))
                                break

                    if len(aspects_ranking) != 19:
                        for j, val1 in enumerate(aspects):
                            if val1 in details_name:
                                continue
                            else:
                                aspects_ranking.insert(j, 0.00)

                    try:

                        query = "insert into pub_college_aspects_ranking (college_name,academics,administration,athletics,campus_food,campus_housing," \
                                "campus_quality,diversity,drug_safety,greek_life,friendliest_students,health_safety,local_area,off_campus_dining,off_campus_housing,parking,party_scene,technology," \
                                "transportation,weather)" \
                                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                        insert_data = (college_name, aspects_ranking[0], aspects_ranking[1], aspects_ranking[2],
                                       aspects_ranking[3], aspects_ranking[4], aspects_ranking[5], aspects_ranking[6],
                                       aspects_ranking[7],
                                       aspects_ranking[8], aspects_ranking[9], aspects_ranking[10], aspects_ranking[11],
                                       aspects_ranking[12], aspects_ranking[13], aspects_ranking[14],
                                       aspects_ranking[15], aspects_ranking[16], aspects_ranking[17], aspects_ranking[18])

                        cursor.execute(query, insert_data)
                        aspects_ranking[:] = []

                    except Exception as e:
                        print 'Error with insertion in Database', e
                        return False

                elif link.text_content() == 'Statistics':
                    continue
                elif link.text_content() == 'The Best & Worst':
                    continue

    except Exception as e:
        print 'Exception in reading data : ', e
        return False


if __name__ == "__main__":
    main()
