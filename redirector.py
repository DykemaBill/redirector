# Default user password of Ch@ng3MEN0w! encoded as Q2hAbmczTUVOMHch in config file

from flask import Flask, g, render_template, json, redirect, url_for, request, session
import logging, logging.handlers, time, platform, sys
from base64 import b64encode, b64decode

# Configuration file name
config_name = 'redirector'
config_file = config_name + '.cfg'

# Set default configuration variables
redirector_team = "needtosetteamname"
redirector_email = "needtosetinconfig@nowhere.com"
redirector_logo = "needtosetinconfig"
redirector_logosize = [ 100, 100 ] # This is width and height
redirector_logfilesize = [ 10000, 9 ] # 10000 is 10k, 9 is 10 total copies
redirector_redirects = []
redirector_users = []
user_session = "Not logged in"

# Class to read JSON configuration file
class RedirectJSONtoArray:
    def __init__(self, _index, redirectfrom, redirectto, embed, maintenance):
        self._index = _index
        self.redirectfrom = redirectfrom
        self.redirectto = redirectto
        self.embed = embed
        self.maintenance = maintenance

# Read configuration file for redirects
config_error = False
dataread_records = []
def config_file_read():
    dataread_records.clear()
    try:
        with open(config_file, 'r') as json_file:
            cfg_data = json.loads(json_file.read())
            global redirector_logfilesize
            global redirector_logo
            global redirector_logosize
            global redirector_team
            global redirector_email
            global redirector_redirects
            global redirector_users
            redirector_logfilesize.clear()
            redirector_logfilesize.append(cfg_data['logfilesize'][0])
            redirector_logfilesize.append(cfg_data['logfilesize'][1])
            redirector_logo = cfg_data['logo']
            redirector_logosize.clear()
            redirector_logosize.append(cfg_data['logosize'][0])
            redirector_logosize.append(cfg_data['logosize'][1])
            redirector_team = cfg_data['team']
            redirector_email = cfg_data['email']
            redirector_redirects.clear()
            for dataread_record in cfg_data['redirects']:
                dataread_records.append(RedirectJSONtoArray(**dataread_record))
                redirector_redirects.append(dataread_record)
            redirector_users.clear()
            for dataread_user in cfg_data['users']:
                redirector_users.append(dataread_user)
    except IOError:
        print('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
        global config_error
        config_error = True

# Read configuration file
config_file_read()

# Set log name
log_file = 'redirector.log'
# Start logger with desired output level
logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)
# Setup log handler to manage size and total copies
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=redirector_logfilesize[0], backupCount=redirector_logfilesize[1])
# Setup formatter to prefix each entry with date/time 
formatter = logging.Formatter("%(asctime)s - %(message)s")
# Add formatter
handler.setFormatter(formatter)
# Add handler
logger.addHandler(handler)

# Starting up
logger.info('****====****====****====****====****==== Starting up ====****====****====****====****====****')

# Config file status
if config_error == True:
    print ("Unable to read config")
    logger.info('Problem opening ' + config_file + '.cfg, check to make sure your configuration file is not missing.')
else: # Config settings out to the log
    print ("Configuration file read")
    logger.info('Log file size is set to ' + str(redirector_logfilesize[0]) + ' bytes and ' + str(redirector_logfilesize[1]) + ' copies')
    logger.info('Email is set to: ' + redirector_email)
    logger.info('Team is set to: ' + redirector_team)
    logger.info('Logo is set to: ' + redirector_logo)
    logger.info('Logo size is set to: ' + str(redirector_logosize[0]) + ', ' + str(redirector_logosize[1]))
    logger.info('Redirects loaded as follows:')
    logger.info(redirector_redirects)
    logger.info('Users are as follows:')
    # Write user info to log without encoded passwords
    redirect_users_log = []
    for user_record in redirector_users:
        redirect_users_record = {}
        redirect_users_record['_index'] = user_record['_index']
        redirect_users_record['approved'] = user_record['approved']
        redirect_users_record['login'] = user_record['login']
        redirect_users_record['password'] = "*******"
        redirect_users_record['namelast'] = user_record['namelast']
        redirect_users_record['namefirst'] = user_record['namefirst']
        redirect_users_record['email'] = user_record['email']
        redirect_users_log.append(redirect_users_record)
    logger.info(redirect_users_log)

# Create Flask app to build site
app = Flask(__name__)
# Add secret key since session requires it
app.secret_key = 'redirector session top secret'

# Run first before all route calls
@app.before_request
def before_request():
    global config_error
    if config_error == False:
        # Check to see if the end user already has an existing session
        if 'user_id' in session and session['user_id'] != 999999999999: # User session exists and it is not a guest
            # Find the user ID
            user_session = [user_record for user_record in redirector_users if user_record['_index'] == session['user_id']][0]
            # Set global variables for user
            g.user = user_session
            g.logo=redirector_logo
            g.logosize=redirector_logosize
            g.team=redirector_team
            g.email=redirector_email
        else: # User is a new or existing guest
            # Setup guest variables
            user_guest = {"_index": 999999999999, "login": "guest", "password": "nopass"}
            if 'user_id' not in session:
                # Create guest login session
                session['user_id'] = user_guest['_index']
            # Set global variables for guest
            g.user = user_guest
            g.logo=redirector_logo
            g.logosize=redirector_logosize
            g.team=redirector_team
            g.email=redirector_email
    else:
        return redirect(url_for('errorpage'))

# Root page about
@app.route('/')
def about():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Root about page ')
        return render_template('about.html')
    else:
        return redirect(url_for('errorpage'))

# Configuration page
@app.route('/config')
def config():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Config page user ' + str(g.user['login']))
        if config_error == True:
            logger.info(request.remote_addr + ' ==> Config file read error ')
            return render_template('config_error.html', cfgfile=config_file)
        if session['user_id'] == 999999999999: # User is a guest
            return redirect(url_for('loginpage'))
        return render_template('config.html', redirect_records=dataread_records)
    else:
        return redirect(url_for('errorpage'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    global config_error
    if config_error == False:
        if request.method == 'POST':
            # Clear any previous login session
            session.pop('user_id', None)
            # Process login after form is filled out and a POST request happens
            user_request_login = request.form['user_login']
            user_request_pass = request.form['user_pass']
            # Look to see if this is a valid user
            user_check = [user_record for user_record in redirector_users if user_record['login'] == user_request_login]
            if not user_check:
                # Non-existent user login
                logger.info(request.remote_addr + ' ==> Login failed ' + user_request_login + ' does not exist')
                return render_template('login.html', logintitle="User does not exist, try again")
            else:
                # Password is stored encoded, decoding it
                password_decoded = b64decode(user_check[0]['password']).decode("utf-8")
                # Correct password
                if password_decoded == user_request_pass:
                    # Check to make sure user is approved
                    user_approved = [user_record for user_record in redirector_users if user_record['login'] == user_request_login and user_record['approved'] == True]
                    if not user_approved:
                        # Login successful, but user not approved
                        logger.info(request.remote_addr + ' ==> Login of ' + user_request_login + ' successful, but not approved')
                        return render_template('login.html', logintitle="Login successful, but not approved, check with your administrator")
                    else:
                        # Set session to logged in user
                        session['user_id'] = user_check[0]['_index']
                        # Set global variables for user
                        g.user = user_check[0]
                        g.logo=redirector_logo
                        g.logosize=redirector_logosize
                        g.team=redirector_team
                        g.email=redirector_email
                        # Redirect sucessfully logged in user to configuration page
                        logger.info(request.remote_addr + ' ==> Login of ' + user_request_login + ' successful')
                        return redirect(url_for('config'))
                else: # Incorrect password
                    logger.info(request.remote_addr + ' ==> Login failed ' + user_request_login + ' bad password')
                    return render_template('login.html', logintitle="Incorrect password, try again")
            # Login process failed all together
            logger.info(request.remote_addr + ' ==> Login failed ' + user_request_login + ' unknown reason')
            return render_template('login.html', logintitle="Login attempt failed, try again")
        else:
            # Show login page on initial GET request
            logger.info(request.remote_addr + ' ==> Login page ' + str(g.user['login']))
            return render_template('login.html', logintitle="Please login")
    else:
        return redirect(url_for('errorpage'))

# Logout page
@app.route('/logout')
def logoutpage():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Logout page ' + str(g.user['login']))
        # Clear login session
        session.pop('user_id', None)
        # Setup guest variables
        user_guest = {"_index": 999999999999, "login": "guest", "password": "nopass"}
        # Create guest login session
        session['user_id'] = user_guest['_index']
        # Set global variables for guest
        g.user = user_guest
        g.logo=redirector_logo
        g.logosize=redirector_logosize
        g.team=redirector_team
        g.email=redirector_email
        return render_template('login.html', logintitle="You have successfully logged out")

# Login create page
@app.route('/loginnew', methods=['GET', 'POST'])
def loginnewpage():
    global config_error
    if config_error == False:
        if request.method == 'POST':
            # Process new login after form is filled out and a POST request happens
            user_request_login = request.form['user_login']
            user_request_pass = request.form['user_pass']
            user_request_namelast = request.form['user_namelast']
            user_request_namefirst = request.form['user_namefirst']
            user_request_email = request.form['user_email']

            logger.info(request.remote_addr + ' ==> Login create request ' + user_request_login + ", " + user_request_namefirst + " " + user_request_namelast + ", " + user_request_email)
            
            # Look to see if a user with the same login already exists
            user_check = [user_record for user_record in redirector_users if user_record['login'] == user_request_login]
            if user_check:
                # Login is already in use
                logger.info(request.remote_addr + ' ==> Login name ' + user_request_login + ' already exists')
                return render_template('loginnew.html', logintitle="Login name not available, try again")
            else: # Login not in use already
                # Find index to use for new user
                user_last = redirector_users[-1]
                user_last_index = user_last['_index']
                user_index = user_last_index + 1

                # Encode password
                user_passencoded_byte = b64encode(user_request_pass.encode("utf-8"))
                user_passencoded = user_passencoded_byte.decode("utf-8")

                # Write the new user for the config file
                dataupdate_newuser = {
                    "_index": user_index,
                    "approved": False,
                    "login": user_request_login,
                    "password": user_passencoded,
                    "namelast": user_request_namelast,
                    "namefirst": user_request_namefirst,
                    "email": user_request_email
                }

                # Read entire configuration file so that it can be updated
                try:
                    with open(config_file, 'r') as json_file:
                        dataupdate_json = json.load(json_file)
                except IOError:
                    print('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
                    logger.info('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
                    config_error = True

                # Create backup of configuration file
                datetime = time.strftime("%Y-%m-%d_%H%M%S")
                try:
                    with open(config_name + '_' + datetime + '_old.cfg', 'w') as json_file:
                        json.dump(dataupdate_json, json_file, indent=4)
                except IOError:
                    print('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
                    logger.info('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
                    config_error = True

                # Add new user
                redirector_users.append(dataupdate_newuser)

                # Assemble updated configuration file
                configupdate_jsonedit = {'email': redirector_email, 'logfilesize': redirector_logfilesize, 'logo': redirector_logo, 'logosize': redirector_logosize, 'team': redirector_team, 'redirects': redirector_redirects, 'users': redirector_users}

                # Write updated configuration file
                try:
                    with open(config_file, 'w') as json_file:
                        json.dump(configupdate_jsonedit, json_file, indent=4)
                except IOError:
                    print('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
                    logger.info('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
                    config_error = True

                # Write user info to log without encoded password
                dataupdate_newuser_log = {
                    "_index": user_index,
                    "approved": False,
                    "login": user_request_login,
                    "password": "*******",
                    "namelast": user_request_namelast,
                    "namefirst": user_request_namefirst,
                    "email": user_request_email
                }

                logger.info('Added user: ' + str(dataupdate_newuser_log))

                # Let new user know they are added but not approved
                return render_template('login.html', logintitle="New user " + user_request_login + " added, but not approved!")
        else:
            # Show login create page on initial GET request
            logger.info(request.remote_addr + ' ==> Login create page ' + str(g.user['login']))
            # Clear login session
            session.pop('user_id', None)
            # Setup guest variables
            user_guest = {"_index": 999999999999, "login": "guest", "password": "nopass"}
            # Create guest login session
            session['user_id'] = user_guest['_index']
            # Set global variables for guest
            g.user = user_guest
            g.logo=redirector_logo
            g.logosize=redirector_logosize
            g.team=redirector_team
            g.email=redirector_email
            return render_template('loginnew.html', logintitle="Create a new login")
    else:
        return redirect(url_for('errorpage'))

# Configuration save
@app.route('/save/<int:redirectindex>', methods=['POST'])
def save(redirectindex):
    global config_error
    if config_error == False:
        # Read new redirect from address
        redirectfromSave = request.form['redirectSourceInput']
        # Read new redirect to address
        redirecttoSave = request.form['redirectTargetInput']
        # Embed need try for checkbox to catch exception when it has no value
        try:
            request.form['redirectTargetEmbed']
            embedSave = True
        except:
            embedSave = False
        # Maintenance need try for checkbox to catch exception when it has no value
        try:
            request.form['redirectTargetMaint']
            maintenanceSave = True
        except:
            maintenanceSave = False

        # Write the new record for the config file
        dataupdate_newrecord = {
            "_index": redirectindex,
            "redirectfrom" : redirectfromSave,
            "redirectto" : redirecttoSave,
            "embed" : embedSave,
            "maintenance" : maintenanceSave
        }

        # Read entire configuration file so that it can be updated
        try:
            with open(config_file, 'r') as json_file:
                dataupdate_json = json.load(json_file)
        except IOError:
            print('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
            logger.info('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
            config_error = True

        # Create backup of configuration file
        datetime = time.strftime("%Y-%m-%d_%H%M%S")
        try:
            with open(config_name + '_' + datetime + '_old.cfg', 'w') as json_file:
                json.dump(dataupdate_json, json_file, indent=4)
        except IOError:
            print('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
            logger.info('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
            config_error = True

        # Replace updated record, add new record or delete record
        dataupdate_jsonedit = []
        if redirectindex < len(dataread_records): # Not adding new record
            for dataupdate_existingrecord in dataupdate_json['redirects']:
                # Add all records until we come to the one that was modified
                if dataupdate_existingrecord['_index'] < redirectindex:
                    dataupdate_jsonedit.append(dataupdate_existingrecord)
                # This is the modified record
                elif dataupdate_existingrecord['_index'] == redirectindex:
                    # Check to see if we should replace it or delete/ignore it
                    if request.form['submit'] == 'save':
                        dataupdate_jsonedit.append(dataupdate_newrecord)
                        logger.info(str(g.user['login']) + ' updated redirect: ' + str(dataupdate_newrecord))
                    else:
                        logger.info(str(g.user['login']) + ' deleted redirect: ' + str(dataupdate_newrecord))
                # This is after the modified record
                # If we saved the modified record, save the rest like normal
                elif request.form['submit'] == 'save':
                    dataupdate_jsonedit.append(dataupdate_existingrecord)
                else: # Since we deleted the record, reduce the index
                    curren_index = dataupdate_existingrecord['_index']
                    dataupdate_existingrecord.update({"_index": curren_index-1})
                    dataupdate_jsonedit.append(dataupdate_existingrecord)
        else: # We are just adding a new record
            dataupdate_jsonedit = dataupdate_json['redirects']
            logger.info(str(g.user['login']) + ' added redirect: ' + str(dataupdate_newrecord))
            dataupdate_jsonedit.append(dataupdate_newrecord)

        # Assemble updated configuration file
        configupdate_jsonedit = {'email': redirector_email, 'logfilesize': redirector_logfilesize, 'logo': redirector_logo, 'logosize': redirector_logosize, 'team': redirector_team, 'redirects': dataupdate_jsonedit, 'users': redirector_users}

        # Write updated configuration file
        try:
            with open(config_file, 'w') as json_file:
                json.dump(configupdate_jsonedit, json_file, indent=4)
        except IOError:
            print('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
            logger.info('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
            config_error = True

        # Reload configuration page
        config_file_read()
        return redirect(url_for('config'))
    
    else:
        return redirect(url_for('errorpage'))

# Login management save
@app.route('/loginmanage', methods=['GET', 'POST'])
def loginmanage():
    global config_error
    if config_error == False:
        if session['user_id'] == 999999999999: # User is a guest
            return redirect(url_for('loginpage'))
        else:
            if request.method == 'POST':
                # Read user index
                user_index = request.form['user_index']
                user_index = int(user_index)
                # Read user login
                user_login = request.form['user_login']
                # Read user last name
                user_namelast = request.form['user_namelast']
                # Read user first name
                user_namefirst = request.form['user_namefirst']
                # Read user email address
                user_email = request.form['user_email']
                # Approved need try for checkbox to catch exception when it has no value
                try:
                    request.form['user_approved']
                    user_approved = True
                except:
                    user_approved = False

                # Look for user being modified
                for user_record in redirector_users:
                    if int(user_record['_index']) == int(user_index):
                        user_info = user_record

                # Use stored password for user
                user_passencoded = user_info['password']

                # Write the login information for the config file
                dataupdate_userchanged = {
                    "_index": user_index,
                    "approved": user_approved,
                    "login": user_login,
                    "password": user_passencoded,
                    "namelast": user_namelast,
                    "namefirst": user_namefirst,
                    "email": user_email
                }

                # Write the login information for the log file
                dataupdate_login_log = {
                    "_index": user_index,
                    "approved": user_approved,
                    "login": user_login,
                    "password": "*******",
                    "namelast": user_namelast,
                    "namefirst": user_namefirst,
                    "email": user_email
                }

                # Read entire configuration file so that it can be updated
                try:
                    with open(config_file, 'r') as json_file:
                        dataupdate_json = json.load(json_file)
                except IOError:
                    print('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
                    logger.info('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
                    config_error = True

                # Create backup of configuration file
                datetime = time.strftime("%Y-%m-%d_%H%M%S")
                try:
                    with open(config_name + '_' + datetime + '_old.cfg', 'w') as json_file:
                        json.dump(dataupdate_json, json_file, indent=4)
                except IOError:
                    print('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
                    logger.info('Problem creating to ' + config_file + '_' + datetime + ', check to make sure your filesystem is not write protected.')
                    config_error = True

                # Replace updated login, or delete login
                dataupdate_jsonedit = []
                for dataupdate_existinglogin in dataupdate_json['users']:
                    # Add all logins until we come to the one that was modified
                    if int(dataupdate_existinglogin['_index']) < int(user_index):
                        dataupdate_jsonedit.append(dataupdate_existinglogin)
                    # This is the modified login
                    elif int(dataupdate_existinglogin['_index']) == int(user_index):
                        # Check to see if we should replace it or delete/ignore it
                        if request.form['submit'] == 'save':
                            dataupdate_jsonedit.append(dataupdate_userchanged)
                            logger.info(str(g.user['login']) + ' modified login: ' + str(dataupdate_login_log))
                        else:
                            logger.info(str(g.user['login']) + ' deleted login: ' + str(dataupdate_login_log))
                    # This is after the modified login
                    # If we saved the modified login, save the rest like normal
                    elif request.form['submit'] == 'save':
                        dataupdate_jsonedit.append(dataupdate_existinglogin)
                    else: # Since we deleted the login, reduce the index
                        curren_index = dataupdate_existinglogin['_index']
                        dataupdate_existinglogin.update({"_index": curren_index-1})
                        dataupdate_jsonedit.append(dataupdate_existinglogin)

                # Assemble updated configuration file
                configupdate_jsonedit = {'email': redirector_email, 'logfilesize': redirector_logfilesize, 'logo': redirector_logo, 'logosize': redirector_logosize, 'team': redirector_team, 'redirects': redirector_redirects, 'users': dataupdate_jsonedit}

                # Write updated configuration file
                try:
                    with open(config_file, 'w') as json_file:
                        json.dump(configupdate_jsonedit, json_file, indent=4)
                except IOError:
                    print('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
                    logger.info('Problem writing to ' + config_file + ', check to make sure your configuration file is not write protected.')
                    config_error = True

                # Reload configuration page
                config_file_read()
                return redirect(url_for('loginmanage'))

            else:
                # Show login management page on initial GET request
                logger.info(request.remote_addr + ' ==> Login management page ' + str(g.user['login']))
                return render_template('loginmanage.html', login_records=redirector_users)
    
    else:
        return redirect(url_for('errorpage'))

# Maintenance template page
@app.route('/maint')
def maint():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Maintenance page ')
        return render_template('maintenance.html')
    else:
        return redirect(url_for('errorpage'))

# IE notice page
@app.route('/ienotice')
def ienotice():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> IE notice page ')
        return render_template('ienotice.html')
    else:
        return redirect(url_for('errorpage'))

# Captures routes as defined in configuration file or if not deliver error page
@app.route('/<path:otherpath>')
def redirectfrom(otherpath):
    global config_error
    if config_error == False:
        for redirect_route in dataread_records:
            # Check to see if otherpath equals one of the redirect_route.redirectfrom configured paths
            if otherpath == redirect_route.redirectfrom:
                if redirect_route.maintenance:
                    logger.info(request.remote_addr + ' ==> Maintenance: ' + redirect_route.redirectto)
                    return redirect(url_for('maint'))
                else:
                    if redirect_route.embed:
                        logger.info(request.remote_addr + ' ==> Embedded: ' + redirect_route.redirectto)
                        return render_template('redirect.html', redirectto=redirect_route.redirectto) # If the target allows opening the site in an iFrame
                    else:
                        logger.info(request.remote_addr + ' ==> Direct: ' + redirect_route.redirectto)
                        return redirect(redirect_route.redirectto, code=302) # Use this just to redirect to the site
        logger.info(request.remote_addr + ' ==> Bad path page ' + otherpath)
        return render_template('error.html', bad_path=otherpath)
    else:
        return redirect(url_for('errorpage'))

# Status page
@app.route('/status')
def status():
    global config_error
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Status page ')
        running_python = sys.version.split('\n')
        running_host = platform.node()
        running_os = platform.system()
        running_hardware = platform.machine()
        try:
            with open(config_file, 'r') as text_file:
                config_data = text_file.read()
        except IOError:
            print('Problem opening ' + config_file + ', check to make sure your configuration file is not missing.')
            config_data = "Unable to read config file " + config_file
        try:
            with open(log_file, 'r') as logging_file:
                log_data = logging_file.read()
        except IOError:
            print('Problem opening ' + log_file + ', check to make sure your log file location is valid.')
            log_data = "Unable to read log file " + log_file
        return render_template('status.html', running_python=running_python, running_host=running_host, running_os=running_os, running_hardware=running_hardware, config_data=config_data, log_data=log_data)
    else:
        return redirect(url_for('errorpage'))

# Run in debug mode if started from CLI
if __name__ == '__main__':
    app.run(debug=True)