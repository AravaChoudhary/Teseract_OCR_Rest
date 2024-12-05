import pytesseract
import cv2
import PIL
import re
import json

# Define configuration for pytesseract
my_config = r"--psm 6 --oem 3"

# Function to extract referral code
def extract_referral_code(image_path):
    text = pytesseract.image_to_string(PIL.Image.open(image_path), config=my_config)
    match = re.search(r"Amber_\d+", text)
    if match:
        return {"Referral Code": match.group()}
    return {"Referral Code": "Not found"}

# Function to extract accepted date and student name
def extract_student_info(image_path):
    text = pytesseract.image_to_string(PIL.Image.open(image_path), config=my_config)
    data = {}

    date_match = re.search(r"Accepted on:\s*(\d{2}/\d{2}/\d{4})", text)
    if date_match:
        data["Accepted Date"] = date_match.group(1)

    name_match = re.search(r"Name of student:\s*(.*)", text)
    if name_match:
        data["Student Name"] = name_match.group(1).strip()

    return data if data else {"Accepted Date": "Not found", "Student Name": "Not found"}

# Function to extract accommodation details
def extract_accommodation_details(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
    denoised_image = cv2.fastNlMeansDenoising(threshold_image, None, 30, 7, 21)
    data = pytesseract.image_to_string(denoised_image, config=my_config)

    extracted_data = {}

    contract_length_match = re.search(r"Contract\s*Length\s*(?:.*\s*)?(\d+\s*weeks)", data)
    if contract_length_match:
        extracted_data["Contract Length"] = contract_length_match.group(1).strip()

    arriving_date_match = re.search(r"Arriving\s+Departing\s+(\d{1,2}\s\w+\s\d{4})\s+(\d{1,2}\s\w+\s\d{4})", data)
    if arriving_date_match:
        extracted_data["Arriving Date"] = arriving_date_match.group(1).strip()

    departing_date_match = re.search(r"23 September 2024\s+(\d{1,2}\s\w+\s\d{4})", data)
    if departing_date_match:
        extracted_data["Departing Date"] = departing_date_match.group(1).strip()

    total_cost_match = re.search(r"Total cost of the accommodation\s+£([\d,\.]+)", data)
    if total_cost_match:
        extracted_data["Total Cost of Accommodation"] = total_cost_match.group(1).strip()

    return extracted_data if extracted_data else {"Contract Length": "Not found", "Arriving Date": "Not found", "Departing Date": "Not found", "Total Cost of Accommodation": "Not found"}

# Function to extract booking ID
def extract_booking_id(image_path):
    text = pytesseract.image_to_string(PIL.Image.open(image_path), config=my_config)
    match = re.search(r"\$T\s*(\d+)", text)

    if match:
        return {"Booking ID": match.group(0).strip()}
    return {"Booking ID": "Not found"}

# Function to extract email and account password
def extract_credentials(image_path):
    text = pytesseract.image_to_string(PIL.Image.open(image_path), config=my_config)
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    password_pattern = r"Account Password:\s*(\S+)"

    extracted_cred = {}

    email_match = re.search(email_pattern, text)
    if email_match:
        extracted_cred["Username"] = email_match.group(0)

    password_match = re.search(password_pattern, text)
    if password_match:
        extracted_cred["Account Password"] = password_match.group(1)

    return extracted_cred if extracted_cred else {"Username": "Not found", "Account Password": "Not found"}

# Main function to process images and save the extracted data into a JSON file
def main():
    extracted_info = {}

    # Process each image and extract data
    extracted_info.update(extract_referral_code("812115.png"))
    extracted_info.update(extract_student_info("812101.png"))
    extracted_info.update(extract_accommodation_details("812102.png"))
    extracted_info.update(extract_booking_id("812103.png"))
    extracted_info.update(extract_credentials("812117.png"))

    # Save the extracted data as a JSON file
    with open("2531747.json", "w") as json_file:
        json.dump(extracted_info, json_file, indent=4)

    # Print the extracted data to console
    print(json.dumps(extracted_info, indent=4))

# Run the main function
if __name__ == "__main__":
    main()
