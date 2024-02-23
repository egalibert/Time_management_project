import uuid
# report_uploader creates and uploads a new blob storage which consists of working_hours_report.txt
# Import the client object from the SDK library
from azure.storage.blob import BlobClient
#Connects to Azure storage account (needs proper connection string)
def export_data():
    conn_string = "" 
    # vaihda connection string tähän 
    # az storage account show-connection-string --name timestorage123 --resource-group Elliot_Joel_RG

    #Creates BlobClient object, specifies container name and gives the blob a random name
    blob_client = BlobClient.from_connection_string(
        conn_string,
        container_name="blob-container-01",
        blob_name=f"sample-blob-{str(uuid.uuid4())[0:5]}.txt",
    )

    # Open a local file "working_hours_report.txt" and upload its contents to Blob Storage
    with open("working_hours_report.txt", "rb") as data:
        blob_client.upload_blob(data)
        print(f"Uploaded working_hours to {blob_client.url}")

if __name__ == '__main__':
    export_data()