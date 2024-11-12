from flask import Flask, request, redirect, render_template, session, flash, jsonify
from ldap3 import Server, Connection, Tls, SUBTREE, SIMPLE, SCHEMA
from services.coordinator.coordinate import coordinator
from config.versioning import getVersion
from config.ldapConfig import getLDAPinfo
from config.checkHashMap import htmlHashMap
import ssl


app = Flask(__name__)
app.secret_key = '' # set this with a key for auth to be enabled: 637F25EE5230546546546
tls_config         = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)

# Configuration settings

# ServiceDesk
serviceDeskDomain = "" # Domain name of your service desk + URL
serviceDeskAPIKey = "" # API key of technician/service in SD+

# MSTeams webhook
teamsWebHook = '' # webhook URL to the MS teams channel

# auth user, this is on LDAPS, input required is email address to search for the user and grab the samaccountname from attributes
# pass the samaccount name with domain prefixed to second connection and then bind the connection
# if the bind is successful, pass to home route and confirm login with hello user in logs.
def authenticate_user(email, password):
    # pull ldap config
    ldapConfig = getLDAPinfo()
    try:
        server = Server(ldapConfig['LDAP_SERVER'], port=ldapConfig['LDAP_PORT'], use_ssl=True, get_info=SCHEMA)
        conn = Connection(server, user=ldapConfig['LDAP_BIND_US'], password=ldapConfig['LDAP_BIND_PW'], auto_bind=True, authentication=SIMPLE, check_names=True)
        search_filter = f'(mail={email})'
        conn.search(ldapConfig['LDAP_BASE_DN'], search_filter,  attributes=['sAMAccountName'], search_scope=SUBTREE)
        if conn.entries:
            user_dn = conn.entries[0].sAMAccountName
            user_conn = Connection(server, user=f"{ldapConfig['LDAP_USER_DN']}\\{user_dn}", password=password, auto_bind=True, authentication=SIMPLE, auto_referrals=True)
            if user_conn.bind():
                user_conn.unbind()
                return True
        conn.unbind()
        return False
    except Exception as e:
        print(f"Auth failed for {email} with ERROR: {e}")
        return False


# root page to login.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            session['user'] = email
            return redirect('/home')
        else:
            flash('Login failed. Please check your email and password.', 'error')
            return render_template('login.html')
    return render_template(
            'login.html',
            siteVersion = getVersion()
        )


# direct to home page after successful login.
@app.route('/home')
def home():
    if 'user' in session:
        print(f"Hello {session['user']}")
        checks = htmlHashMap()
        return render_template(
            'home.html',
            checkItems = checks,
            goodMorning = session['user'].split('.')[0]
        )
    else:
        return redirect('/')


@app.route('/catch', methods=['POST'])
def catch():
    payload = request.get_json()
    completed = coordinator(payload, teamsWebHook, serviceDeskDomain, serviceDeskAPIKey, session['user'])
    print(f"coordinator completed with: {completed}")
    ticketAssignedCheck = completed[1][3]
    if ticketAssignedCheck == True:
        ticketsAssignedResponse = completed[1][2]
    else:
        ticketsAssignedResponse = 'Not Applicable, no tickets were logged.'
    completedResponse = {
        "ticketsLogged"       : completed[1][1], # to select items from the tuple returned from coordinator
        "ticketsLoggedPassed" : completed[1][3],
        "ticketsAssignedTo"   : ticketsAssignedResponse,
        "teamsPostSentStatus" : completed[0]
    }
    return jsonify(
        completedResponse
    )


# logout page.
@app.route('/logout', methods=['POST'])
def logout():
    print(f"Logging out: {session['user']}")
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()