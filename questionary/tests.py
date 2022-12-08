from django.test import TestCase


# Create your tests here.

# this is not a function but bulkupload logic
import csv
from questionary.models import Questionary


def upload(text):
    hand = open(text)
    reader = csv.reader(hand)
    bulk_list = []

    for row in reader:
        bulk_list.append(Questionary(
            index = 'sprint_first',
            order = row[0],
            main_category = row[1],
            sub_category = row[2],
            questionary=row[3],
            tag=row[4]
        ))
    return bulk_list
# Questionary.objects.bulk_create(bulk_list)

def export_csv(data):
    list_set = []
    for item in data:
        sub_list = []
        sub_list.append(item.Question_number.questionary)
        sub_list.append(item.category)
        sub_list.append(item.main_category)
        sub_list.append(item.sub_category)
        sub_list.append(item.tag)
        sub_list.append(item.user)
        sub_list.append(item.able)
        sub_list.append(item.description)
        sub_list.append(item.review)
        list_set.append(sub_list)
    return list_set

def save_csv(list):
    with open('test.csv', 'w', encoding='utf-8', newline='') as f:
        write = csv.writer(f)
        # write.writerow = ['질문', '카테고리', '메인 카테고리', '서브카테고리', '태그', '작성자', '작동여부', '설명', '리뷰여부']
        write.writerows(list)