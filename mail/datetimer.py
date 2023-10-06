from datetime import datetime

# Get the current date
current_date = datetime.now().date()

# Format the date as a string in the desired format (e.g., 17/04/2004)
formatted_date = current_date.strftime("%d/%m/%Y")

# Print the formatted date
print(formatted_date)
