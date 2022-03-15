# Modern Data Engineering Architect Solution
📚Proof of Concept Solution to Batch Data Load with Azure Data Factory to Azure SQL DB with Azure Functions (Python) and Azure Key Vault

## Criteria:
- Develop Python API with HTTP Request (Make sure to have KeyVault Implemented)
- Get file from web API with Azure Function and store it on Azure Data Lake Storage Gen 2 > Blob container
- Azure Function is HTTP triggered and Azure Data Factory is blob triggered event
- Load only new records from the file to Azure SQL Database (based on the primary key)
- Use the Consumption plan for Azure Function.
- Backup the input file into another Azure Data Lake Storage Gen 2 > Blob container.

I am using web api to scrape data from: https://pokeapi.co/api/v2/pokemon/

![image](https://user-images.githubusercontent.com/22649754/158362472-2637896d-60c3-4c3c-b3b8-2ac89a593c0f.png)

