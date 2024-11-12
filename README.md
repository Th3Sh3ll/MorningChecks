# MorningChecks
Checklist for infrastructure systems to be checked "morning checks"

# About the app
**What is it**

A simple check list with checkboxes for any sort of checks that need to be completed.

**What can it do**

It allows you to add notes as well as screen shots.

It can post a summary of the checks to a teams channel you specify by webhook.

It can also log a ticket to service desk plus.  The ticket will include the notes as well as the screenshots.

# How to configure and run
**Update main.py**

app.secret_key - add your secret key (generate one.)

**Update ldapConfig.py | Thiss will allow you to auth**

Domain controller server name.

LDAP_BASE_DN = DC=contoso,DC=com (root of your domain distinguished name.)

LDAP_USER_DN = domain prefix contoso which is **CONOTSO**\username (This is misleading, i know, sorry.)

LDAP_BIND_US = The user/service account to bind with into AD (use the distinguished name of the account.)

LDAP_BIND_PW = Password of the user/service account you configured LDAP_BIND_US with.

**Update checkHashMap.py**

Here you can update the dictionary that will be used for all check items you need, add/remove in one place.

**Versioning | versioning.py**

Keep updated with anything you add etc.. Also displays on the site.

**RUN**

Copy all files into a folder on your linux server with docker-compose installed.

Run: docker-compose up --build -d
