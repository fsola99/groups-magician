import requests
from bs4 import BeautifulSoup

lista_grupos = []
lista_id = []
dic_grupo_tact = {}

url = 'https://attack.mitre.org/groups/'

# Realizar la solicitud HTTP GET a la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Crear un objeto BeautifulSoup con el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar la tabla que contiene los grupos
    table = soup.find('table')

    # Recorrer las filas de la tabla
    for row in table.find_all('tr'):
        # Encontrar la celda que contiene el ID del grupo
        id_cell = row.find('td')

        # Extraer el ID del grupo si se encuentra la celda
        if id_cell:
            group_id = id_cell.text.strip()
            if group_id.startswith('G'):  # Filtrar solo los IDs que comienzan con 'G'
                print(group_id)
                lista_grupos.append(group_id)

    for grupo in lista_grupos:
        url_grupo = url + "/" + grupo
        response_grupo = requests.get(url_grupo)
        soup_grupo = BeautifulSoup(response_grupo.content, 'html.parser')

        table_tecnicas = soup_grupo.find('table', {'class': 'table techniques-used background table-bordered'})

        # Recorrer las filas de la tabla
        #print("El problema termina siendo: "+ grupo) PROBLEMON G0097 NO TIENE TECNICA. FIJARSE.

        for row_tact in table_tecnicas.find_all('tr'):
            # Encontrar todas las celdas de la fila
            cells = row_tact.find_all('td')
            if len(cells) >= 2:  # Verificar si hay al menos dos celdas
                tact_id = cells[1].text.strip()
                if tact_id.startswith('T'):  # Filtrar solo los IDs que comienzan con 'T'
                    #print(tact_id)
                    lista_id.append(tact_id)
                    print(tact_id)

        dic_grupo_tact[grupo]=lista_id

    print(dic_grupo_tact)


else:
    print('No se pudo acceder a la página:', response.status_code)

print(lista_id)
