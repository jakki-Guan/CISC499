from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import pandas as pd
from selenium import webdriver

delay = 100
firefox_driver_path = 'C:/Users/jakkiG/Downloads/geckodriver-v0.30.0-win64' \
                      '/geckodriver.exe '

driver = webdriver.Chrome('C:/Windows/chromedriver_win32 (1)/chromedriver.exe')
# By replaceing the 'teaching-and-academics' part of website address with
# each of the element in category list, renaming the category name in line 101
# and .to_csv function csv file name in the end, this crawler can produce 13
# datasets based on the number of elements in category list.
driver.get(
    'https://www.udemy.com/courses/teaching-and-academics/?persist_locale'
    '=&locale=en_US')
category = ['development', 'it-and-software', 'business',
            'finance-and-accounting', 'office-productivity',
            'personal-development', 'design', 'marketing', 'lifestyle',
            'photography-and-video', 'health-and-fitness', 'music',
            'teaching-and-academics']


def extract_pro_organization(aList, bList, cList):
    if len(aList) == 1:
        if ('School' in aList[0]) or ('Learn' in aList[0]) or (
                'Academy' in aList[0]):
            cList.append(aList[0])
            bList.append('NaN')
        else:
            bList.append(aList[0])
            cList.append('NaN')
    else:
        for i in range(0, len(aList)):
            if i != len(aList) - 1:
                bList.append(aList[i])
            else:
                cList.append(aList[i])


try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'course-list--container--3zXPS')))

except TimeoutException:
    print('Loading exceeds delay time')
else:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    course_list = soup.find('div',
                            {'class': 'course-list--container--3zXPS'})
    print(course_list)
    courses = course_list.findAll('div', {'class': 'popper--popper--2r2To'})
    print(courses)
    list_of_lists = []
    for course in courses:
        list_of_page = []
        head = course.find('h3', attrs={
            'udlite-heading-md course-card--course-title--vVEjC'}).get_text()
        print(head)
        course_headline = course.find('p', attrs={
            'udlite-text-sm course-card--course-headline--2DAqq'}).get_text()
        print(course_headline)
        instructors = course.find('div', attrs={
            'course-card--instructor-list--nH1OC'}).get_text()
        instructor_txt = instructors.split(", ")
        instructor_pro = []
        organization = []
        extract_pro_organization(instructor_txt, instructor_pro,
                                 organization)
        instructors_actual = ",".join(instructor_pro)
        organization_actual = ",".join(organization)
        print("instructor is", instructors_actual)
        print("organization is", organization_actual)
        rating = course.find('span', attrs={
            'udlite-heading-sm star-rating--rating-number--2o8YM'}).get_text()
        print('rating is', rating)
        num_reviews = course.find('span', attrs={
            'udlite-text-xs course-card--reviews-text--1yloi'}).get_text()
        print('num_review is ', str(num_reviews))
        difficulty = course.find_all('span', attrs={'course-card--row--29Y0w'})
        difficultyL = []
        for item in difficulty:
            difficultyL.append(item.get_text())
        print('difficulty', difficultyL[2])
        links = 'https://www.udemy.com'
    # course_url=course.find('a',attrs={'course-card--row--29Y0w'}).get_text()
        for a in course.find_all('a', href=True):
            course_url = links + a['href']
        print(course_url)
        for item in soup.findAll('div', attrs={
            'class': 'price-text--price-part--2npPm '
                     'price-text--original-price--1sDdx '
                     'course-card--list-price--3RTcj udlite-text-sm'}):
            # for dt in item.findAll('span'):
            print(item.text)
        list_of_lists.append(
            [head, instructor_txt, course_headline, 'teaching-and-academics',
             difficultyL[2], num_reviews, rating, 'True', course_url])
df = pd.DataFrame(list_of_lists,
                  columns=['title', 'instructor', 'description', 'type',
                           'difficulty', 'num_reviews', 'rating', 'price',
                           'url'])
df.to_csv('Udmey teaching-and-academics Courses.csv', index=False)

driver.quit()
