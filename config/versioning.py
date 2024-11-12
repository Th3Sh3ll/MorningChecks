# versioning file to keep track of changes and push version to login page

def getVersion():
    MorningChecksVersion = "3.6"
    '''
        #### Versioning ####
        ver1:   simple radio button checklist to post to teams.
        ver2:   Converted radion buttons to check boxes.
                Enabled Authentication to grab email accounts to bind to a check
                Logged ticket to Servicedkes.
                Teams post with summary of checks.
        ver3:   Enabled image pasting into notes section for screenshots to be uploaded.
                Updated logticket to embed screenshot into ticket
                Ticket now logged straight to technician that is logged in by using email address
                Teams post updated to include screenshot from frontEnd into post.
                Teams post now has a summary of total OK checks and total Problem checks.
                Teams post split into problem and summary posts, summary will contain all checks and their result, problem post will only happen if there is a problem.
                Ticket logging is now only for problems found, including screenshot and logging directly to technician(person doing the checks.)
                Improved how checks are managed to frontend by creating a hashmap in coordinator to easily allow removal and additions to frontEnd.
        ver3.1: Refactored SDPlus service when logging tickets to a for loop for each image logged, this will handle each screenshot attached to a single check 
                Javascript also had to be updated from storing only images to storing images and specific notes.
        ver3.2: MSteams function updated to handle image and subsequent conversion.
                Excluded single post to teams, only including summary as screenshots are in the tickets logged and also cleaning up the string payload by removing html tags such as div and br
        ver3.3: Updated authentication on LDAPS to AD, search for email address, bring back samaccount name attribute and bind with domain\\samaccount. 
        ver3.4: Patched logticket code to handle no notes added to the problem section and only a screenshot, this would error out because the regex to remove any divs would fail
                as there are no divs to remove, moved this into an if condition, if notes are empty add "no notes added" to list so it can still index the screenshot added.
                Added additional check: AZURE AD CONNECT, tested and confirmed working.
        ver3.5: Cosmetic updates done to HTML and CSS, version moved to login page with new look header.  Added counters for TO DO and DONE and made the counter stick when scrolling.
                New header and moved to the left.  Logged In user changed to Hello User |.
                Changed the order of checks as well to align more with solar winds.
        ver3.6: Cleaned up code and moved functions for configuration to config folder to be imported to main.
                Improved hashmap for user convertion to what SD+ expects , this allows for quicker lookup instead of using a for loop and if condition.
                Moved ldap configuration from main to own module in config folder.
                Moved check items hashmap from main to own module in config folder.
                Moved versioning from main to own module in config folder.
                Cleaned up MS teams code and removed none used functions.  
    '''
    return MorningChecksVersion