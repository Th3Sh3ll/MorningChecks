import pymsteams
from config.checkHashMap import htmlHashMap
from PIL import Image


# function to return colord style for reults in teams post
def returnColorCodedResponse(result):
    if 'OK' in result:
        return f"<span style='color:Lime'>OK</span>"
    else:
        return f"<span style='color:yellow'>Problem</span>"


# function to return colored number based off threshold set, if OK is low then yellow else green and if NotOK is high then yellow else green
def returnColorBasedOffThreshold(count, checkState):
    if checkState == 'OK':
        if count > 10:
            colorCodedResult = f"<span style='color:Lime'>{count}</span>"
        else:
            colorCodedResult = f"<span style='color:yellow'>{count}</span>"
    if checkState == 'PROBLEM':
        if 3 > count:
            colorCodedResult = f"<span style='color:Lime'>{count}</span>"
        else:
            colorCodedResult = f"<span style='color:yellow'>{count}</span>"
    return colorCodedResult


# import the hasmap as a labelcheck to properly convert ID to LABEL for the teams post.
def convertToLabelNameForFacts(check):
    for id in htmlHashMap():
        if check in id['id']:
            return id['label']


def teamsPost(payload, teamsWebHook, userAccount, logTicketsResult):
    # build card and title
    teamsPostBuild = pymsteams.connectorcard(teamsWebHook)
    teamsPostBuild.title(f"Morning Checks | Completed by: {logTicketsResult[2]}")
    teamsPostBuild.color("DBF3C9")
    teamsPostBuild.text(f"PROBLEMS: {returnColorBasedOffThreshold(logTicketsResult[1], "PROBLEM")}<br>CHECKS GOOD: {returnColorBasedOffThreshold(logTicketsResult[0], "OK")}")

    # build message section
    health_checks = pymsteams.cardsection()
    
    # summary post
    for eachCheck in payload.items():
        if eachCheck[1]['notes']:
            # Clean up the notes field by replacing unwanted HTML tags
            cleaned_notes = eachCheck[1]['notes'].replace('<div>', '').replace('</div>', '').replace('<br>', ' ')
            
            # Format the result and cleaned notes into a single string
            payloadFact = f"{returnColorCodedResponse(eachCheck[1]['result'])}: {cleaned_notes}"
            
            # Add the fact with the formatted string
            health_checks.addFact(
                f"{convertToLabelNameForFacts(eachCheck[0])}", 
                payloadFact
            )
        else:
            # If no notes are present, just add the result
            health_checks.addFact(convertToLabelNameForFacts(eachCheck[0]), f"{returnColorCodedResponse(eachCheck[1]['result'])}")

    # add facts to 1 section
    teamsPostBuild.addSection(health_checks)
    # send
    teamsPostResult = teamsPostBuild.send()
    if teamsPostResult == True:
        return teamsPostResult
    else:
        teamsPostResult = False
        print(f"TeamsPost error: {teamsPostResult}")
    return teamsPostResult
