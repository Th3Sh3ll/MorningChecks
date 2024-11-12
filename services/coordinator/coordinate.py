from services.MSTeams.teamsPost import teamsPost
from services.SDPlus.logTicket import logTicketRequest
import json

# Coordination between services from receiving payload from frontEnd.
def coordinator(payload, teamsWebHook, serviceDeskDomain, serviceDeskAPIKey, session):
    print('Coordinator Started')
    emailAddres = session
    userAccount = session.split('@')[0].replace('.',' ').upper()
    print("Coordination completed extracting name and email address")

    print("Coordinator starting to log tickets and return count for teams summary post.")
    logTicketsResult  = logTicketRequest(payload, serviceDeskDomain, serviceDeskAPIKey, userAccount, emailAddres)
    print(f"OK checks: {logTicketsResult[0]}\nProblem Checks: {logTicketsResult[1]} ")

    print("Coordinator starting with teams post")
    msTeamsPostResult = teamsPost(payload, teamsWebHook, userAccount, logTicketsResult)
    print(f"Teams post complegted: {msTeamsPostResult}")

    return msTeamsPostResult, logTicketsResult
