# !sudo apt install tesseract-ocr
# !pip install pytesseract

from PIL import Image
import pytesseract
import io
import re
import time
import boto3
import pandas as pd
import json

def check_keyword(text,keyword):
    return keyword in text.split()

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]+', ' ', text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

def get_text_from_image(image):
    text = pytesseract.image_to_string(image)
    text = clean_text(text)
    return text


def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']

def get_dataframes(tables,cells,words,selections):
    dataframes = []

    for table in tables.values():
        # Determine all the cells that belong to this table
        table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

        # Determine the table's number of rows and columns
        n_rows = max(cell['RowIndex'] for cell in table_cells)
        n_cols = max(cell['ColumnIndex'] for cell in table_cells)
        content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

        # Fill in each cell
        for cell in table_cells:
            cell_contents = [
                words[child_id]['Text']
                if child_id in words
                else selections[child_id]['SelectionStatus']
                for child_id in get_children_ids(cell)
            ]
            i = cell['RowIndex'] - 1
            j = cell['ColumnIndex'] - 1
            content[i][j] = ' '.join(cell_contents)

        # We assume that the first row corresponds to the column names
        column_names = [f'col{i+1}' for i in range(0,n_cols)]
        dataframe = pd.DataFrame(content[0:],columns=column_names)
        dataframes.append(dataframe)
    
    return dataframes

def extract_table(image_path,client):
    im = Image.open(image_path)

    buffered = io.BytesIO()
    im.save(buffered, format='PNG')

    response = client.analyze_document(Document={'Bytes': buffered.getvalue()},
                                        FeatureTypes=['TABLES']
                                        )
    
    blocks = response['Blocks']
    tables = map_blocks(blocks, 'TABLE')
    cells = map_blocks(blocks, 'CELL')
    words = map_blocks(blocks, 'WORD')
    selections = map_blocks(blocks, 'SELECTION_ELEMENT')

    dataframes = get_dataframes(tables,cells,words,selections)
    return dataframes

def dataframe_to_json(df):
    df_json = df.to_json(orient='index')
    return df_json

def json_to_dataframe(df_json):
    df_json = json.loads(df_json)
    df = pd.DataFrame.from_dict(df_json,orient='index')
    return df

if __name__=="__main__":
    image_path = 'Predicted Quarterly/inferenced_image_0_21.jpeg'
    start_time = time.time()
    client = boto3.client('textract',
                      aws_access_key_id = '..',
                      aws_secret_access_key = '..',
                      region_name = 'us-west-2')
    dataframes = extract_table(image_path,client)
    delta = time.time()-start_time
    df_json = dataframe_to_json(dataframes[0])
    df = json_to_dataframe(df_json)
    
    start_time = time.time()
    text = get_text_from_image(Image.open(image_path))
    check_keyword(text,'consolidated')
    standalone = check_keyword(text,'standalone')
    consolidated = check_keyword(text,'consolidated')
    print(standalone,consolidated)
    print('text checking : ',time.time()-start_time)
    print('textract time : ',delta)
    print(len(dataframes))