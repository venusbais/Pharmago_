from bs4 import BeautifulSoup
import requests

def master_scrapper(medicine):
  urls_to_send= link_creator(medicine)
  pharm_url = urls_to_send[0]
  app_url = urls_to_send[2]
  pharm_master_list= pharmeasy_scrapper(pharm_url)
  app_master_list= appolo_scrapper(app_url)
  full_response=[pharm_master_list, app_master_list]

  return(full_response)


def link_creator(medicine):
  medicine = medicine.lower()
  pharm_base_url_start = "https://pharmeasy.in/search/all?name="
  net_base_url_start = "https://www.netmeds.com/catalogsearch/result/"
  app_base_url_start = "https://www.apollopharmacy.in/search-medicines/"
  pharm_base_url_end = ""
  net_base_url_end = "/all"
  app_base_url_end = ""
  pharm_url_create = pharm_base_url_start + medicine + pharm_base_url_end
  net_url_create = net_base_url_start + medicine + net_base_url_end
  app_url_create = app_base_url_start + medicine + app_base_url_end
  list_of_urls = [pharm_url_create, net_url_create, app_url_create]

  return (list_of_urls)


def pharmeasy_scrapper(pharm_link):
  og_pharm = "https://pharmeasy.in"
  pharm_response = requests.get(pharm_link)
  pharm_page = pharm_response.text
  pharm_soup = BeautifulSoup(pharm_page, "html.parser")
  pharm_med_names = pharm_soup.find_all(class_="ProductCard_medicineName__8Ydfq")
  # print(pharm_med_names)
  # pharm_med_prices = pharm_soup.find_all(class_="ProductCard_gcdDiscountContainer__CCi51")
  # print(pharm_med_prices)

  discounts = []
  for elem in pharm_soup.find_all(class_='ProductCard_gcdDiscountContainer__CCi51'):
    first_span = elem.find('span')
    if first_span:
      discounts.append(first_span.text.strip())

  print(discounts)

  pharm_half_med_links = pharm_soup.find_all(name="a",
                                             class_="ProductCard_medicineUnitWrapper__eoLpy ProductCard_defaultWrapper__nxV0R")
  pharm_med_names_list = []
  pharm_med_prices_list = discounts
  pharm_half_med_links_list = []
  for i in pharm_med_names:
    med_name = i.getText()
    pharm_med_names_list.append(med_name)
  print(pharm_med_names_list)
  # for i in pharm_med_prices:
  #   med_price = i.getText()
  #   med_price = med_price[1:-1]
  #   med_price = float(med_price)
  #   pharm_med_prices_list.append(med_price)
  for i in pharm_half_med_links:
    med_link = i.get("href")
    med_link = og_pharm + med_link
    pharm_half_med_links_list.append(med_link)
  Finans_pharmeasy = sorted(zip(pharm_med_prices_list, pharm_med_names_list, pharm_half_med_links_list), reverse=False)[
                     :3]

  return (Finans_pharmeasy)


def appolo_scrapper(app_link):
  og_app = "https://www.apollopharmacy.in"
  app_response = requests.get(app_link)
  app_page = app_response.text
  app_soup = BeautifulSoup(app_page, "html.parser")
  app_med_names = app_soup.find_all(class_="ProductCard_productName__f82e9")
  # print(app_med_names)
  app_med_prices = app_soup.find_all(class_="ProductCard_priceGroup__V3kKR")
  # print(app_med_prices)
  app_half_med_links = app_soup.find_all(name="a", class_="ProductCard_proDesMain__LWq_f")
  # print(app_half_med_links)
  app_med_names_list = []
  app_med_prices_list = []
  app_half_med_links_list = []
  for i in app_med_names:
    med_name = i.getText()
    app_med_names_list.append(med_name)
  # print(app_med_names_list)
  for i in app_med_prices:
    med_price = i.getText()
    # print(med_price)
    x = med_price.split("₹")
    # print(x)
    med_price = float(x[-1])
    app_med_prices_list.append(med_price)
  # print(app_med_prices_list)
  for i in app_half_med_links:
    med_link = i.get("href")
    med_link = og_app + med_link
    app_half_med_links_list.append(med_link)
  # app_half_med_links_list
  Finans_appolo = sorted(zip(app_med_prices_list, app_med_names_list, app_half_med_links_list), reverse=False)[:3]

  return (Finans_appolo)

def response_corrector(tocorr):
  # modelresponse="paminglael"
  modelresponse = tocorr

  modelresponse = modelresponse.lower()
  base_url_start = "https://www.google.co.in/search?q="
  base_url_end = '%22medicine%22&sxsrf=ALiCzsZ1raIfRE9QvWmS_Uao7KztHTHXJw%3A1668029297476&source=hp&ei=cRtsY63MGb-wz7sP8sSp6Aw&iflsig=AJiK0e8AAAAAY2wpgR5-_u-1K-cIq3G23Vi9Z2a9ALkI&oq=para&gs_lcp=Cgdnd3Mtd2l6EAMYADIECCMQJzIFCAAQkQIyCgguENQCELEDEEMyCggAELEDEIMBEEMyBwgAELEDEEMyBAgAEEMyBQgAEJECMgQIABBDMgcILhDUAhBDMgQIABBDOggIABCxAxCDAToLCAAQgAQQsQMQgwE6BgguEAoQQzoECC4QQzoOCC4QgwEQ1AIQsQMQgAQ6DQgAEIAEEIcCELEDEBQ6CgguELEDENQCEENQAFi8A2DdDmgAcAB4AIAB2wGIAfUEkgEFMC4zLjGYAQCgAQE&sclient=gws-wiz'
  corrector_url_entire = base_url_start + modelresponse + base_url_end
  corrector_response = requests.get(corrector_url_entire)
  corrector_page = corrector_response.text
  corrector_soup = BeautifulSoup(corrector_page, "html.parser")
  correct_name = corrector_soup.find_all(class_="MUxGbd v0nnCb lyLwlc")

  if correct_name == []:
    return (tocorr)
    # this means autocorrect has nothing to say
    # write code here.........................
  else:
    interested_part = correct_name[0].contents[1]
    a = interested_part.contents[0]
    b = a.contents[0].contents[0].contents[0]
    return (b)


# a= appolo_scrapper("https://www.apollopharmacy.in/search-medicines/paracetomol")
# print(a)