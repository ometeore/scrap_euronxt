from selenium import webdriver
from selenium.common import exceptions
import pandas as pd
import pprint


def add_to_dict(dico, nom, elm):
	if len(elm)>0:
		dico[nom] = elm[0][0]
	else:
		dico[nom] = ''

########### check last element of an iterable
def lookahead(iterable):
	it = iter(iterable)
	try:
		last = next(it)
	except StopIteration:
		return
	for val in it:
		yield last, True
		last = val
	yield last, False

def longest_array(dico):
	max = 1
	for key, value in dico.items():
		if type(value) is list and len(value) > max:
			max = len(value)
	return max

def complete_array(dico, max):
	for key, value in dico.items():
		if type(value) is list and len(value) != max:
			while len(value) != max:
				value.extend([''])



#charge la page n1 a remplir 101 fois a peu pres 15 min/page pour 
for i in range(1):
	url = 'https://live.euronext.com/en/ipo-showcase?field_keys=&field_iponi_ipo_date_value%5Bmin%5D=&field_iponi_ipo_date_value%5Bmax%5D=&page=' + str(i)
	browser = webdriver.Firefox()
	browser.get(url)


	##################   recupère et listes toute les lignes --> [[],[row0],[row1],....]
	#### première liste vide (sans doute le thead)


	list_of_lists = [[td.text
					  for td in tr.find_elements_by_xpath('td')]
					  for tr in browser.find_elements_by_xpath('//tr')]


	####### recupère les info de la main page et parse par ligne pour rentrer dans chaque lien

	####################################### A PARTIR D ICI ON BOUCLE SUR CHAQUE COMPANY


	for row in list_of_lists[1:]:

		temp_dict = {}
		temp_dict['company_name'] = row[1]

		url_company = browser.find_element_by_partial_link_text(row[1]).get_attribute("href")
		driver = webdriver.Firefox()
		driver.get(url_company)


		###############################################################################
		####################### LA PARTIE OPERATION ###################################
		###############################################################################



		operation_ipo_type_list = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-issue-type')]

		operation_ipo_date = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-ipo-date')]

		operation_price_range = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-price-range')]	

		operation_price = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-ipo-price')]

		operation_categorie = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-issue-type')]

		add_to_dict(temp_dict, 'operation_ipo_type', operation_ipo_type_list)
		add_to_dict(temp_dict, 'operation_ipo_date', operation_ipo_date)
		add_to_dict(temp_dict, 'operation_price_range', operation_price_range)
		add_to_dict(temp_dict, 'operation_price', operation_price)
		add_to_dict(temp_dict, 'operation_categorie', operation_categorie)





		###############################################################################
		####################### LA PARTIE IDENTIFICATION ##############################
		###############################################################################


		identification_instrument_name = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-instrument-name')]

		identification_symbol = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-ticker-symbol')]

		identification_isin_code = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-isin-code')]

		identification_listing_sponsor = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-listing-sponsor')]

		identification_market = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-exchange__market')]
		
		identification_products_family = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-products-family')]

		identification_icb = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-icb')]
		
		identification_website_adress = [[elm.text
						for elm in ipo.find_elements_by_class_name('field__item')]
						for ipo in driver.find_elements_by_class_name('field--name-field-iponi-website-address')]
		
		
		add_to_dict(temp_dict, 'identification_instrument_name', identification_instrument_name)
		add_to_dict(temp_dict, 'identification_symbol', identification_symbol)
		add_to_dict(temp_dict, 'identification_isin_code', identification_isin_code)
		add_to_dict(temp_dict, 'identification_listing_sponsor', identification_listing_sponsor)
		add_to_dict(temp_dict, 'identification_market', identification_market)
		add_to_dict(temp_dict, 'identification_products_family', identification_products_family)
		add_to_dict(temp_dict, 'identification_icb', identification_icb)
		add_to_dict(temp_dict, 'identification_website_adress', identification_website_adress)







		###############################################################################
		####################### KEY EXECUTIVES  #######################################
		###############################################################################


		i = 0
		key_executives_fonction = []
		key_executives_names = []
		temp_dict['last_update_key_executives'] = ''

		new_text=driver.find_elements_by_xpath(("//table[@id='key-executives-table-values-nodrag']/tbody/tr/td"))
		for text, end in lookahead(new_text):
			if not end:
				temp_dict['last_update_key_executives'] = text.text
				continue
			if i%2 == 0:
				key_executives_fonction.append(text.text)
			else:
				key_executives_names.append(text.text)
			i = i + 1


		temp_dict['key_executives_fonction'] = key_executives_fonction
		temp_dict['key_executives_names'] = key_executives_names




		###############################################################################
		####################### SHAREHOLDERS ##########################################
		###############################################################################


		i = 0
		shareholders_name = []
		shareholders_share = []
		temp_dict['shareholders_last_update'] = ''

		new_text=driver.find_elements_by_xpath(("//table[@id='shareholders-table-values-nodrag']/tbody/tr/td"))
		for text, end in lookahead(new_text):
			if not end:
				temp_dict['shareholders_last_update'] = text.text
				continue
			if i%2 == 0:
				shareholders_name.append(text.text)
			else:
				shareholders_share.append(text.text)
			i = i + 1


		temp_dict['shareholders_name'] = shareholders_name
		temp_dict['shareholders_share'] = shareholders_share


		###############################################################################
		####################### DOCUMENTATION #########################################
		###############################################################################

		temp_dict['documentation_url'] = browser.find_element_by_partial_link_text(row[1]).get_attribute("href")


		###############################################################################
		####################### KEY_FIGURES ###########################################
		###############################################################################

		key_figures_year = []
		key_figures_net_sales = []
		key_figures_consumed_purchases = []
		key_figures_personnal_costs = []
		key_figures_operating_profit = []
		key_figures_income_tax = []
		key_figures_net_income = []
		key_figures_net_consolidated_income = []
		key_figures_length_of_fiscal_year = []
		key_figures_curency = []


		############Ce con recupere tous les tableau et honnetement franchement voila#############
		list_of_lists_2 = [[[td.text
		  for td in tr.find_elements_by_xpath('td')]
		  for tr in table.find_elements_by_xpath('//tr')]
		  for table in driver.find_elements_by_xpath("//table[@id='key-figures-table-en']")]
		
		try:
			for elm in list_of_lists_2[0]:
				if len(elm)>0:
					if elm[0] == "Net sales":
						key_figures_net_sales.extend(elm[1:])
					if elm[0] == "Consumed purchases":
						key_figures_consumed_purchases.extend(elm[1:])
					if elm[0] == "Personnal costs":
						key_figures_personnal_costs.extend(elm[1:])					
					if elm[0] == "Consumed purchases":
						key_figures_consumed_purchases.extend(elm[1:])
					if elm[0] == "Operating profit":
						key_figures_operating_profit.extend(elm[1:])
					if elm[0] == "Income tax":
						key_figures_income_tax.extend(elm[1:])
					if elm[0] == "Net income":
						key_figures_net_income.extend(elm[1:])
					if elm[0] == "Fiscal year end":   #maybe maybe not
						key_figures_length_of_fiscal_year.extend(elm[1:])
					if elm[0] == "Currency & Unit":
						key_figures_curency.extend(elm[1:])

		except IndexError:
			print("IndexError")



		list_of_lists_3 = [[[td.text
		  for td in tr.find_elements_by_xpath('th')]
		  for tr in table.find_elements_by_xpath('//tr')]
		  for table in driver.find_elements_by_xpath("//table[@id='key-figures-table-en']")]

		try:
			for elm in list_of_lists_3[0]:
				if len(elm)>0:
					if elm[0] == "MILLENIUM":
						key_figures_year.extend(elm[1:])
		except IndexError:
			print("FY")




		temp_dict['key_figures_year'] = key_figures_year
		temp_dict['key_figures_net_sales'] = key_figures_net_sales
		temp_dict['key_figures_consumed_purchases'] = key_figures_consumed_purchases
		temp_dict['key_figures_personnal_costs'] = key_figures_personnal_costs
		temp_dict['key_figures_consumed_purchases'] = key_figures_consumed_purchases
		temp_dict['key_figures_operating_profit'] = key_figures_operating_profit
		temp_dict['key_figures_income_tax'] = key_figures_income_tax
		temp_dict['key_figures_net_income'] = key_figures_net_income
		temp_dict['key_figures_length_of_fiscal_year'] = key_figures_length_of_fiscal_year
		temp_dict['key_figures_curency'] = key_figures_curency


		###############################################################################
		######################## EXCELCIUR ############################################
		###############################################################################

		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(temp_dict)


		#first is to equalize the array by adding empty elm to the one in lack
		size = longest_array(temp_dict)

		complete_array(temp_dict, size)

		data_original = pd.DataFrame.from_dict(temp_dict)

		try: 
			data_total = data_total.append(data_original)
		except:
			data_total = pd.DataFrame(columns=data_original.columns)
			data_total = data_total.append(data_original)

		data_total = data_total.sort_values(by='company_name', ascending=True)
		data_total.reset_index(inplace=True, drop=True)


		data_total.to_excel('./tableau_pour_xav.xlsx')

		pp.pprint(temp_dict)





		driver.quit()
	browser.quit()