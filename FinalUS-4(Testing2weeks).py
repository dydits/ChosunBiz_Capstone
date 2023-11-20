# 라이브러리 import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
import re

def initialize_chrome_driver():
  # Chrome 옵션 설정 : USER_AGENT는 알아서 수정
  USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15'
  chrome_options = Options()
  chrome_options.page_load_strategy = 'normal'  # 'none', 'eager', 'normal'
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument(f'user-agent={USER_AGENT}')
  # Chrome 드라이버 설정
  service = Service()
  wd = webdriver.Chrome(service=service, options=chrome_options)
  return wd

# 날짜 통합 함수
def date_util(article_date):
  try:
    # Parse the date using dateutil.parser
    article_date = parser.parse(article_date).date()
  except ValueError:
    # If parsing fails, handle the relative dates
    article_date = article_date.lower()
    time_keywords = ["h", "hrs", "hr", "m", "s", "hours","hour", "minutes", "minute", "mins", "min", "seconds", "second", "secs", "sec"]
    if any(keyword in article_date for keyword in time_keywords):
      article_date = today
    elif "days" in article_date or "day" in article_date:
      # Find the number of days and subtract from today
      number_of_days = int(''.join(filter(str.isdigit, article_date)))
      article_date = today - timedelta(days=number_of_days)
    else:
      return None
  return article_date

# 에러 메시지 작성 함수
def Error_Message(message, add_error):
    if message is not str() : message += '/'
    message += add_error
    return message

# 데이터프레임
articles = []
error_list = []
today = parser.parse('2023-11-01').date()
today_list = [parser.parse('2023-11-' + str(i)).date() for i in range(1, 18)]
start_date = datetime.strptime('2023-11-01', '%Y-%m-%d').date()
# 연방정부 + 방산업체들 + NASA
url_1 = 'https://www.state.gov/press-releases/'
url_2 = 'https://www.state.gov/department-press-briefings/'
url_3 = 'https://home.treasury.gov/news/press-releases'
url_4 = 'https://www.defense.gov/News/'
url_5 = 'https://www.army.mil/news'
url_6 = 'https://www.navy.mil/Press-Office/'
url_7 = 'https://www.af.mil/News/Category/22750/'
url_8 = 'https://www.nsa.gov/Press-Room/Press-Releases-Statements/'
url_9 = 'https://www.justice.gov/news'
url_10 = 'https://www.fbi.gov/news/press-releases'
url_11 = 'https://www.doi.gov/news'
url_12 = 'https://www.usda.gov/media/press-releases'
url_13 = 'https://www.ars.usda.gov/news-events/news-archive/'
url_14 = 'https://www.fs.usda.gov/news/releases'
url_15 = 'https://www.fas.usda.gov/newsroom/search'
url_16 = 'https://www.commerce.gov/news'
url_17 = 'https://www.dol.gov/newsroom/releases?agency=All&state=All&topic=All&year=all&page=0'
url_18 = 'https://www.hhs.gov/about/news/index.html'
url_19 = 'https://www.fda.gov/news-events/fda-newsroom/press-announcements'
url_20 = 'https://www.fda.gov/news-events/speeches-fda-officials'
url_21 = 'https://www.transportation.gov/newsroom/press-releases'
url_22 = 'https://www.transportation.gov/newsroom/speeches'
url_23 = 'https://www.energy.gov/newsroom'
url_24 = 'https://www.ed.gov/news/press-releases'
url_25 = 'https://www.ed.gov/news/speeches'
url_26 = 'https://news.va.gov/news/'
url_27 = 'https://www.dhs.gov/news-releases/press-releases'
url_28 = 'https://www.dhs.gov/news-releases/speeches'
url_29 = 'https://www.fema.gov/about/news-multimedia/press-releases'
url_30 = 'https://www.secretservice.gov/newsroom'
url_31 = 'https://www.epa.gov/newsreleases/search'
url_32 = 'https://www.lockheedmartin.com/en-us/news.html'
url_33 = 'https://boeing.mediaroom.com/news-releases-statements'
url_34 = 'https://www.rtx.com/news'
url_35 = 'https://news.northropgrumman.com/news/releases'
url_36 = 'https://www.gd.com/news/news-feed?page=0'
url_37 = 'https://www.baesystems.com/en/newsroom'
url_38 = 'https://www.l3harris.com/ko-kr/newsroom/search?size=n_10_n&sort-field%5Bname%5D=Publish%20Date&sort-field%5Bvalue%5D=created_date&sort-field%5Bdirection%5D=desc&sort-direction='
url_39 = 'https://investor.textron.com/news/news-releases/default.aspx'
url_40 = 'https://www.nasa.gov/news/all-news/'

# Georgia
url_41 = 'https://sos.ga.gov/news/division/31?page=0'
url_42 = 'https://gov.georgia.gov/press-releases'
url_43 = 'https://dol.georgia.gov/latest-news'
url_44 = 'https://www.georgia.org/press-releases'
url_45 = 'https://www.gachamber.com/all-news/'

# California
url_46 = 'https://www.sos.ca.gov/administration/news-releases-and-advisories/2023-news-releases-and-advisories'
url_47 = 'https://www.gov.ca.gov/newsroom/'
url_48 = 'https://business.ca.gov/newsroom/'
url_49 = 'https://business.ca.gov/calosba-latest-news/'
url_50 = 'https://www.dir.ca.gov/dlse/DLSE_whatsnew.htm'
url_51 = 'https://www.dir.ca.gov/dosh/DOSH_Archive.html'
url_52 = 'https://www.dir.ca.gov/mediaroom.html'
url_53 = 'https://news.caloes.ca.gov/'
url_54 = 'https://advocacy.calchamber.com/california-works/calchamber-members-in-the-news/'

# Texas
url_55 = 'https://gov.texas.gov/news'
url_56 = 'https://www.texasattorneygeneral.gov/news'
url_57 = 'https://www.txdot.gov/about/newsroom/statewide.html'
url_58 = 'https://www.dps.texas.gov/news'
url_59 = 'https://www.twc.texas.gov/news'
url_60 = 'https://tpwd.texas.gov/newsmedia/releases/'
url_61 = 'https://comptroller.texas.gov/about/media-center/news//'
url_62 = 'https://www.tdi.texas.gov/index.html'
url_63 = 'https://www.txbiz.org/chamber-news'
url_64 = 'https://www.txbiz.org/press-releases'

# New York
url_65 = 'https://www.governor.ny.gov/news'
url_66 = 'https://www.ny.gov/'
url_67 = 'https://www.dot.ny.gov/news/press-releases/2023'
url_68 = 'https://ag.ny.gov/press-releases'
url_69 = 'https://www.dfs.ny.gov/'
url_70 = 'https://www.tax.ny.gov/'
url_71 = 'https://chamber.nyc/news'
url_72 = 'https://aging.ny.gov/'
url_73 = 'https://www.nyserda.ny.gov/'

# New Jersey
url_74 = 'https://www.njchamber.com/press-releases'
url_75 = 'https://www.nj.gov/health/news/'
url_76 = 'https://www.nj.gov/mvc/news/news.htm'

# North Carolina
url_77 = 'https://sosnc.gov/news_events/press_releases'
url_78 = 'https://www.commerce.nc.gov/news/press-releases'
url_79 = 'https://www.commerce.nc.gov/news/feed'
url_80 = 'https://www.ncdor.gov/news/press-releases'
url_81 = 'https://www.iprcenter.gov/news'
url_82 = 'https://edpnc.com/news-events/'
url_83 = 'https://ncchamber.com/category/chamber-updates/'

# 워싱턴 dc
url_84 = 'https://dc.gov/newsroom'
url_85 = 'https://dcchamber.org/posts/'
url_86 = 'https://planning.dc.gov/newsroom'
url_87 = 'https://dpw.dc.gov/newsroom'

# Virginia
url_88 = 'https://www.governor.virginia.gov/newsroom/news-releases/'
url_89 = 'https://www.vedp.org/press-releases'
url_90 = 'https://www.doli.virginia.gov/category/announcements/'
url_91 = 'https://vachamber.com/category/press-releases/'

# Maryland
url_92 = 'https://governor.maryland.gov/news/press/Pages/default.aspx?page=1'
url_93 = 'https://news.maryland.gov/mde/category/press-release/'
url_94 = 'https://commerce.maryland.gov/media/press-room'
url_95 = 'https://www.dllr.state.md.us/whatsnews/'
url_96 = 'https://www.mdchamber.org/news/'

urls = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12, url_13, url_14, url_15, url_16, url_17, url_18, url_19, url_20,
        url_21, url_22, url_23, url_24, url_25, url_26, url_27, url_28, url_29, url_30, url_31, url_32, url_33, url_34, url_35, url_36, url_37, url_38, url_39, url_40,
        url_41, url_42, url_44, url_45, url_46, url_47, url_48, url_49, url_50, url_51, url_52, url_53, url_54, url_55, url_56, url_57, url_58, url_59, url_60,
        url_61, url_62, url_63, url_64, url_65, url_67, url_68, url_71, url_74, url_75, url_76, url_78, url_80,
        url_81, url_82, url_83, url_84, url_86, url_87, url_88, url_89, url_90, url_91, url_92, url_93, url_94, url_95, url_96]

########################################### <1> ##############################################
# url_1 = 'https://www.state.gov/press-releases/'
wd = initialize_chrome_driver()
wd.get(url_1)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
for page_num in range(1, 20):  # 20 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    if page_num == 1:
        url = url_1
    else:
        url = f'{url_1}/page/{page_num}/'
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_items = soup.find_all('li', class_='collection-result')
        if not news_items:
            error_list.append({
                'Error Link': url_1,
                'Error': "None News"
                })
        for item in news_items:
            title = item.find('a', class_='collection-result__link').text.strip()
            if not title: error_message = Error_Message(error_message, "None Title")
            link = item.find('a', class_='collection-result__link')['href']
            if not link: error_message = Error_Message(error_message, "None Link")
            wd.get(link)  # 기사 링크로 이동
            time.sleep(5)
            article_html = wd.page_source
            news_soup = BeautifulSoup(article_html, 'html.parser')
            date_tag = news_soup.find('p', class_='article-meta__publish-date')
            if date_tag:
                date_string = date_tag.text.strip()
                news_date = parser.parse(date_string).date()
                if news_date >= today:
                    paragraphs = news_soup.find_all('p')
                    content_list = [p.text for p in paragraphs if p]
                    content = '\n'.join(content_list)
                    if error_message is not str():
                        error_list.append({
                            'Error Link': link,
                            'Error': error_message
                                })
                    else : 
                        articles.append({
                            'Title': title,
                            'Link': link,
                            'Content(RAW)': content
                        })
    except Exception as e:
        error_list.append({
            'Error Link': url_1,
            'Error': str(e)
        })
########################################### <2> ##############################################
# url_2 = 'https://www.state.gov/department-press-briefings/'
wd = initialize_chrome_driver()
wd.get(url_1)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
for page_num in range(1, 5):  
    if page_num == 1:
        url = url_2
    else:
        url = f'{url_2}/page/{page_num}/'
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_items = soup.find_all('li', class_='collection-result')
        if not news_items:
            error_list.append({
                'Error Link': url_2,
                'Error': "None News"
                })
        for item in news_items:
            title = item.find('a', class_='collection-result__link').text.strip()
            if not title: error_message = Error_Message(error_message, "None Title")
            link = item.find('a', class_='collection-result__link')['href']
            if not link: error_message = Error_Message(error_message, "None Link")
            wd.get(link)  # 기사 링크로 이동
            time.sleep(5)
            article_html = wd.page_source
            news_soup = BeautifulSoup(article_html, 'html.parser')
            date_tag = news_soup.find('p', class_='article-meta__publish-date')
            if date_tag:
                date_string = date_tag.text.strip()
                news_date = parser.parse(date_string).date()
                if news_date in today_list:
                    paragraphs = news_soup.find_all('p')
                    content = '\n'.join(p.text for p in paragraphs if p)
                    if error_message is not str():
                        error_list.append({
                            'Error Link': link,
                            'Error': error_message
                        })
                    else : articles.append({
                        'Title': title,
                        'Link': link,
                        'Content(RAW)': content
                    })
    except Exception as e:
        error_list.append({
            'Error Link': url_2,
            'Error': str(e)
        })
########################################### <3> ##############################################
# url_3 = 'https://home.treasury.gov/news/press-releases'
wd = initialize_chrome_driver()
wd.get(url_3)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
for page_num in range(0, 6):  # 6 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    url = f'{url_3}?page={page_num}' if page_num > 0 else url_3
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    error_message = str()
    try:
        news_items = soup.find_all('h3', class_='featured-stories__headline')
        if not news_items:
            error_list.append({
                'Error Link': url_3,
                'Error': "None News"
            })
        for item in news_items:
            error_message = ''
            link_tag = item.find('a')
            if not link_tag: error_message = Error_Message(error_message, "None Link")
            else: 
                title = link_tag.text.strip()
                if not title: error_message = Error_Message(error_message, "None Title")
                link = "https://home.treasury.gov" + link_tag['href']
                if not link:error_message = Error_Message(error_message, "None Link")
                date_tag = link_tag.find_parent().find_parent().find('time', class_='datetime')
                if not date_tag:error_message = Error_Message(error_message, "None Date")
                else:
                    date_str = parser.parse(date_tag.text.strip()).date()
                    wd = initialize_chrome_driver()
                    wd.get(link)  # 기사 링크로 이동
                    time.sleep(5)
                    article_html = wd.page_source
                    news_soup = BeautifulSoup(article_html, 'html.parser')
                    if date_str in today_list:
                        content_tag = news_soup.find('div', class_='clearfix text-formatted field field—name-field-news-body field—type-text-long field—label-hidden field__item')
                        if content_tag:
                            content = content_tag.get_text(strip=True)
                        if error_message is not str():
                            error_list.append({
                            'Error Link': link,
                            'Error': error_message
                            })
                        else:
                            articles.append({
                                'Title': title,
                                'Link': link,
                                'Content(RAW)': content
                            })
    except Exception as e:
            error_list.append({
                'Error Link': url_3,
                'Error': str(e)
            })
########################################### <5> ##############################################
# url_5 = 'https://www.army.mil/news'
wd = initialize_chrome_driver()
wd.get(url_5)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try:
    # 뉴스 아이템 가져오기
    news_items = soup.find_all('div', class_='news-item')
    if not news_items:
        error_list.append({
            'Error Link': url_5,
            'Error': "None News"
        })
    else:
        for item in news_items:
            link_tag = item.find('a')
            if link_tag:
                title_tag = item.find('p', class_='title').find('a')
                title = title_tag.get_text().strip()
                if not title: error_message = Error_Message(error_message, "None Title")
                # 링크 구성
                article_link = link_tag['href']
                link = f"https://www.army.mil{article_link}" if not article_link.startswith('http') else article_link
                if not link: error_message = Error_Message(error_message, "None Link")
                # 해당 기사 페이지로 이동
                wd = initialize_chrome_driver()
                wd.get(link)
                article_html = wd.page_source
                article_soup = BeautifulSoup(article_html, 'html.parser')
                # 날짜 추출
                date_span = article_soup.select_one('p.small span')
                if not date_span: error_message = Error_Message(error_message, "None Date")
                if date_span:
                    article_date = datetime.strptime(date_span.text.strip(), '%B %d, %Y').date()
                    if article_date >= today:  # 시작 날짜 이후의 기사만 추출
                        content = ' '.join(p.text.strip() for p in article_soup.find_all('p'))
                        if error_message is not str():
                            error_list.append({
                                'Error Link': link,
                                'Error': error_message
                                })
                        else:
                            articles.append({
                                'Title': title,
                                'Link': link,
                                'Content(RAW)': content
                                })
except Exception as e:
    error_list.append({
        'Error Link': url_5,
        'Error': str(e)
    })
########################################### <6> ##############################################
# url_6 = 'https://www.navy.mil/Press-Office/'
wd = initialize_chrome_driver()
wd.get(url_6)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
news_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  news_blocks = soup.find_all('div', class_='col-12 col-sm-8')
  if not news_blocks: error_list.append({'Error Link': url_6, 'Error': "None News"})
  else:
    for article in news_blocks:
      date_str = article.find('h6').text
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = article.find('h2').find('a')['href']
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1', class_='maintitle press-briefing__title').get_text().strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div', class_=['press-briefing-columns','acontent-container']).text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_6,
      'Error': str(e)
      })
########################################### <7> ##############################################
# url_7 = 'https://www.af.mil/News/Category/22750/'
wd = initialize_chrome_driver()
wd.get(url_7)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try :
  #뉴스 아이템 가져오기
  news_items = soup.find_all('article', class_='article-listing-item')
  if not news_items:
    error_list.append({
        'Error Link': url_7,
        'Error': "None News"
        })
  else :
    for item in news_items :
      title_tag = item.find('h1')
      if title_tag and title_tag.find('a'):
        title = title_tag.get_text().strip()
        if not title: error_message = Error_Message(error_message, "None Title")
      link_tag = title_tag.find('a')
      link = link_tag['href'].strip() if link_tag else None
      if not link: error_message = Error_Message(error_message, "None Link")
      date_tag = item.find('time')
      if date_tag:
        date_string = date_tag.text.strip()
        article_date = date_util(date_string)
        if article_date >= today:
          wd = initialize_chrome_driver()
          wd.get(link)
          time.sleep(5)
          article_html = wd.page_source
          article_soup = BeautifulSoup(article_html, 'html.parser')
          paragraphs = article_soup.find_all('p')
          if not paragraphs: error_message = Error_Message(error_message, "None Contents")
          content = ' '.join(paragraph.get_text().strip() for paragraph in paragraphs)
          if error_message is not str():
                    error_list.append({
                        'Error Link': link,
                        'Error': error_message
                        })
          else:
                    articles.append({
                        'Title': title,
                        'Link': link,
                        'Content(RAW)': content
                        })
except Exception as e:
    error_list.append({
        'Error Link': url_7,
        'Error': str(e)
    })
########################################### <8> ##############################################
url_8 = 'https://www.nsa.gov/Press-Room/Press-Releases-Statements/'
wd = initialize_chrome_driver()
wd.get(url_8)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try:
    # 뉴스 아이템 가져오기
    news_items = soup.find_all('div', class_='item')
    if not news_items:
      error_list.append({
          'Error Link': url_8,
          'Error': "None News"
          })
    else :
      for item in news_items :
        title_tag = item.find('div', class_='title').find('a')
        title = title_tag.text.strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        link = title_tag['href'].strip()
        if not link: error_message = Error_Message(error_message, "None Link")
        date_tag = item.find('span', class_='date')
        if date_tag:
          date_string = date_tag.text.strip()
          article_date = date_util(date_string)
          if article_date >= today:
              wd = initialize_chrome_driver()
              wd.get(link)
              time.sleep(5)
              article_html = wd.page_source
              article_soup = BeautifulSoup(article_html, 'html.parser')
              article_body = article_soup.find('div', itemprop='articleBody')
              content = ''
              if article_body:
                # 'articleBody' div 내에서 텍스트만 추출 (HTML 구조를 무시하고 텍스트만 가져옴)
                content = article_body.get_text(strip=True, separator=' ')
              else: error_message = Error_Message(error_message, "None Contents")
              if error_message is not str():
                  error_list.append({
                      'Error Link' : link,
                      'Error': error_message
                      })
              else :
                  articles.append({
                      'Title': title,
                      'Link': link,
                      'Content(RAW)': content
                      })
except Exception as e:
    error_list.append({
        'Error Link': url_8,
        'Error': str(e)
    })
########################################### <9> ##############################################
# url_9 = 'https://www.justice.gov/news' 
wd = initialize_chrome_driver()
wd.get(url_9)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
for page_num in range(0, 10):  # 10 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    url = f'{url_9}?page={page_num}' if page_num > 0 else url_9
    
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_items = soup.find_all('article', class_='news-content-listing')
        if not news_items:
            error_list.append({
                'Error Link': url_9,
                'Error': "None News"
            })
        else :
            for item in news_items :
                title_tag = item.find('h2', class_='news-title')
                if title_tag and title_tag.find('a'):
                    title = title_tag.get_text().strip()
                    if not title: error_message = Error_Message(error_message, "None Title")
                link_tag = title_tag.find('a')
                if link_tag:
                    relative_link = link_tag['href']
                    # 상대 링크를 절대 링크로 변환
                    base_url = url_9.rsplit('/', 1)[0]  # 'https://www.justice.gov'를 얻기 위해 /news 제거
                    full_link = base_url + relative_link
                date_tag = item.find('time')
                if date_tag :
                    date_string = date_tag.text.strip()
                    article_date = date_util(date_string)
                    if article_date >= today:
                        wd = initialize_chrome_driver()
                        wd.get(full_link)
                        time.sleep(5)
                        article_html = wd.page_source
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        article_body = article_soup.find('div', class_='node-body')
                        content = ''
                        if article_body: paragraphs = article_soup.find_all('p')
                        content = ' '.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
                        if error_message is not str():
                                  error_list.append({
                                      'Error Link': full_link,
                                      'Error': error_message
                                      })
                        else:
                                  articles.append({
                                    'Title': title,
                                    'Link': full_link,
                                    'Content(RAW)': content
                                    })
    except Exception as e:
        error_list.append({
            'Error Link': url_9,
            'Error': str(e)
        })
########################################### <11> ##############################################
# url_11 = 'https://www.doi.gov/news'
wd = initialize_chrome_driver()
wd.get(url_11)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('div', class_='publication-date')
  if not date_blocks: error_list.append({'Error Link': url_11, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent()['href']
        if article_link[0] =='/': article_link = 'https://www.doi.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1',class_='section-page-title').text.strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        body = article_soup.find('div',class_='field field--name-body field--type-text-with-summary field--label-hidden').text.strip()
        for i in range(len(body)): bodys += body[i]
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_11,
      'Error': str(e)
      })
########################################### <12> ##############################################
url_12 = 'https://www.usda.gov/media/press-releases'
wd = initialize_chrome_driver()
wd.get(url_12)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
news_blocks, article_date, article_link, title, bodys = None, None, None, None, None
for page_num in range(0, 10):  # 10 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    url = f'{url_12}?page={page_num}' if page_num > 0 else url_12
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_blocks = soup.find_all('li', class_='news-releases-item')
        if not news_blocks: error_list.append({'Error Link': url_12, 'Error': "None News"})
            
        else:
            for block in news_blocks:
                date_str = block.find('div',class_='news-release-date').text.strip()
                article_date = date_util(date_str)
                article_link, title, bodys = None, None, None
                if article_date >= today:
                    article_link = block.find('a')['href']
                    if article_link[0] =='/': article_link = 'https://www.usda.gov' + article_link
                    if not article_link: error_message = Error_Message(error_message, "None Link")
                    wd = initialize_chrome_driver()
                    wd.get(article_link)
                    time.sleep(5)
                    article_html = wd.page_source
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    title = article_soup.find('h1',class_='usda-page-title').text.strip()
                    if not title: error_message = Error_Message(error_message, "None Title")
                    # 기사 본문을 찾습니다.
                    body = [] ; bodys = str()
                    body = article_soup.find('div',id='block-usda-content').find_all('div')
                    for i in range(2,len(body)): bodys += body[i].text.strip()
                    if not bodys: error_message = Error_Message(error_message, "None Contents")
                    if error_message is not str():
                        error_list.append({
                            'Error Link': article_link,
                            'Error': error_message
                        })
                    else:
                        articles.append({
                            'Title': title,
                            'Link': article_link,
                            'Content(RAW)': bodys
                        })
    except Exception as e:
      error_list.append({
          'Error Link': url_12,
          'Error': str(e)
          })
########################################### <13> ##############################################
# url_13 = 'https://www.ars.usda.gov/news-events/news-archive/'
wd = initialize_chrome_driver()
wd.get(url_13)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
base_url = 'https://www.ars.usda.gov'
try:
    # 뉴스 아이템 가져오기
    news_items = soup.find_all('tr', valign='TOP')
    if not news_items:
        error_list.append({
            'Error Link': url_13,
            'Error': "None News"
        })
    else:
        for item in news_items:
            error_message = ''
            # 날짜 정보 가져오기
            date_tag = item.find('td', class_='ars-tablecell-space')
            if date_tag:
                # 기존에는 텍스트 그대로를 사용했지만, 날짜로 변환하는 과정 추가
                date_text = date_tag.text.strip()
                article_date = date_util(date_text)
                # 제목과 링크 정보 가져오기
                title_link = item.find('a', id=lambda x: x and x.startswith('anch_'))
                if title_link:
                    title = title_link.text.strip()
                    relative_link = title_link['href']
                    if relative_link.startswith('/'):
                        full_link = base_url + relative_link
                    else:
                        full_link = base_url + '/' + relative_link
                    if not title:
                        error_message = Error_Message(error_message, "None Title")
                    if not full_link:
                        error_message = Error_Message(error_message, "None Link")

                    if article_date >= today:
                        # 기사 페이지의 브라우저 인스턴스 초기화
                        wd_article = initialize_chrome_driver()
                        wd_article.get(full_link)
                        time.sleep(5)
                        article_html = wd_article.page_source
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        paragraphs = article_soup.find_all('p')
                        content = '\n'.join([p.text for p in paragraphs if p])
                        if not paragraphs:
                            error_message = Error_Message(error_message, "None Contents")

                        wd_article.quit()  # 기사 페이지의 브라우저 인스턴스 종료

                        if error_message is not str():
                            error_list.append({
                                'Error Link': full_link,
                                'Error': error_message
                            })
                        else:
                            articles.append({
                                'Title': title,
                                'Link': full_link,
                                'Content(RAW)': content
                            })
except Exception as e:
    error_list.append({
        'Error Link': url_13,
        'Error': str(e)
    })
########################################### <14> ##############################################
# url_14 = 'https://www.fs.usda.gov/news/releases'
wd = initialize_chrome_driver()
wd.get(url_14)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try:
     news_items = soup.find_all('div', class_='margin-bottom-2 views-row')
     if not news_items:
         error_list.append({
             'Error Link': url_14,
             'Error': "None News"
         })
     else:
         for item in news_items:
             date_tag = item.find('time', class_='text-base-darker')
             date_str = date_tag.get_text(strip=True)
             article_date = date_util(date_str)
             if not article_date:
                 error_message = Error_Message(error_message, "None Date")
             if article_date >= today:
                 title_tag = item.find('span', class_='field-content featured-title')
                 title = title_tag.get_text(strip=True)
                 if not title:
                     error_message = Error_Message(error_message, "None Title")
                 article_link = f"https://www.fs.usda.gov{item.a['href']}"
                 if not article_link:
                     error_message = Error_Message(error_message, "None Link")
                 wd = initialize_chrome_driver()
                 wd.get(article_link)
                 article_html = wd.page_source
                 article_soup = BeautifulSoup(article_html, 'html.parser')
                 content_div = article_soup.find('div', class_='usa-prose full-width')
                 article_body = ' '.join(p.get_text() for p in content_div.find_all('p')) #if content_div else "No content available."
                 if not article_body:
                     error_message = Error_Message(error_message, "None Contents")
                 if error_message != "":
                     error_list.append({
                         'Error Link': article_link,
                         'Error': error_message
                     })
                 else:
                     articles.append({
                         'Title': title,
                         'Link': article_link,
                         'Content(RAW)': article_body
                     })
except Exception as e:
     error_list.append({
         'Error Link': url_14,
         'Error': str(e)
     })
########################################### <15> ##############################################
# url_15 = 'https://www.fas.usda.gov/newsroom/search'
wd = initialize_chrome_driver()
wd.get(url_15)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
base_url = 'https://fas.usda.gov'
try:
    # 뉴스 아이템 가져오기
    news_items = soup.find_all('div', class_='card__header')
    if not news_items:
        error_list.append({
            'Error Link': url_15,
            'Error': "None News"
        })
    else:
        for item in news_items:
            error_message = ''
            link_tag = item.find('a', class_='card__url')
            if link_tag:
                title = link_tag.text.strip()
                if not title:
                    error_message = Error_Message(error_message, "None Title")
                relative_link = link_tag['href']
                full_link = base_url + relative_link
                if not full_link:
                    error_message = Error_Message(error_message, "None Link")
                date_tag = item.find('time')
                if date_tag:
                    date_time_str = date_tag['datetime']
                    date_str = date_time_str.split('T')[0]
                    article_date = date_util(date_str)
                    if article_date >= today:
                        wd = initialize_chrome_driver()
                        wd.get(full_link)
                        time.sleep(5)
                        article_html = wd.page_source
                        article_soup = BeautifulSoup(article_html, 'html.parser')
                        article_body = article_soup.find('div', class_='l-story__body-inner')
                        paragraphs = [p.get_text() for p in article_body.find_all('p') if p.get_text().strip() != '']
                        content_text = ' '.join(paragraphs)
                        if not content_text:
                            error_message = Error_Message(error_message, "None Content")
                        if error_message is not str():
                            error_list.append({
                                'Error Link': full_link,
                                'Error': error_message
                            })
                        else:
                            articles.append({
                                'Title': title,
                                'Link': full_link,
                                'Content(RAW)': content_text
                            })
except Exception as e:
    error_list.append({
        'Error Link': url_15,
        'Error': str(e)
    })
########################################### <17> ##############################################
url_17 = 'https://www.dol.gov/newsroom/releases?agency=All&state=All&topic=All&year=all&page=0'
base_url = 'https://www.dol.gov/newsroom/releases'
wd = initialize_chrome_driver()
wd.get(url_17)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
for page_num in range(0, 10):  # 10 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    url = f"{base_url}?agency=All&state=All&topic=All&year=all&page={page_num}"
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        date_blocks = soup.find_all('p', class_='dol-date-text')
        if not date_blocks: error_list.append({'Error Link': url_17, 'Error': "Date Blocks"})
        for block in date_blocks:
            date_str = block.text.strip()
            article_date = date_util(date_str)
            article_link, title, bodys = None, None, None
            if article_date >= today:  # 시작 날짜 이후의 기사만 추출
                article_link = block.find_parent().find('a')['href']
                if article_link[0] == ' ':
                    article_link = ('https://www.dol.gov' + article_link[4:]).strip()
                if article_link.endswith('s'):
                    article_link = article_link[:-1]
                if not article_link: error_message = Error_Message(error_message, "None Link")
                wd = initialize_chrome_driver()
                wd.get(article_link)
                time.sleep(5)
                article_html = wd.page_source
                article_soup = BeautifulSoup(article_html, 'html.parser')
                if article_html == '<html><head></head><body></body></html>': 
                    title = block.find_parent().find('h3').text.strip()
                    bodys = 'pdf File'
                else : 
                    title = article_soup.find('div',class_='field field--name-field-press-header field--type-string field--label-hidden clearfix').text.strip()
                    if not title: error_message = Error_Message(error_message, "None Title")
                    body = [] ; bodys = str()
                    bodys = article_soup.find('div',class_='field field--name-field-press-body field--type-text-with-summary field--label-hidden clearfix').text.strip()
                    if not bodys: error_message = Error_Message(error_message, "None Contents")
                if error_message is not str():
                    error_list.append({
                        'Error Link': article_link,
                        'Error': error_message
                    })
                else : 
                    articles.append({
                        'Title': title,
                        'Link': article_link,
                        'Content(RAW)': bodys
                    })
    except Exception as e:
        error_list.append({
            'Error Link': url_17,
            'Error': str(e)
        })
########################################### <18> ##############################################
# url_18 = 'https://www.hhs.gov/about/news/index.html'
wd = initialize_chrome_driver()
wd.get(url_18)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
for page_num in range(0, 10):  # 10 페이지까지 순회
    url = f"{url_18}?page={page_num}" if page_num > 0 else url_18
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        date_blocks = soup.find_all('time')
        if not date_blocks: error_list.append({'Error Link': url_18, 'Error': "Date Blocks"})
        for block in date_blocks:
            date_str = block.text.strip()
            article_date = parser.parse(date_str).date()
            article_link, title, bodys = None, None, None
            if article_date >= today:  # 시작 날짜 이후의 기사만 추출
                article_link = block.find_parent().find_parent().find_parent().find('a')['href']
                if article_link[0] == '/':
                    article_link = 'https://www.hhs.gov' + article_link
                if not article_link: error_message = Error_Message(error_message, "None Link")
                wd = initialize_chrome_driver()
                wd.get(article_link)
                time.sleep(5)
                article_html = wd.page_source
                article_soup = BeautifulSoup(article_html, 'html.parser')
                title = article_soup.find('h1').text
                if not title: error_message = Error_Message(error_message, "None Title")
                content = article_soup.find('div', class_='field__item usa-prose').text.strip()
                if not content : error_message = Error_Message(error_message, "None Contents")
                if error_message is not str():
                    error_list.append({
                        'Error Link': article_link,
                        'Error': error_message
                    })
                else : 
                    articles.append({
                        'Title': title,
                        'Link': article_link,
                        'Content(RAW)': content
                    })
    except Exception as e:
        error_list.append({
            'Error Link': url,
            'Error': str(e)
        })
########################################### <19> ##############################################
url_19 = 'https://www.fda.gov/news-events/fda-newsroom/press-announcements'
wd = initialize_chrome_driver()
wd.get(url_19)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('time')
  if not date_blocks: error_list.append({'Error Link': url_19, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      if block.find_parent().get('class') == None:
        date_str = block.text.strip()
        article_date = date_util(date_str)
        article_link, title, bodys = None, None, None
        if article_date >= today:
          article_link = block.find_parent().find_parent().find('a')['href']
          if article_link[0] =='/': article_link = 'https://www.fda.gov' + article_link
          if not article_link: error_message = Error_Message(error_message, "None Link")
          wd = initialize_chrome_driver()
          wd.get(article_link)
          time.sleep(5)
          article_html = wd.page_source
          article_soup = BeautifulSoup(article_html, 'html.parser')
          title = article_soup.find('h1', class_='content-title text-center').text
          if not title: error_message = Error_Message(error_message, "None Title")
          # 기사 본문을 찾습니다.
          body = [] ; bodys = str()
          body = article_soup.find('div', class_='col-md-8 col-md-push-2').find_all('p')
          for i in body: bodys += i.get_text().strip()
          if not bodys: error_message = Error_Message(error_message, "None Contents")
          if error_message is not str():
            error_list.append({
              'Error Link': article_link,
              'Error': error_message
            })
          else:
            articles.append({
              'Title': title,
              'Link': article_link,
              'Content(RAW)': bodys
            })
except Exception as e:
  error_list.append({
      'Error Link': url_19,
      'Error': str(e)
      })
########################################### <20> ##############################################
# url_20 = 'https://www.fda.gov/news-events/speeches-fda-officials'
wd = initialize_chrome_driver()
wd.get(url_20)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('time')
  if not date_blocks: error_list.append({'Error Link': url_20, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.fda.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('div', class_='field--item').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div', class_='col-md-8 col-md-push-2').get_text().strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        # 기사만 추출
        start_delimiter = "\n\n\n\n\n\n"
        end_delimiter = "Related Information"
        start_index = bodys.find(start_delimiter) + len(start_delimiter)
        end_index = bodys.find(end_delimiter)
        extracted_article = bodys[start_index:end_index].strip()
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': extracted_article
          })
except Exception as e:
  error_list.append({
      'Error Link': url_20,
      'Error': str(e)
      })
########################################### <21> ##############################################
# url_21 = 'https://www.transportation.gov/newsroom/press-releases'
wd = initialize_chrome_driver()
wd.get(url_21)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('time', class_='datetime')
  if not date_blocks: error_list.append({'Error Link': url_21, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.transportation.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('span', class_='field field--name-title field--type-string field--label-hidden').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div', class_='mb-4 clearfix').get_text().strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_21,
      'Error': str(e)
      })
########################################### <22> ##############################################
# url_22 = 'https://www.transportation.gov/newsroom/speeches'
wd = initialize_chrome_driver()
wd.get(url_22)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('td', class_='views-field views-field-field-effective-date')
  if not date_blocks: error_list.append({'Error Link': url_22, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.transportation.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('span', class_='field field--name-title field--type-string field--label-hidden').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div', class_='mb-4 clearfix').get_text().strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_22,
      'Error': str(e)
      })
########################################### <23> ##############################################
# url_23 = 'https://www.energy.gov/newsroom'
wd = initialize_chrome_driver()
wd.get(url_23)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('div', class_='search-result-display-date')
  if not date_blocks: error_list.append({'Error Link': url_23, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.find('p').text
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find('a', class_="search-result-title")['href']
        if article_link[0] =='/': article_link = 'https://www.energy.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1', class_='page-title').text.replace('\n','').strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div',class_='block block-system block-system-main-block').text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_23,
      'Error': str(e)
      })
########################################### <24> ##############################################
# url_24 = 'https://www.ed.gov/news/press-releases'
wd = initialize_chrome_driver()
wd.get(url_24)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('span', class_='field-content date-display-single')
  if not date_blocks: error_list.append({'Error Link': url_24, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.ed.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div',class_='field field-name-body field-type-text-with-summary field-label-hidden').text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_24,
      'Error': str(e)
      })
########################################### <25> ##############################################
# url_25 = 'https://www.ed.gov/news/speeches'
wd = initialize_chrome_driver()
wd.get(url_25)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('span', class_='field-content date-display-single')
  if not date_blocks: error_list.append({'Error Link': url_25, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.ed.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div',class_='field field-name-body field-type-text-with-summary field-label-hidden').text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_25,
      'Error': str(e)
      })
########################################### <26> ##############################################
# url_26 = 'https://news.va.gov/news/'
wd = initialize_chrome_driver()
wd.get(url_26)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
article_links, article_date, article_link, title, bodys = None, None, None, None, None
try:
  article_links = soup.find_all('a', class_='awb-custom-text-color awb-custom-text-hover-color')
  if not article_links: error_list.append({'Error Link': url_26, 'Error': "None Links"})
  else:
    links = [link.get('href') for link in article_links]
    for link in links:
      wd = initialize_chrome_driver()
      wd.get(link)
      time.sleep(5)
      article_html = wd.page_source
      article_soup = BeautifulSoup(article_html, 'html.parser')
      date_str = article_soup.find('div', class_='fusion-text fusion-text-3').find('p').text
      article_date = date_util(date_str)
      article_link = link
      title, bodys = None, None
      if article_date >= today:
        title = article_soup.find('h1', class_='fusion-title-heading title-heading-left').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        article = (article_soup.find('article',class_='fusion-layout-column fusion_builder_column fusion-builder-column-7 fusion-flex-column'))
        for tag in article.find_all(True):  # True는 모든 태그를 찾는다는 의미입니다.
            # 현재 태그의 이름을 가져옵니다.
            current_tag_name = tag.name
            if tag.name == 'p':
                body.append(tag.get_text())
        for i in range(len(body)-1): bodys += str(body[i])
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_26,
      'Error': str(e)
      })
########################################### <27> ##############################################
# url_27 = 'https://www.dhs.gov/news-releases/press-releases'
wd = initialize_chrome_driver()
wd.get(url_27)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('time')
  if not date_blocks: error_list.append({'Error Link': url_27, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.get('datetime')
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.dhs.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1', class_='uswds-page-title page-title').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div',class_='block block-system block-system-main-block').text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_27,
      'Error': str(e)
      })
########################################### <28> ##############################################
# url_28 = 'https://www.dhs.gov/news-releases/speeches'
wd = initialize_chrome_driver()
wd.get(url_28)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('time')
  if not date_blocks: error_list.append({'Error Link': url_28, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.get('datetime')
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.dhs.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1', class_='uswds-page-title page-title').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        bodys = article_soup.find('div',class_='block block-system block-system-main-block').text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_28,
      'Error': str(e)
      })
########################################### <29> ##############################################
# url_29 = 'https://www.fema.gov/about/news-multimedia/press-releases'
wd = initialize_chrome_driver()
wd.get(url_29)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
news_blocks, article_date, article_link, title, bodys = None, None, None, None, None
for page_num in range(0, 10):  # 10 페이지까지 순회 (더 많은 페이지가 필요하면 이 값을 변경)
    url = f"{url_29}?page={page_num}" if page_num > 0 else url_29
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        date_blocks = soup.find_all('div', class_='views-listing views-row')
        if not date_blocks: error_list.append({'Error Link': url_29, 'Error': "Date Blocks"})
        for block in date_blocks:
            date_str = block.find('time').text
            article_date = date_util(date_str)
            article_link, title, bodys = None, None, None
            if article_date >= today:  # 시작 날짜 이후의 기사만 추출
                article_link = block.find('a')['href']
                if article_link[0] == '/':
                    article_link = 'https://www.fema.gov' + article_link
                if not article_link: error_message = Error_Message(error_message, "None Link")
                wd = initialize_chrome_driver()
                wd.get(article_link)
                time.sleep(5)
                article_html = wd.page_source
                article_soup = BeautifulSoup(article_html, 'html.parser')
                title = article_soup.find('span', class_='field field--name-title field--type-string field--label-hidden').text
                if not title: error_message = Error_Message(error_message, "None Title")
                body = [] ; bodys = str()
                bodys = article_soup.find('div',class_='content-inner-container').text.strip()
                if not bodys: error_message = Error_Message(error_message, "None Contents")
                if error_message is not str():
                    error_list.append({
                        'Error Link': article_link,
                        'Error': error_message
                    })
                else : 
                    articles.append({
                        'Title': title,
                        'Link': article_link,
                        'Content(RAW)': bodys
                    })
    except Exception as e:
        error_list.append({
            'Error Link': url,
            'Error': str(e)
        })
########################################### <30> ##############################################
# url_30 = 'https://www.secretservice.gov/newsroom'
wd = initialize_chrome_driver()
wd.get(url_30)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('div', class_='field-content usss-news-blk-date-y')
  if not date_blocks: error_list.append({'Error Link': url_29, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      # 날짜 요소를 추출합니다.
      day = block.find('p', class_='usss-news-date-d').text
      month = block.find('p', class_='usss-news-date-m').text
      year = block.find('p', class_='usss-news-date-y').text
      # 날짜를 문자열로 합칩니다.
      date_str = f"{month} {day}, {year}"
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://www.secretservice.gov' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        # 정규 표현식 패턴을 컴파일
        pattern = re.compile("page-node-\d+ field field--name-title field--type-string field--label-hidden")
        title = article_soup.find('span', class_=pattern).text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        pattern = re.compile("page-node-\d+ block block-layout-builder block-field-blocknodepress-releasebody")
        bodys = article_soup.find('div',class_=pattern).text.strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_30,
      'Error': str(e)
      })

########################################### <35> ##############################################
# url_35 = 'https://news.northropgrumman.com/news/releases'
wd = initialize_chrome_driver()
wd.get(url_35)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('div', class_='index-item-info')
  if not date_blocks: error_list.append({'Error Link': url_35, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find('a')['href']
        if article_link[0] =='/': article_link = 'https://news.northropgrumman.com' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = article_soup.find('h1').text
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        paragraphs = article_soup.find_all('p')
        for p in paragraphs: body.append(p.get_text().strip())
        for i in range(len(body)-8): bodys += str(body[i])
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_35,
      'Error': str(e)
      })
########################################### <36> ##############################################
# url_36 = 'https://www.gd.com/news/news-feed?page=0'
wd = initialize_chrome_driver()
wd.get(url_36)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find('div', class_='news-feed-target').find_all('div', class_='news__publish-date')
  if not date_blocks: error_list.append({'Error Link': url_36, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.contents[0].strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find('a')['href']
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = block.find_parent().find('h3').text.strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        paragraphs = article_soup.find('div', class_='article-body')
        for p in paragraphs: body.append(p.get_text().strip())
        for i in range(len(body)): bodys += str(body[i]).strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_36,
      'Error': str(e)
      })
########################################### <37> ##############################################
# url_37 = 'https://www.baesystems.com/en/newsroom'
wd = initialize_chrome_driver()
wd.get(url_37)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('div', class_='cell__body')
  if not date_blocks:
    error_list.append({
            'Error Link': url_37,
            'Error': "Date Blocks"
          })
  else:
    for block in date_blocks:
      date_str = block.find_next('div',class_='searchresult-tags').text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_parent().find_parent().find_parent().find('a')['href']
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = block.find_parent().find('h3').text.strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        bodys = article_soup.find('div', class_='content-container').get_text().strip()
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_37,
      'Error': str(e)
      })
########################################### <38> ##############################################
# url_38 = 'https://www.l3harris.com/ko-kr/newsroom/search?size=n_10_n&sort-field%5Bname%5D=Publish%20Date&sort-field%5Bvalue%5D=created_date&sort-field%5Bdirection%5D=desc'
wd = initialize_chrome_driver()
wd.get(url_38)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
base_url = 'https://www.l3harris.com/ko-kr/newsroom/search'
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
for page_num in range(1, 10):  # 10 페이지까지 순회 -> 더 많은 페이지 필요하면 이 값 변경
    if page_num == 1:
        url = f'{base_url}?size=n_10_n&sort-field%5Bname%5D=Publish%20Date&sort-field%5Bvalue%5D=created_date&sort-field%5Bdirection%5D=desc'
    else:
        url = f'{base_url}?current=n_{page_num}_n&size=n_10_n&sort-field%5Bname%5D=Publish%20Date&sort-field%5Bvalue%5D=created_date&sort-field%5Bdirection%5D=desc'
    wd.get(url)
    time.sleep(5)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        date_blocks = soup.find('ul', class_='search-results-page__result-list').find_all('p', class_='d-block mb-4 mb-lg-8 subtitle')
        if not date_blocks: error_list.append({'Error Link': url_38, 'Error': "Date Blocks"})
        else:
            for block in date_blocks:
                date_str = block.get_text().split('|')[1].strip()
                article_date = parser.parse(date_str).date()
                if article_date >= today:  # 시작 날짜 이후의 기사만 추출
                    article_link = block.find_parent().find_parent().find_parent().find('a')['href']
                    if not article_link: error_message = Error_Message(error_message, "None Link")
                    wd.get(article_link)
                    time.sleep(5)
                    article_html = wd.page_source
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    title = block.find_parent().find('p', class_='result-item__link font-600 d-block mb-4 mb-lg-8').text.strip()
                    if not title: error_message = Error_Message(error_message, "None Title")
                    body = [] ; bodys = str()
                    body = [p.get_text().strip() for p in article_soup.find_all('div', class_='text-long')]
                    for p in paragraphs: body.append(p.get_text().strip())
                    for i in range(len(body)): bodys += str(body[i]).strip()
                    if not bodys: error_message = Error_Message(error_message, "None Contents")
                    if error_message is not str():
                        error_list.append({
                            'Error Link': article_link,
                            'Error': error_message
                        })
                    else: articles.append({
                        'Title': title,
                        'Link': article_link,
                        'Content(RAW)': bodys
                    })
    except Exception as e:
        error_list.append({
            'Error Link': url_38,
            'Error': str(e)
        })
########################################### <39> ##############################################
# url_39 = 'https://investor.textron.com/news/news-releases/default.aspx'
wd = initialize_chrome_driver()
wd.get(url_39)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
date_blocks, article_date, article_link, title, bodys = None, None, None, None, None
try:
  date_blocks = soup.find_all('span', class_='ModuleDate')
  if not date_blocks: error_list.append({'Error Link': url_39, 'Error': "Date Blocks"})
  else:
    for block in date_blocks:
      date_str = block.text.strip()
      article_date = date_util(date_str)
      article_link, title, bodys = None, None, None
      if article_date >= today:
        article_link = block.find_next('a', class_='ModuleMoreLink')['href']
        if article_link[0] =='/': article_link = 'https://investor.textron.com' + article_link
        if not article_link: error_message = Error_Message(error_message, "None Link")
        wd = initialize_chrome_driver()
        wd.get(article_link)
        time.sleep(5)
        article_html = wd.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        title = block.find_parent().find('span', class_='ModuleHeadline').text.strip()
        if not title: error_message = Error_Message(error_message, "None Title")
        # 기사 본문을 찾습니다.
        body = [] ; bodys = str()
        paragraphs = article_soup.find('div',class_=['q4default','module_body']).find_all('p')
        for p in paragraphs: body.append(p.get_text().strip())
        for i in range(len(body)-2): bodys += str(body[i])
        if not bodys: error_message = Error_Message(error_message, "None Contents")
        if error_message is not str():
          error_list.append({
            'Error Link': article_link,
            'Error': error_message
          })
        else:
          articles.append({
            'Title': title,
            'Link': article_link,
            'Content(RAW)': bodys
          })
except Exception as e:
  error_list.append({
      'Error Link': url_39,
      'Error': str(e)
      })
########################################### <42> ##############################################
# url_42 = 'https://gov.georgia.gov/press-releases'
wd = initialize_chrome_driver()
wd.get(url_42)
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try:
     news_items = soup.select(".news-teaser")
     if not news_items:
         error_list.append({
             'Error Link': url_42,
             'Error': "None News"
         })
     else:
         for item in news_items:
             date_str = item.select_one('.global-teaser__description').get_text(strip=True)
             article_date = date_util(date_str)
             if not article_date:
                 error_message = Error_Message(error_message, "None Date")
             if article_date >= today:
                 title = item.select_one('.global-teaser__title').get_text(strip=True)
                 if not title:
                     error_message = Error_Message(error_message, "None Title")
                 article_link = f"https://gov.georgia.gov{item.a['href']}"
                 if not article_link:
                     error_message = Error_Message(error_message, "None Link")
                 wd = initialize_chrome_driver()
                 wd.get(article_link)
                 article_html = wd.page_source
                 article_soup = BeautifulSoup(article_html, 'html.parser')
                 paragraphs = article_soup.select("main.content-page__main p")
                 article_body = ' '.join(p.get_text(strip=True) for p in paragraphs)
                 if not article_body:
                     error_message = Error_Message(error_message, "None Contents")
                 if error_message != "":
                     error_list.append({
                         'Error Link': url_42,
                         'Error': error_message
                     })
                 else:
                     articles.append({
                         'Title': title,
                         'Link': article_link,
                         'Content(RAW)': article_body
                     })
except Exception as e:
     error_list.append({
         'Error Link': url_42,
         'Error': str(e)
     })
########################################### <94> ##############################################
# url_94 = 'https://commerce.maryland.gov/media/press-room'
wd = initialize_chrome_driver()
wd.get(url_94)
base_url = "https://commerce.maryland.gov"
time.sleep(5)
html = wd.page_source
soup = BeautifulSoup(html, 'html.parser')
error_message = str()
try:
    # 뉴스 아이템 가져오기
    news_item = soup.find('table', id='speakerTable')
    if not news_item:
        error_list.append({
            'Error Link': url_94,
            'Error': "None News"
        })
    else:
        for row in news_item.find_all('tr'):
            error_message = ''
            # 날짜와 제목을 추출
            date_tag = row.find('nobr')
            title_tag = row.find('a')
            if date_tag and title_tag:
                date_string = date_tag.text.strip()
                article_date = date_util(date_string)
                title = title_tag.text.strip()
                link = title_tag['href']
                full_link = base_url + link if link.startswith('/') else link
                if article_date in today_list:
                    wd = initialize_chrome_driver()
                    wd.get(full_link)
                    time.sleep(5)
                    article_html = wd.page_source
                    article_soup = BeautifulSoup(article_html, 'html.parser')
                    content = ''
                    content_blocks = article_soup.find('div', id='ctl00_PlaceHolderMain_ctl06__ControlWrapper_RichHtmlField')
                    if content_blocks:
                        # content_blocks 내의 모든 텍스트 추출
                        content = content_blocks.get_text(strip=True, separator='\n')
                    if not content:
                        error_message = Error_Message(error_message, "None Contents")
                    if error_message is not str():
                        error_list.append({
                            'Error Link': full_link,
                            'Error': error_message
                        })
                    else:
                        articles.append({
                            'Title': title,
                            'Link': full_link,
                            'Content(RAW)': content
                        })
except Exception as e:
    error_list.append({
        'Error Link': url_94,
        'Error': str(e)
    })
