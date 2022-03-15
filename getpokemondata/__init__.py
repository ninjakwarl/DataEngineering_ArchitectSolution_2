import logging
import pandas as pd
import requests
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from azure.identity import DefaultAzureCredential
import azure.functions as func
from getpokemondata import config as cfg

def get_pokemons(url = 'https://pokeapi.co/api/v2/pokemon/'):
	name = []
	weight = []
	height = []
	base_hp = []
	pokeid = []

	for i in range (208):
		response = requests.get(url+str(i))
		if response.status_code == 200:
			payload = response.json()
			pokeid.append(payload ['id'])
			name.append(payload ['name'])
			weight.append(payload ['weight'])
			height.append(payload ['height'])
			base_hp.append(payload ['stats'] [0] ['base_stat'])
	return pokeid, name, weight, height, base_hp

def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Python HTTP trigger function processed a request.')

	
	pokeid, name, weight, height, base_hp = get_pokemons()	
	poke_df = pd.DataFrame({
		'pokemon_id': pokeid,
		'pokemon_name' : name,
		'weight' : weight,
		'height' : height,
		'base_hp' : base_hp
		}, index = pokeid)
	pokecsv = poke_df.to_csv(index=False, encoding = "utf-8")
	print(pokecsv)

	connection_string= cfg.GetBlobKeySecret
	blob_service_client = BlobServiceClient.from_connection_string(connection_string)
	container_client_main = blob_service_client.get_container_client('rawdatasource')
	container_client_archive = blob_service_client.get_container_client('archivedata')

	try:
		container_client_archive.create_container()
		container_client_main.create_container()
		properties1 = container_client_main.get_container_properties()
		properties2 = container_client_archive.get_container_properties()
	except Exception as ex:
		logging.info("Container already exists")
	
	file = "extracted_pokemondata"+ "-" + cfg.stringtime + ".csv"
	blobmain = container_client_main.get_blob_client(file)
	blobmain.upload_blob(pokecsv)
	blobarchive = container_client_archive.get_blob_client(file)
	blobarchive.upload_blob(pokecsv)
	
	logging.info(f"Blob trigger executed!")
	

	return func.HttpResponse(f"the {file} loaded to main blob and achived to blob - archivedata successfully")