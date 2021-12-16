import os
from PIL import Image
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://XXXX.cognitiveservices.azure.com/"
credential = AzureKeyCredential("XXXXXXXXXXXXX")

document_analysis_client = DocumentAnalysisClient(endpoint, credential)
model_id = "XXXXXXXXXXXXXXXXXXX"


# Creating the DataFrame:
df = pd.DataFrame(columns=['part_no', 'batch_no', 'quantity', 'weigth', 'date', 'serial'])


# File Directory
dir_name = 'C:/Users//XXXXX/Barcode/'
image_name = os.listdir(dir_name)


i = 1

for doc in image_name:
    print(i)
    i +=1
    # Resizing the image
    image = Image.open(f'{dir_name}/{doc}')
    l = image.size[0]
    w = image.size[1]
    if l > 2100:
        image = image.resize((2000, int(2000 / l * w)))
        image.save(f'{dir_name}/{doc}')
        
        

    with open(f'{dir_name}/{doc}', "rb") as fd:
        document = fd.read()

    poller = document_analysis_client.begin_analyze_document(model=model_id, document=document)
    result = poller.result()

#     for analyzed_document in result.documents:
#         print("Document was analyzed by model with ID {}".format(result.model_id))
#         print("Document has confidence {}".format(analyzed_document.confidence))
        
        for name, field in analyzed_document.fields.items():
            print("Field '{}' has value '{}' with confidence of {}".format(name, field.value, field.confidence))
            df.loc[doc[:15], name] = field.value
        
        
df


## Comment ##
# iterate over lines, words, and selection marks on each page of the document
for page in result.pages:
    print("\nLines found on page {}".format(page.page_number))
    for line in page.lines:
        print("...Line '{}'".format(line.content))
    print("\nWords found on page {}".format(page.page_number))
    for word in page.words:
        print(
            "...Word '{}' has a confidence of {}".format(
                word.content, word.confidence
            )
        )
    print("\nSelection marks found on page {}".format(page.page_number))
    for selection_mark in page.selection_marks:
        print(
            "...Selection mark is '{}' and has a confidence of {}".format(
                selection_mark.state, selection_mark.confidence
            )
        )

# iterate over tables in document
for i, table in enumerate(result.tables):
    print("\nTable {} can be found on page:".format(i + 1))
    for region in table.bounding_regions:
        print("...{}".format(region.page_number))
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
                cell.row_index, cell.column_index, cell.content
            )
        )