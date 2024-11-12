# config for LDAP variables for authentication

def getLDAPinfo():
    # config for authentication
    ldapConfig = {
        'LDAP_SERVER'  : '',
        'LDAP_PORT'    : 636,
        'LDAP_BASE_DN' : '',
        'LDAP_USER_DN' : '',
        'LDAP_BIND_US' : "",
        'LDAP_BIND_PW' : ""
    }
    return ldapConfig