import requests
import json
import base64
import os
import re
from datetime import datetime
from flask import current_app, url_for

# function to pass what SD expects to assign tickets to technicians.
# The names are split and converted to upper to avoid any casing issues when username is typed in logon.
# Names are then passed to this hashmap to return the value matching the key "NAME" will return "NAME SURNAME" which is what is expected by service desk plus.
def checkNameForTicketAssignment(userAccount):
    convertedUser = {
        'NAME 1'   : 'Surname 1',
        'NAME 2'   : 'Surname 2'
    }
    return convertedUser[userAccount]


# log tickets to SD+
def logTicketRequest(payload, serviceDeskDomain, serviceDeskAPIKey, userAccount, emailAddres):

    # Convert username to the full name SD+ expects
    userAccountConverted = checkNameForTicketAssignment(userAccount.split(' ')[0])
    
    print(f"Conversion result: {userAccount} converted to: {userAccountConverted}")

    headers = {
        'Content-Type'  : 'application/json',
        'technician_key': serviceDeskAPIKey
    }
    
    checksOK = 0
    checksNotOK = 0 
    ticketLoggedStatus = False
    
    # Process each ticket in the payload
    for ticket in payload.items():
        headliner = ticket[0]
        
        description = f"{headliner.upper()} Completed with {ticket[1]['result'][0]}<br><br>"
        # imagesArray = []

        # Only log tickets if there is a 'PROBLEM'
        if 'PROBLEM' in ticket[1]['result']:
            print(f"Ticket found and will log: {headliner}")
            checksNotOK += 1

            # Get notes and images
            notes_list = ticket[1].get('notes', '')
            # create a new list to hold only items filtering out empty entries
            newListToUse = []
            if notes_list:
                # Clean the notes by removing unwanted HTML tags using regex
                # This removes any <div>, </div>, and <br> tags.
                cleaned_notes = re.sub(r'</?div>', '', notes_list)
                # Split cleaned notes into list if needed, using another separator
                notes_list = cleaned_notes.split('<br>')  # Ensure the split logic is correct
                
                for item in notes_list:
                    if item == '':
                        continue
                    else:
                        newListToUse.append(item)
            else:
                print(f"No notes added, nothing to clean.")
                newListToUse.append('No notes added<br>')

            images_list = ticket[1].get('image', [])

            # remove empty list items after split
            # Process notes and images, interleaving them in the description
            for index, note in enumerate(newListToUse):
                description += f"{note}<br>"

                # Ensure that images_list is always a list
                if images_list is None:
                    images_list = []

                # Process images if available
                if index < len(images_list):
                    # print(f"Checking images list: {images_list}")
                    imgBase64 = images_list[index].replace('data:image/png;base64,', '')
                    imageData = base64.b64decode(imgBase64)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
                    screenShotFileName = f"screenshot_{headliner}_{timestamp}.png"
                    static_folder = os.path.join(current_app.root_path, 'static', 'uploads', f"{screenShotFileName}")

                    with open(static_folder, 'wb') as f:
                        f.write(imageData)

                    # imagesArray.append(screenShotFileName)
                    image_url = url_for('static', filename=f'uploads/{screenShotFileName}', _external=True)
                    description += f"<img src='{image_url}' alt='Screenshot' /><br><br>"
            
            # Append user info at the end
            description += f"<br>Logged by: {userAccountConverted}"

            # Prepare the request payload with interleaved notes and images
            request = {
                "request": {
                    "subject"      : f"Morning Check: {headliner.upper()} | Status: {ticket[1]['result'][0]}",
                    "description"  : description,
                    "urgency"      : {"name": "3. LOW"},
                    "requester"    : {"name": "Morning Checks", "email_id": "emal@address.com"},
                    "status"       : {"name": "Open"},
                    "category"     : {"name": "Server Management"},
                    "subcategory"  : {"name": "Daily Checks"},
                    "priority"     : {"name": "P4 - LOW"},
                    "group"        : {"name": "L3 - Server Engineering"},
                    "resolution"   : {"content": None},
                    "impact"       : {"name": "4. LOW - Individual Impacted"},
                    "site"         : {"name": "Region", "id": "19502"},
                    "udf_fields"   : {
                        "udf_pick_2425" : "No",
                        "udf_pick_2103" : "CITY"
                    },
                    "technician"   : {"email_id": f"{emailAddres}", "name": f"{userAccountConverted}"}
                }
            }

            data = {"input_data": json.dumps(request)}
            
            # Log the ticket only once, outside of the notes/images loop
            print(f"Logging ticket for: {ticket[0]}")
            response = requests.post(url=f"http://{serviceDeskDomain}/api/v3/requests", headers=headers, params=data)
            
            if response.status_code == 201:
                print("Ticket created successfully!")
                ticketLoggedStatus = True
            else:
                print(f"Failed to create ticket: {response.status_code} - {response.text}")
                print(f"Ticket payload\n{json.dumps(data, indent=2)}")
        else:
            checksOK += 1  # If no problem, just count the OK checks
            continue
    
    if not ticketLoggedStatus:
        ticketLoggedStatus = 'All checks OK, no tickets logged, enjoy your day further'
    
    return checksOK, checksNotOK, userAccountConverted, ticketLoggedStatus