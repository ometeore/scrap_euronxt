import pandas as pd

dico = {
    'identification_icb': 'NR',
    'identification_instrument_name': 'TECHNIP ENERGIES',
    'identification_isin_code': 'NL0014559478',
    'identification_listing_sponsor': 'NR',
    'identification_market': 'Euronext',
    'identification_products_family': 'NR',
    'identification_symbol': 'TE',
    'identification_website_adress': 'www.technipenergies.com',
    'operation_ipo_date': 'Tue 16/02/2021',
    'operation_ipo_type': 'Direct listing',
    'operation_price_range': 'NR',
    'post': ['ceo', 'ceo 2nd', 'ceo 3rd'],
    'name': ['A', 'B', 'C']
}

dico1 = {
    'identification_icb': 'NR',
    'identification_instrument_name': 'BOLOSS',
    'identification_isin_code': 'NL0014559478',
    'identification_listing_sponsor': 'NR',
    'identification_market': 'Euronext',
    'identification_products_family': 'NR',
    'identification_symbol': 'TE',
    'identification_website_adress': 'www.technipenergies.com',
    'operation_ipo_date': 'Tue 16/02/2021',
    'operation_ipo_type': 'Direct listing',
    'operation_price_range': 'NR',
    'post': ['ceo', 'ceo 2nd', 'ceo 3rd'],
    'name': ['A', 'B', 'C']
}

#data_original = pd.DataFrame.from_dict(dico)




list_dico = [dico, dico1]

for dic in list_dico:
    data_original = pd.DataFrame.from_dict(dic)
    try: 
        data_total = data_total.append(data_original)
    except:
        data_total = pd.DataFrame(columns=data_original.columns)
        data_total = data_total.append(data_original)
print(data_total)


# maintenant la mise en forme:
data_total = data_total.sort_values(by='identification_instrument_name', ascending=True)
# ici on met de l'ordre
data_total.reset_index(inplace=True, drop=True)
# on reset l'index pour que ce soit plus propre. Attention, le drop True veut dire qu'on vire l'index précédent
# plutôt que de le garder en colonne. C'est ce qu'il faut faire si ton index précédent était les numéros de ligne,
# mais pas cool si c'était des informations importantes. print(data_original.index) pour vérifier.
data_total.to_excel('./tableau_pour_xav.xlsx')
# oui il y a des duplicatas des données pour les lignes dupliquées mais c'est bien il va pouvoir gérer ça sans souci
# avec excel et crois-moi ça vaut mieux que les valeurs vides!