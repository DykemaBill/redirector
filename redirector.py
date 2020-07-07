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
    logger.info(redirector_users)

# Create Flask app to build site
app = Flask(__name__)
# Add secret key since session requires it
app.secret_key = 'redirector session top secret'

# Run first before all route calls
@app.before_request
def before_request():
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
        user_guest = {"_index": 999999999999, "name": "guest", "password": "nopass"}
        if 'user_id' not in session:
            # Create guest login session
            session['user_id'] = user_guest['_index']
        # Set global variables for guest
        g.user = user_guest
        g.logo=redirector_logo
        g.logosize=redirector_logosize
        g.team=redirector_team
        g.email=redirector_email

# Root page about
@app.route('/')
def about():
    logger.info(request.remote_addr + ' ==> Root about page ')
    return render_template('about.html')

# Configuration page
@app.route('/config')
def config():
    logger.info(request.remote_addr + ' ==> Config page user ' + str(g.user['name']))
    if config_error == True:
        logger.info(request.remote_addr + ' ==> Config file read error ')
        return render_template('config_error.html', cfgfile=config_file)
    if session['user_id'] == 999999999999: # User is a guest
        return redirect(url_for('loginpage'))
    return render_template('config.html', redirect_records=dataread_records)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    if config_error == False:
        if request.method == 'POST':
            # Clear any previous login session
            session.pop('user_id', None)
            # Process login after form is filled out and a POST request happens
            user_request_name = request.form['user_login']
            user_request_pass = request.form['user_pass']
            # Look to see if this is a valid user
            user_check = [user_record for user_record in redirector_users if user_record['name'] == user_request_name]
            if not user_check:
                # Non-existent user name
                logger.info(request.remote_addr + ' ==> Login failed ' + user_request_name + ' does not exist')
                return render_template('login.html', logintitle="User does not exist, try again")
            else:
                # Password is stored encoded, decoding it
                password_decoded = b64decode(user_check[0]['password']).decode("utf-8")
                # Correct password
                if password_decoded == user_request_pass:
                    # Check to make sure user is approved
                    user_approved = [user_record for user_record in redirector_users if user_record['name'] == user_request_name and user_record['approved'] == True]
                    if not user_approved:
                        # Login successful, but user not approved
                        logger.info(request.remote_addr + ' ==> Login of ' + user_request_name + ' successful, but not approved')
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
                        logger.info(request.remote_addr + ' ==> Login of ' + user_request_name + ' successful')
                        return redirect(url_for('config'))
                else: # Incorrect password
                    logger.info(request.remote_addr + ' ==> Login failed ' + user_request_name + ' bad password')
                    return render_template('login.html', logintitle="Incorrect password, try again")
            # Login process failed all together
            logger.info(request.remote_addr + ' ==> Login failed ' + user_request_name + ' unknown reason')
            return render_template('login.html', logintitle="Login attempt failed, try again")
        else:
            # Show login page on initial GET request
            logger.info(request.remote_addr + ' ==> Login page ' + str(g.user['name']))
            return render_template('login.html', logintitle="Please login")
    else:
        return redirect(url_for('errorpage'))

# Logout page
@app.route('/logout')
def logoutpage():
    if config_error == False:
        logger.info(request.remote_addr + ' ==> Logout page ' + str(g.user['name']))
        # Clear login session
        session.pop('user_id', None)
        # Setup guest variables
        user_guest = {"_index": 999999999999, "name": "guest", "password": "nopass"}
        # Create guest login session
        session['user_id'] = user_guest['_index']
        # Set global variables for guest
        g.user = user_guest
        g.logo=redirector_logo
        g.logosize=redirector_logosize
        g.team=redirector_team
        g.email=redirector_email
        return render_template('login.html', logintitle="You have successfully logged out")

# Configuration save
@app.route('/save/<int:redirectindex>', methods=['POST'])
def save(redirectindex):
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
                    logger.info(str(g.user['name']) + ' updated redirect: ' + str(dataupdate_newrecord))
                else:
                    logger.info(str(g.user['name']) + ' deleted redirect: ' + str(dataupdate_newrecord))
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
        logger.info(str(g.user['name']) + ' added redirect: ' + str(dataupdate_newrecord))
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

# Maintenance template page
@app.route('/maint')
def maint():
    logger.info(request.remote_addr + ' ==> Maintenance page ')
    return render_template('maintenance.html')

# IE notice page
@app.route('/ienotice')
def ienotice():
    logger.info(request.remote_addr + ' ==> IE notice page ')
    return render_template('ienotice.html')

# Captures routes as defined in configuration file or if not deliver error page
@app.route('/<path:otherpath>')
def redirectfrom(otherpath):
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

# Status page
@app.route('/status')
def status():
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

# Run in debug mode if started from CLI
if __name__ == '__main__':
    app.run(debug=True)