import requests
import matplotlib.pyplot as plt

# headers = {"X-ClientId":"YOUR-API-KEY"}
headers = {}
plt.rcParams['figure.figsize'] = [19.2, 10.8]

def get_product_info(product_id):
    url = f'https://bdl.stat.gov.pl/api/v1/data/by-variable/{product_id}?format=json&unit-level=0'
    response = requests.get(url, headers=headers)
    data = response.json()
    results = [(item['year'], item['val']) for item in data['results'][0]['values']]
    years, values = list(zip(*results))
    return (years, values)


# **** get interesting products IDs ****
subject_url = 'https://bdl.stat.gov.pl/api/v1/variables?subject-id=P1466&format=json&lang=pl&page-size=100'
response = requests.get(subject_url, headers=headers)
data = response.json()
food_ids_and_name = [(item['id'], item['n1']) for item in data['results']]
food_ids_and_name = food_ids_and_name[:20]


# **** parse single ****
number_of_products = len(food_ids_and_name)
cmap = plt.get_cmap('jet')
colors = []
for index, (product_id, product_name) in enumerate(food_ids_and_name):
    print(product_id, product_name)
    years, values = get_product_info(product_id)
    current_color = cmap(index/number_of_products)
    colors.append(current_color)
    plt.plot(years, values, label=f'{product_id} - {product_name}')
    
plt.legend(loc='upper left')
plt.show()
