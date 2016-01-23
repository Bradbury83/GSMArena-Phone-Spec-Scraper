# GSMArena-Phone-Spec-Scraper
Scrapes individual GSMArena phone specification pages for individual specs

#Web scraper for gsmarena: returns specs based on url input

#Release dates currently only work for already released phones, it'll break if called upon pre-release phone
#Could be neatened up using functions
#Only works for andoird and ios phones atm

import re
import requests
from bs4 import BeautifulSoup

def phoneGet():
	url = input("Enter site url: ")
	r = requests.get(url)
	r_html = r.text

	soup = BeautifulSoup(r_html, "html.parser")

	phoneName = soup.find(class_="specs-phone-name-title").text
	firstSpace = phoneName.index(" ")
	phoneManufacturer = phoneName[0 : firstSpace]

	specList = {}
	for tableRow in soup.find_all("tr"):	#cycles through all rows in spec table and adds row title and row content to dictionary
		try:
			specList[tableRow.find(class_="ttl").text] = tableRow.find(class_="nfo").text
		except (AttributeError):
			pass

	wirelessCharging = "No"
	quickCharge = "No"
	batterySize = "Unknown"
	for item in soup.find_all(class_="nfo"):	#less robust search based on table content for rows without titles
		try:
			if "Wireless Charging" in item.text:	#checks for wireless charging
				wirelessCharging = "Yes"
		except (AttributeError):
			pass
		try:
			if "Quick Charge" in item.text:
				quickCharge = "Yes"
		except (AttributeError):
			pass
		try:
			if "mAh battery" in item.text:
				batterySize = item.text
		except (AttributeError):
			pass

	price = soup.find(class_="price").text	#approximate price based on pricing group



	#From previous variables assign new variables based on text within prev variables

	if "Released" in specList["Status"]:	#stores phone's release year, month and date as variables
		releasedIndex = specList["Status"].index("Released")
		phoneReleaseYear = specList["Status"][releasedIndex + 9 : releasedIndex + 13]
		phoneReleaseMonth = specList["Status"][releasedIndex + 15 : len(specList["Status"])]
		phoneReleaseDate = phoneReleaseMonth + " " + phoneReleaseYear
	else:
		phoneReleaseYear = 0
		phoneReleaseMonth = 0
		phoneReleaseDate = 0

	millimetreIndex = specList["Dimensions"].index("mm")	#stores phone's dimensions, as well as its height, length, thickness as variables
	phoneDimensionsInMM = specList["Dimensions"][0 : millimetreIndex - 1]
	xIndexes = [i for i, x in enumerate(specList["Dimensions"]) if x =="x"]
	phoneHeight = specList["Dimensions"][0 : xIndexes[0] - 1]
	phoneWidth	= specList["Dimensions"][xIndexes[0] + 2 : xIndexes[1] - 1]
	phoneThickness = specList["Dimensions"][xIndexes[1] + 2 : millimetreIndex - 1]

	gIndex = specList["Weight"].index("g")	#stores phone's weight as variable
	phoneWeightInGrams = specList["Weight"][0 : gIndex - 1]

	phoneSIM = specList["SIM"] 	#stores phone's SIM card type as variable

	inchesIndex = specList["Size"].index("inches")	#stores phone's screen size as variable
	phoneScreenSize = specList["Size"][0 : inchesIndex - 1]

	pixelsIndex = specList["Resolution"].index("pixels")	#stores phones resolution, pixels high, pixels wide, PPI (pixels per inch)
	phoneResolution = specList["Resolution"][0 : pixelsIndex - 1]
	xIndex = specList["Resolution"].index("x")
	phonePixelsWide = specList["Resolution"][0 : xIndex - 1]
	phonePixelsHigh = specList["Resolution"][xIndex + 2 : pixelsIndex - 1]
	tildeIndex = specList["Resolution"].index("~")
	ppiIndex = specList["Resolution"].index("ppi")
	phonePPI = specList["Resolution"][tildeIndex + 1 : ppiIndex - 1]

	vIndexes = [i for i, x in enumerate(specList["OS"]) if x =="v"]	#stores phone's operating system and versions as variables
	if "Android" in specList["OS"]:	
		phoneOS = "Android"
		firstBlankIndex = specList["OS"][vIndexes[0] : vIndexes[0] + 10].index(" ")
		phoneOSBaseVersion = specList["OS"][vIndexes[0] + 1 : firstBlankIndex]
		if "upgradable" in specList["OS"] and len(vIndexes) > 1:
			secondBlankIndex = specList["OS"][vIndexes[1] : vIndexes[1] + 10].index(" ")
			phoneOSCurrentVersion = specList["OS"][vIndexes[1] + 1 : secondBlankIndex]
		else:
			phoneOSCurrentVersion = phoneOSBaseVersion
	elif "iOS" in specList["OS"]:
		firstCommaIndex = specList["OS"].index(",")
		phoneOS = "iOS"
		phoneOSBaseVersion = specList["OS"][4 : firstCommaIndex]
		if "upgradable" in specList["OS"]:
			upgradableIndex = specList["OS"].index("upgradable")
			phoneOSCurrentVersion = specList["OS"][upgradableIndex + 18 : len(specList["OS"])]
		else:
			phoneOSCurrentVersion = phoneOSBaseVersion

	phoneChipset = specList["Chipset"] 	#stores phone's chipset as a variable

	phoneCPU = specList["CPU"] 	#stores phone's chipset, core count and clock speed as a variable
	if "Dual-core" in specList["CPU"]:
		phoneCoreCount = "2"
	elif "Quad-core" in specList["CPU"]:
		phoneCoreCount = "4"
	elif "Octa-core" in specList["CPU"]:
		phoneCoreCount = "8"
	elif "Hexa-core" in specList["CPU"]:
		phoneCoreCount = "6"
	else:
		phoneCoreCount = "1"

	phoneGPU = specList["GPU"] 	#stores phone's chipset as a variable

	phoneCardSlot = specList["Card slot"] 	#stores phone's car slot status as a variable

	GBIndex = specList["Internal"].index("GB")	#stores phone's internal storage and RAM as variables
	phoneStorage = specList["Internal"][0 : GBIndex - 1]
	h = len(list(specList["Internal"]))
	if "MB" in specList["Internal"]:
		v = specList["Internal"][h - 10: h - 7]
		phoneRAM = str(int(v) / 1000.0)
	else:
		phoneRAM = specList["Internal"][h - 8 : h - 7]

	MPIndex = specList["Primary"].index("MP")	#stores phone's primary camera megapixel count as a variable
	phoneCameraPrimaryInMP = specList["Primary"][0 : MPIndex - 1]

	try:
		MP2Index = specList["Secondary"].index("MP")	#stores phone's secondary camera megapixel count as a variable
		phoneCameraSecondaryInMP = specList["Secondary"][0 : MP2Index - 1]
	except (ValueError):
		phoneCameraSecondaryInMP = "N/A"

	firstCommaIndex2 = specList["WLAN"].index(",")	#stores phone's wifi chip info as variable
	wifiIndex = specList["WLAN"].index("Wi-Fi")
	phoneWifiChip = specList["WLAN"][wifiIndex + 6 : firstCommaIndex2]

	firstCommaIndex3 = specList["Bluetooth"].index(",")	#stores phone's bluetooth version as variable
	phoneBluetooth = specList["Bluetooth"][1 : firstCommaIndex3]

	try:
		phoneNFC = specList["NFC"] 	#stores phone's NFC status as variable
	except (KeyError):
		phoneNFC = "No"

	phoneWirelessCharging = wirelessCharging 	#stores phone's wireless charging status as variable

	try:
		maHIndex = batterySize.index("mAh")	#stores phone's battery size as a variable
		phoneBatterySizeInMAh = batterySize[maHIndex - 5 : maHIndex - 1]
	except (ValueError):
		phoneBatterySizeInMAh = "Unknown"

	return {"phoneName" : phoneName, "phoneManufacturer" : phoneManufacturer, "phoneReleaseMonth" : phoneReleaseMonth, "phoneReleaseYear" : phoneReleaseYear, "phoneReleaseDate" : phoneReleaseDate, "phoneDimensionsInMM" : phoneDimensionsInMM, "phoneHeight" : phoneHeight, "phoneWidth" : phoneWidth, "phoneThickness" : phoneThickness, "phoneWeightInGrams" : phoneWeightInGrams, "phoneSIM" : phoneSIM, "phoneScreenSize" : phoneScreenSize, "phoneResolution" : phoneResolution, "phonePixelsHigh" : phoneResolution, "phonePixelsWide" : phonePixelsWide, "phonePPI" : phonePPI, "phoneOS" : phoneOS, "phoneOSBaseVersion" : phoneOSBaseVersion, "phoneOSCurrentVersion" : phoneOSCurrentVersion, "phoneChipset" : phoneChipset, "phoneCPU" : phoneCPU, "phoneCoreCount" : phoneCoreCount, "phoneGPU" : phoneGPU, "phoneCardSlot" : phoneCardSlot, "phoneStorage" : phoneStorage, "phoneRAM" : phoneRAM, "phoneCameraPrimaryInMP" : phoneCameraPrimaryInMP, "phoneCameraSecondaryInMP" : phoneCameraSecondaryInMP, "phoneWifiChip" : phoneWifiChip, "phoneBluetooth" : phoneBluetooth, "phoneNFC" : phoneNFC, "phoneWirelessCharging" : phoneWirelessCharging, "phoneBatterySizeInMAh" : phoneBatterySizeInMAh}

phoneList = []
phoneList.append(phoneGet())
while True:
	v = input("Add another phone? ")
	if v == "Yes" or v == "yes" or v == "y" or v== "Y":
		phoneList.append(phoneGet())
	else:
		break

print(phoneList)
