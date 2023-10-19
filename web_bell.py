import pytesseract
from PIL import Image
import cv2
from datetime import datetime
import os
import re
import zipfile
import io
import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Cert",
    layout = 'wide',
)

st.title('Cert Scraper BELL')

def crop_image(img):
    # Get the dimensions of the original image
    height, width, channels = img.shape if len(img.shape) == 3 else (img.shape[0], img.shape[1], 1)

    top =  int(height/8.24)
    bottom = int(height/ 5.55)
    left_crop1 = int(width/ 3.05)
    right_crop1 = int(width/2.19625)

    top_crop2 = int(height/4)
    bottom_crop2 = int(height/1.9776)
    left_crop2 = 0
    right_crop2 = int(width/2)

    top_crop3 = int(height/ 1.6773)
    bottom_crop3 = int(height/ 1.413)
    left_crop3 = int(width/ 17.57)
    right_crop3 = int(width/ 2.9283)

    top_crop4 = int(height/1.9776)
    bottom_crop4 = int(height/1.72)
    left_crop4 = int(width/ 4.136)

    top_crop5 = int(height/2.38)
    bottom_crop5 = int(height/1.9776)
    left_crop5 = int(width/ 4.136)

    crop1 = img[top:bottom, left_crop1:right_crop1]
    crop2 = img[top_crop2:bottom_crop2, left_crop2:right_crop2]
    crop3 = img[top_crop3:bottom_crop3, left_crop3:right_crop3]
    crop4 = img[top_crop4:bottom_crop4, left_crop4:right_crop2]
    crop5 = img[top_crop5:bottom_crop5, left_crop5:right_crop2]

    return crop1, crop2, crop3, crop4, crop5

# Initialize the Tesseract OCR
def initialize_tesseract():
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Initialize Tesseract
initialize_tesseract()

def process_cropped_images(img):
    # Perform OCR on the cropped image
    extracted_text = pytesseract.image_to_string(img)

    return extracted_text

def process_cropped_images(img):
    # Perform OCR on the cropped image
    extracted_text = pytesseract.image_to_string(img)

    return extracted_text

def extract_gemstone_info(img):
    # Assuming you have the functions crop_image and process_cropped_images defined elsewhere
    crop1, crop2, crop3, crop4, crop5 = crop_image(img)
    extracted_texts1 = process_cropped_images(crop1)
    lines1 = [line for line in extracted_texts1.split('\n') if line.strip()]


    extracted_texts2 = process_cropped_images(crop2)
    lines2 = [line for line in extracted_texts2.split('\n')]
    lines2 = [line.strip() for line in lines2 if line.strip()]
    if len(lines2) == 6 :
        lines2 = [line.split() for line in lines2]
        g = lines2[0][-1]
        ct = lines2[1][-2] + ' ct'
        dimen = lines2[2][-6] + ' x ' + lines2[2][-4] + ' x ' +lines2[2][-2] + ' mm'
        s = lines2[3][-1]
        lines2 = [g] + [ct] + [dimen] + [s]
    else:
        lines2 = [line.split() for line in lines2]
        g = 'gem'
        ct = lines2[0][-2] + ' ct'
        dimen = lines2[1][-6] + ' x ' + lines2[1][-4] + ' x ' +lines2[1][-2] + ' mm'
        s = lines2[2][-1]
        lines2 = [g] + [ct] + [dimen] + [s]

    extracted_texts5 = process_cropped_images(crop5)
    lines5 = [line.split(' ', 1)[1] if ' ' in line else line for line in extracted_texts5.split('\n')]
    lines5 = [line.strip() for line in lines5 if line.strip()]

    extracted_texts4 = process_cropped_images(crop4)
    lines4 = [line for line in extracted_texts4.split('\n') if line.strip()]

    extracted_texts3 = process_cropped_images(crop3)
    lines3 = [line for line in extracted_texts3.split('\n') if line.strip()]
    filtered_lines3 = [line for line in lines3 if 'may be called' in line]

    combined_lines = lines1 + lines2+ lines5 + lines4 + filtered_lines3
    
    if len(combined_lines) == 11 :
        df = pd.DataFrame({i: [combined_lines[i]] for i in range(11)})
        df[0] = df[0].str.strip('REPORT No.')
        df[10] = df[10].str.extract(r'may be called "([^"]+)"', expand=False)
        df = df.drop([2], axis=1)
        df = df.rename(columns={0: 'certNo', 1:'issuedDate',
                                3:'Carat',4 : 'Dimensions', 
                                5:'Shape', 6: 'Identification',
                                7: 'Color', 8:'indications',
                                9: 'Origin', 10: 'Color0'})
    elif len(combined_lines) == 10 :
        df = pd.DataFrame({i: [combined_lines[i]] for i in range(10)})
        df[0] = df[0].str.strip('REPORT No.')
        df = df.drop([2], axis=1)
        df = df.rename(columns={0: 'certNo', 1:'issuedDate',
                                3:'Carat',4 : 'Dimensions', 
                                5:'Shape', 6: 'Identification',
                                7: 'Color', 8:'indications',
                                9: 'Origin'})
    else :
        df = pd.DataFrame({i: [combined_lines[i]] for i in range(10)})
        df[0] = df[0].str.strip('REPORT No.')
        df = df.drop([2], axis=1)
        df = df.rename(columns={0: 'certNo', 1:'issuedDate',
                                3:'Carat',4 : 'Dimensions', 
                                5:'Shape', 6: 'Identification',
                                7: 'Color', 8:'indications',
                                9: 'Origin'})
        
    return df

def extract_gemstone_info1(img):
    crop1, crop2, crop3, crop4, crop5 = crop_image(img)

    extracted_texts1 = process_cropped_images(crop1)
    lines1 = [line for line in extracted_texts1.split('\n') if line.strip()]

    extracted_texts2 = process_cropped_images(crop2)
    lines2 = [line for line in extracted_texts2.split('\n')]
    lines2 = [line.strip() for line in lines2 if line.strip()]
    lines2 = [line.split() for line in lines2]
    g = lines2[0][-1]
    ct = lines2[1][-2] + ' ct'
    dimen = lines2[2][-6] + ' x ' + lines2[2][-4] + ' x ' +lines2[2][-2] + ' mm'
    s = lines2[3][-1]
    id = lines2[4][-1]
    c = lines2[5][-1]
    lines2 = [g] + [ct] + [dimen] + [s] + [id] +[c]

    extracted_texts5 = process_cropped_images(crop5)
    # Split each line by space and take only parts after the first space (if space exists)
    lines5 = [line.split(' ', 1)[1] if ' ' in line else line for line in extracted_texts5.split('\n')]

    # Remove leading and trailing whitespace from each line and filter out empty strings
    lines5 = [line.strip() for line in lines5 if line.strip()]

    extracted_texts4 = process_cropped_images(crop4)
    lines4 = [line for line in extracted_texts4.split('\n') if line.strip()]

    extracted_texts3 = process_cropped_images(crop3)
    lines3 = [line for line in extracted_texts3.split('\n') if line.strip()]
    filtered_lines3 = [line for line in lines3 if 'may be called' in line]

    combined_lines = lines1 + lines2+ lines5 + lines4 + filtered_lines3

    if len(combined_lines) == 11 :
        df = pd.DataFrame({i: [combined_lines[i]] for i in range(11)})
        df[0] = df[0].str.strip('REPORT No.')
        df[10] = df[10].str.extract(r'may be called "([^"]+)"', expand=False)
        df = df.drop([2], axis=1)
        df = df.rename(columns={0: 'certNo', 1:'issuedDate',
                                3:'Carat',4 : 'Dimensions', 
                                5:'Shape', 6: 'Identification',
                                7: 'Color', 8:'indications',
                                9: 'Origin', 10: 'Color0'})
    elif len(combined_lines) == 10 :
        df = pd.DataFrame({i: [combined_lines[i]] for i in range(10)})
        df[0] = df[0].str.strip('REPORT No.')
        df = df.drop([2], axis=1)
        df = df.rename(columns={0: 'certNo', 1:'issuedDate',
                                3:'Carat',4 : 'Dimensions', 
                                5:'Shape', 6: 'Identification',
                                7: 'Color', 8:'indications',
                                9: 'Origin'})
    
    return df

def detect_color(text):
    text = str(text).lower()  # Convert the text to lowercase
    if 'vivid red' in text:
        return "VividRed"
    elif 'vivid pink' in text:
        return 'VividPink'
    elif 'pinkish red' in text:
        return "PinkishRed"
    elif "royal blue"  in text:
        return "RoyalBlue"
    elif 'vibrant' in text :
        return 'Vibrant'
    elif text == 'nan' :
        return 'Vibrant'
    elif "cornflower"  in text:
        return "Cornflower"
    elif "pink"  in text:
        return "Pink"
    if "pigeon" in text:
        return "PigeonsBlood"
    else:
        return text
    
def detect_cut(cut):
    text = str(cut).lower()
    if "sugar loaf" in text :
        return "sugar loaf"
    elif "cabochon" in text:
        return "cab"
    else:
        return "cut"
    
def detect_shape(shape):
    shape = str(shape).lower()
    valid_shapes = [
        "cushion", "heart", "marquise", "octagonal", "oval",
        "pear", "rectangular", "round", "square", "triangular",
        "star", "sugarloaf", "tumbled"
    ]
    if shape in valid_shapes:
        return shape
    else:
        return "Others"
    
def detect_origin(origin):
    if not origin.strip():
        return "No origin"
    
    # Remove words in parentheses
    origin_without_parentheses = re.sub(r'\([^)]*\)', '', origin)
    if "Mozam" in origin_without_parentheses:
        return "Mozambique"
    return origin_without_parentheses.strip()

def reformat_issued_date(issued_date):
    try:
        # Create a datetime object from the date string
        parsed_date = datetime.strptime(issued_date, "%B %d, %Y")
        
        # Convert the datetime object to the desired format
        reformatted_date = parsed_date.strftime("%Y-%m-%d")
        
        return reformatted_date
    except ValueError:
        # Handle the case where the input date string is not in the expected format
        return ""
    
def detect_mogok(origin):
    return str("(Mogok, Myanmar)" in origin)

def generate_indication(comment):
    comment = str(comment).lower()
    if "no" in comment or 'te1' in comment:
        return "Unheated"
    else:
        return "Heated"
    
def detect_old_heat(comment, indication):
    if indication == "Heated":
        return comment
    else :
        comment = ''
        return comment

def generate_display_name(color, Color_1, origin, indication, comment):
    display_name = ""

    if color is not None:
        color = str(color).lower()  # Convert color to lowercase
        if indication == "Unheated":
            display_name = f"BELL({Color_1})"
        if indication == "Heated": 
            display_name = f"BELL({Color_1})(H)"
    
    if "(mogok, myanmar)" in str(origin).lower():  # Convert origin to lowercase for case-insensitive comparison
        display_name = "MG-" + display_name
    
    return display_name

# Define the function to extract the year and number from certNO
def extract_cert_info(df,certName):
    # Split the specified column into two columns
    df['certName'] = 'BELL'
    df['certNO'] = df[certName]
    return df

def convert_carat_to_numeric(value_with_unit):
    value_without_unit = value_with_unit.replace(" ct", "").replace(" et", "").replace(" ot", "")
    numeric_value = (value_without_unit)
    return numeric_value

def convert_dimension(dimension_str):
    parts = dimension_str.replace("—_", "").replace("_", "").replace("§", "5").replace(",", ".").replace("=", "").replace("mm", "").split(" x ")
    length = (parts[0])
    width = (parts[1])
    height = (parts[2])
    return length, width, height

def rename_identification_to_stone(dataframe):
    # Rename "Identification" to "Stone"
    dataframe.rename(columns={"Identification": "Stone"}, inplace=True)

    # Define a dictionary to handle stone names dynamically
    stone_name_modifications = {
        "RUBY": "Ruby",
        "SAPPHIRE": "Sapphire",
        "STAR RUBY": "Star Ruby",
        "CORUNDUM": "Corundum",
        "EMERALD": "Emerald",
        "PINK SAPPHIRE": "Pink Sapphire",
        "PURPLE SAPPHIRE": "Purple Sapphire",
        "SPINEL": "Spinel",
        "TSAVORITE": "Tsavorite",
        "BLUE SAPPHIRE": "Blue Sapphire",
        "FANCY SAPPHIRE": "Fancy Sapphire",
        "PERIDOT": "Peridot",
        "PADPARADSCHA": "Padparadscha"
    }

    # Remove unwanted words and trim spaces in the "Stone" column
    dataframe["Stone"] = dataframe["Stone"].str.replace("‘", "").str.strip()

    # Function to handle stone name modifications
    def modify_stone_name(name):
        modified_name = stone_name_modifications.get(name.upper(), name)
        return modified_name

    # Function to remove "Natural" or "Star" from the stone name
    def remove_prefix(name):
        for prefix in ["Natural", "Star", "Natura"]:
            name = name.replace(prefix, "").strip()
        return name

    # Function to get the last word if there are multiple words
    def get_last_word(name):
        words = name.split()
        if len(words) > 1:
            return words[-1]
        return name

    # Update the "Stone" column with dynamically modified names and the last word
    dataframe["Stone"] = dataframe["Stone"].apply(
        lambda x: modify_stone_name(remove_prefix(get_last_word(x)))
    )

    return dataframe

def detect_vibrant(Vibrant):
    Vibrant = str(Vibrant).lower() 
    return str("vibrant" in Vibrant)

def create_vibrant(row):
    def convert_color(color):
        if 'Vividred' in color:
            return 'VividRed'
        elif 'Vividpink' in color:
            return 'VividPink'
        return color
    
    if row['Vibrant'] == 'True' and row['Indication'] == 'Heated':
        modified_display_name = row['displayName'].replace('(H)','')
        modified_color = row['Color'].replace(' ', '')
        return f"{modified_display_name}({convert_color(modified_color)})(H)"
    elif row['Vibrant'] == 'True':
        modified_color = row['Color'].replace(' ', '')
        return f"{row['displayName']}({convert_color(modified_color)})"
    else:
        return row['displayName']

# Define the function to perform all data processing steps
def perform_data_processing(img):
    try:
        result_df = extract_gemstone_info(img)
    except Exception as e:
        result_df = extract_gemstone_info1(img)
    
    result_df["Detected_Origin"] = result_df["Origin"].apply(detect_origin)
    result_df["Detected_Origin"] = result_df["Detected_Origin"].str.replace('Ceylon','Sri Lanka').str.replace('Cevlon','Sri Lanka')
    result_df["Indication"] = result_df["indications"].apply(generate_indication)
    result_df["oldHeat"] = result_df.apply(lambda row: detect_old_heat(row["indications"], row["Indication"]), axis=1)
    
    if "Color0" in result_df and "Color" in result_df:
        result_df["Detected_Color"] = result_df.apply(lambda row: detect_color(row["Color0"]), axis=1)
        result_df['Vibrant'] = result_df["Detected_Color"].apply(detect_vibrant)
        result_df["displayName"] = result_df.apply(lambda row: generate_display_name(row["Color0"], row['Detected_Color'], row["Detected_Origin"], row['Indication'], row['oldHeat']), axis=1)
        result_df["displayName"] = result_df.apply(create_vibrant, axis=1)
    elif "Color" in result_df:
        result_df["Detected_Color"] = result_df.apply(lambda row: detect_color(row["Color"]), axis=1)
        result_df['Vibrant'] = result_df["Detected_Color"].apply(detect_vibrant)
        result_df["displayName"] = result_df.apply(lambda row: generate_display_name(row["Color"], row['Detected_Color'], row["Detected_Origin"], row['Indication'], row['oldHeat']), axis=1)
        result_df["displayName"] = result_df.apply(create_vibrant, axis=1)

    result_df["Detected_Cut"] = ''
    result_df["Detected_Shape"] = result_df["Shape"].apply(detect_shape)
    result_df["Reformatted_issuedDate"] = result_df["issuedDate"].apply(reformat_issued_date)
    result_df["Mogok"] = result_df["Origin"].apply(detect_mogok)
    result_df["Indication"] = result_df["indications"].apply(generate_indication)
    result_df = extract_cert_info(result_df, 'certNo')
    result_df['certNO'] = result_df['certNO'].str.replace(", ", "")
    result_df['certNO'] = result_df['certNO'].apply(lambda x: 'R' + x if x.startswith('-') and not x.startswith('R-') else x)
    result_df["carat"] = result_df["Carat"].apply(convert_carat_to_numeric)
    result_df[["length", "width", "height"]] = result_df["Dimensions"].apply(convert_dimension).apply(pd.Series)
    result_df = rename_identification_to_stone(result_df)


    result_df = result_df[[
    "certName",
    "certNO",
    "displayName",
    "Stone",
    "Detected_Color",
    "Detected_Origin",
    "Reformatted_issuedDate",
    "Indication",
    "oldHeat",
    "Mogok",
    "Vibrant",
    "Detected_Cut",
    "Detected_Shape",
    "carat",
    "length",
    "width",
    "height"
    ]]
    
    return result_df
# Specify the folder containing the images
# folder_path = r'C:\Users\kan43\Downloads\Cert Scraping Test'

# Specify the file pattern you want to filter
file_pattern = "-01_BELL"

# Create a Streamlit file uploader for the zip file
zip_file = st.file_uploader("Upload a ZIP file containing images", type=["zip"])

if zip_file is not None:
    # Extract the uploaded ZIP file
    with zipfile.ZipFile(zip_file) as zip_data:
        df_list = []

        for image_file in zip_data.namelist():
            if file_pattern in image_file:
                filename_without_suffix = image_file.split('-')[0]
                try:
                    # Read the image
                    with zip_data.open(image_file) as file:
                        img_data = io.BytesIO(file.read())
                        img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), 0)
                        
                        # Process the image and perform data processing
                        result_df = perform_data_processing(img)
    
                        result_df['StoneID'] = filename_without_suffix
                        result_df["StoneID"] = result_df["StoneID"].str.split("/")
                        # Get the last part of each split
                        result_df["StoneID"] = result_df["StoneID"].str.get(-1)
                        result_df['carat'] = result_df['carat'].astype(float)
                        result_df['carat'] = round(result_df['carat'], 2)
    
                        result_df = result_df[[
                            "certName",
                            "certNO",
                            "StoneID",
                            "displayName",
                            "Stone",
                            "Detected_Color",
                            "Detected_Origin",
                            "Reformatted_issuedDate",
                            "Indication",
                            "oldHeat",
                            "Mogok",
                            "Vibrant",
                            "Detected_Cut",
                            "Detected_Shape",
                            "carat",
                            "length",
                            "width",
                            "height",
                        ]]
                        result_df = result_df.rename(columns={
                            "Detected_Color": "Color",
                            "Detected_Origin": "Origin",
                            "Reformatted_issuedDate": "issuedDate",
                            "Detected_Cut": "Cut",
                            "Detected_Shape": "Shape"
                        })
    
                        # Append the DataFrame to the list
                        df_list.append(result_df)
                except Exception as e:
                    # Handle errors for this image, you can log or print the error message
                    st.error(f"Error processing image {image_file}: {str(e)}")
                    pass  # Skip to the next image

        # Concatenate all DataFrames into one large DataFrame
        final_df = pd.concat(df_list, ignore_index=True)

        # Display the final DataFrame
        st.write(final_df)


        csv_data = final_df.to_csv(index=False, float_format="%.2f").encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="Cert.csv",
            key="download-button"
        )

