import pytesseract
from PIL import Image

# Define functions for each task
def referral_code(data):
    """Extract referral code from OCR data."""
    text = data['text']
    for line in text.split('\n'):
        if "Referral Code" in line:
            return line.split(':')[-1].strip()
    return "Referral code not found."

def booking_completion(data):
    """Extract booking completion status from OCR data."""
    text = data['text']
    if "Booking Complete" in text:
        return "Booking is complete."
    return "Booking is not complete."

def booking_id(data):
    """Extract booking ID from OCR data."""
    text = data['text']
    for line in text.split('\n'):
        if "Booking ID" in line:
            return line.split(':')[-1].strip()
    return "Booking ID not found."

def email_proof(data):
    """Extract email information from OCR data."""
    text = data['text']
    for line in text.split('\n'):
        if "@" in line and ".com" in line:
            return line.strip()
    return "Email proof not found."

def tenancy_details(data):
    """Extract tenancy details from OCR data."""
    text = data['text']
    for line in text.split('\n'):
        if "Tenancy" in line:
            return line.strip()
    return "Tenancy details not found."

def booking_and_tenancy(data):
    """Extract both booking and tenancy details."""
    booking = booking_id(data)
    tenancy = tenancy_details(data)
    return {
        "Booking": booking,
        "Tenancy": tenancy
    }

def new_task(data):
    """Placeholder for a new task."""
    return "New task processing not implemented yet."

# Mapping of task names to functions
task_functions = {
    "referral_code": referral_code,
    "booking_completion": booking_completion,
    "booking_id": booking_id,
    "email_proof": email_proof,
    "tenancy_details": tenancy_details,
    "booking_and_tenancy": booking_and_tenancy,
    "new_task": new_task
}

def process_image(task_name, image_path):
    """Process an image using the specified task."""
    if task_name not in task_functions:
        raise ValueError(f"Task '{task_name}' is not recognized.")

    # Open the image and perform OCR
    image = Image.open(image_path)
    ocr_data = {
        "text": pytesseract.image_to_string(image)
    }

    # Call the appropriate function
    return task_functions[task_name](ocr_data)

if __name__ == "__main__":
    # List of tasks with their respective image paths
    tasks = [
        {"task": "referral_code", "image": "referral_image.png"},
        {"task": "booking_completion", "image": "booking_completion_image.png"},
        {"task": "booking_id", "image": "814594.png"},
        {"task": "email_proof", "image": "email_image.png"},
        {"task": "tenancy_details", "image": "tenancy_image.png"},
        {"task": "booking_and_tenancy", "image": "combined_image.png"},
        {"task": "new_task", "image": "new_task_image.png"}
    ]

    # Process each task
    results = {}
    for task in tasks:
        task_name = task["task"]
        image_path = task["image"]
        print(f"Processing task: {task_name} with image: {image_path}")
        try:
            result = process_image(task_name, image_path)
            results[task_name] = result
        except Exception as e:
            results[task_name] = str(e)

    # Print results
    for task_name, result in results.items():
        print(f"\nTask: {task_name}\nResult: {result}")
