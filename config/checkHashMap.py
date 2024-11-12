# Check Items to be added/removed , this will be displayed on home page and will also work in conjuction with the teams post.
# Labels are what will be shown for user experience instead of showing IDs
# ID's are used for backend processing from Javascript Ajax post, which looks for the ID's and posts the results to be processed.

def htmlHashMap():
    hashmap = [{
        "label" : "AZURE CONNECT",
        "id"    : "azureconnect"
    },{
        "label" : "DHCP:",
        "id"    : "dhcp"
    }, {
        "label" : "DC HEALTH:",
        "id"    : "dchealth"
    }, {
        "label" : "DIRTY DISKS:",
        "id"    : "dirtydisks"
    },{
        "label" : "SERVER HEALTH:",
        "id"    : "serverhealth"
    },{
        "label" : "CHECKPOINTS:",
        "id"    : "checkpoints"
    },{
        "label" : "DISK SPACE:",
        "id"    : "diskspace"
    },{
        "label" : "CSV's:",
        "id"    : "csvs"
    },{
        "label" : "EXCHANGE:",
        "id"    : "exchange"
    },{
        "label" : "REPLICATION:",
        "id"    : "replication"
    },{
        "label" : "CLUSTERS:",
        "id"    : "clusters"
    },{
        "label" : "STORAGEARRAYS:",
        "id"    : "storagearrays"
    },{
        "label" : "SQL:",
        "id"    : "sql"
    },{
        "label" : "DFS:",
        "id"    : "dfs"
    },{
        "label" : "BACKUPS DPM:",
        "id"    : "backupsdpm"
    },{
        "label" : "BACKUPS CV:",
        "id"    : "backupscv"
    },{
        "label" : "BACKUPS PRONTO:",
        "id"    : "prontobackups"
    },{
        "label" : "BOMGAR:",
        "id"    : "bomgar"
    }]
    return hashmap