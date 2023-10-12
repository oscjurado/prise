import gspread
import datetime
import requests
import json

savedListingsJSON = open('savedListings.json', 'r')
listings = json.load(savedListingsJSON)

rolloversJSON = open('rollovers.json', 'r')
rollovers = json.load(rolloversJSON)



# aldi request
url = "https://graphql-cdn-slplatform.liquidus.net"
headers = {
    "Host": "graphql-cdn-slplatform.liquidus.net",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "Content-Type": "application/json",
    "campaignId": "955ba004cd1e8395"
}
payload = listings
response = requests.post(url, headers=headers, json=payload)
data = json.loads(response.text)
parsedList = data['data']['listings']['list']


collectedList = []
for listing in parsedList:
    department = listing['departments'][0]['name']
    title = listing['title']
    price = listing['finalPrice']
    startDate = listing['saleStartDateString']
    endDate = listing['saleEndDateString']
    priceQualifier = listing['priceQualifier']
    dealInfo = listing['additionalDealInformation']
    description = listing['description']
    description2 = listing['productDescription']
    customDescription = listing['customProductDescription']
    if department != "Non-Food":
        collectedList.append([department, title, price, startDate, endDate, priceQualifier, dealInfo, description, description2, customDescription])

# starts gspread
gc = gspread.service_account()


# Create the doc
title = 'Prices-' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
newSheet = gc.create(title)

print(title)
newSheet.share('katherinedill17@gmail.com', perm_type='user', role='writer')

# Add the data to the sheet
sheet = newSheet.sheet1

sheet.update( '1:150', collectedList)

print(sheet.get_all_records())