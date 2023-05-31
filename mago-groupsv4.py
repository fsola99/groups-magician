import requests
from bs4 import BeautifulSoup
import csv

lista_grupos = []
dic_grupo_tec = {}
i = 0
dic_id_grupo = {}
dic_tecnicas_nombre = {}

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
                lista_grupos.append(group_id)

    for row_grupos in table.find_all('tr'):
        # Encontrar todas las celdas de la fila
        cells_grupos = row_grupos.find_all('td')
        if len(cells_grupos) >= 2:  # Verificar si hay al menos dos celdas
            nombre_grupo = cells_grupos[1].text.strip()
            dic_id_grupo[lista_grupos[i]] = [nombre_grupo]  # {GXXX: [nombre_grupo]}
            i = i + 1

    for grupo in lista_grupos:
        url_grupo = url + "/" + grupo
        response_grupo = requests.get(url_grupo)
        soup_grupo = BeautifulSoup(response_grupo.content, 'html.parser')

        table_tecnicas = soup_grupo.find('table', {'class': 'table techniques-used background table-bordered'})

        # Recorrer las filas de la tabla
        lista_id = []
        try:
            tec_id_aux=""
            for row_tec in table_tecnicas.find_all('tr'):
                # Encontrar todas las celdas de la fila
                cells = row_tec.find_all('td')
                if len(cells) >= 2:  # Verificar si hay al menos dos celdas
                    tec_id = cells[1].text.strip()
                    if tec_id.startswith('T'):  # Filtrar solo los IDs que comienzan con 'T'
                        tec_id_aux=tec_id
                        subtec_id = cells[2].text.strip()  # Obtener el ID de la subtecnología si existe
                        if subtec_id.startswith('.'):
                            tec_id += subtec_id  # Concatenar el ID de la subtecnología a la tecnología principal
                        lista_id.append(tec_id) 
                    else:
                       subtec_id = cells[2].text.strip()  # Obtener el ID de la subtecnología si existe
                       if subtec_id.startswith('.'):
                        lista_id.append(tec_id_aux + subtec_id) # Concatenar el ID de la subtecnología a la tecnología principal
                        

            dic_grupo_tec[grupo] = lista_id  # {GXXX: [tec_id, tec_id, ...]}
            lista_id = []
        except:
            dic_grupo_tec[grupo] = []  # Grupo sin técnicas

    
    
    for grupo, tecnicas in dic_grupo_tec.items():
      for tecnica in tecnicas:
        if tecnica not in dic_tecnicas_nombre:
          url_id = 'https://attack.mitre.org/techniques/'

          if '.' in tecnica:
            subtecnica_id = tecnica.split('.')
            url_id += subtecnica_id[0]+'/'+subtecnica_id[1]
          else:
            url_id += tecnica

          # Realizar la solicitud HTTP GET a la página
          response_id = requests.get(url_id)
          print(url_id)
          # Verificar si la solicitud fue exitosa
          if response_id.status_code == 200:
              # Crear un objeto BeautifulSoup con el contenido HTML de la página
              soup_id = BeautifulSoup(response_id.content, 'html.parser')

              # Encontrar la tabla que contiene los grupos
              titulo = soup_id.find('h1').text.strip() #, {'id': 'table techniques-used background table-bordered'}
              if ':' in titulo:
                titulo_separado= titulo.split(":")
                titulo= titulo_separado[0]+": "+titulo_separado[1].lstrip()
              
              dic_tecnicas_nombre[tecnica]=tecnica+' - '+titulo #{T1234: T1234-Blablabla, ...}

          '''
              tactica = soup_id.find('div',{'class': 'col-md-11 pl-0'})
              tactica_separada=tactica.split(':')
              tactica_lista=tactica_separada.split(',')
              print(tactica_lista)
              #desc = soup.find()'''

    # Crear un archivo CSV y escribir las columnas
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID de la Tecnica o Subtecnica', 'Actor', 'Tactica', 'Tecnica o Subtecnica','Descripcion de la Tecnica o Subtecnica (MITRE)'])

        # Escribir los datos en el archivo CSV
        for grupo, tecnicas in dic_grupo_tec.items():
            for tecnica in tecnicas:
                writer.writerow([tecnica, dic_id_grupo[grupo][0],"-",dic_tecnicas_nombre[tecnica],"-"])

else:
    print('No se pudo acceder a la página:', response.status_code)
