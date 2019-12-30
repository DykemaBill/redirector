from flask import Flask, render_template, json, jsonify, redirect, request, url_for, request
import logging

# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='redirector.log')

# Configuration file name
config_file = 'config'

# Class to read JSON configuration file
class JSONRead:
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
        with open(config_file + '.json', 'r') as json_file:
            json_data = json.loads(json_file.read())
            global redirector_logo
            global redirector_team
            global redirector_email
            redirector_logo = json_data['logo']
            redirector_team = json_data['team']
            redirector_email = json_data['email']
            for dataread_record in json_data['redirects']:
                dataread_records.append(JSONRead(**dataread_record))
    except IOError:
        print ('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        global config_error
        config_error = True

config_file_read()

# Create Flask app to build site
app = Flask(__name__)

# Root page about
@app.route('/')
def about():
    return render_template('about.html', logo=redirector_logo, team=redirector_team, email=redirector_email)

# Configuration page
@app.route('/config')
def config():
    if config_error == True:
        return render_template('config_error.html', cfgfile=config_file + '.json', logo=redirector_logo, team=redirector_team, email=redirector_email)
    return render_template('config.html', redirect_records=dataread_records, logo=redirector_logo, team=redirector_team, email=redirector_email)

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
    
    print('New path from is ' + redirectfromSave + ' going to ' + redirecttoSave)

    # Read new configuration values into array for page - NEED TO APPEND THE FOLLOWING WHEN NEW RECORD
    if redirectindex < len(dataread_records): # Not adding new record
        print ('Not adding a new record')
        dataread_records[redirectindex].redirectfrom = redirectfromSave
        dataread_records[redirectindex].redirectto = redirecttoSave
        dataread_records[redirectindex].embed = embedSave
        dataread_records[redirectindex].maintenance = maintenanceSave
    else: # We are addding a new record
        print ('We are adding a new record')
        dataread_records[redirectindex].redirectfrom = redirectfromSave
        dataread_records[redirectindex].redirectto = redirecttoSave
        dataread_records[redirectindex].embed = embedSave
        dataread_records[redirectindex].maintenance = maintenanceSave

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
        with open(config_file + '.json', 'r') as json_file:
            dataupdate_json = json.load(json_file)
    except IOError:
        print ('Problem opening ' + config_file + '.json, check to make sure your configuration file is not missing.')
        config_error = True

    # Create backup of configuration file
    try:
        with open(config_file + '_old.json', 'w') as json_file:
            json.dump(dataupdate_json, json_file, indent=4)
    except IOError:
        print ('Problem creating to ' + config_file + '_old.json, check to make sure your filesystem is not write protected.')
        config_error = True

    # Replace updated record or add new record
    dataupdate_jsonedit = []
    for dataupdate_existingrecord in dataupdate_json['redirects']:
        if redirectindex < len(dataread_records): # Not adding new record
            if dataupdate_existingrecord['_index'] == redirectindex:
                dataupdate_jsonedit.append(dataupdate_newrecord)
            else:
                dataupdate_jsonedit.append(dataupdate_existingrecord)
        else: # We are addding a new record
            dataupdate_jsonedit = dataupdate_json['redirects']
            dataupdate_jsonedit.append(dataupdate_newrecord)

    # Assemble updated configuration file
    configupdate_jsonedit = {'email': redirector_email, 'logo': redirector_logo, 'team': redirector_team, 'redirects': dataupdate_jsonedit}

    # Write updated configuration file
    try:
        with open(config_file + '.json', 'w') as json_file:
            json.dump(configupdate_jsonedit, json_file, indent=4)
    except IOError:
        print ('Problem writing to ' + config_file + '.json, check to make sure your configuration file is not write protected.')
        config_error = True

    # Reload configuration page
    config_file_read()
    return redirect(url_for('config'))

# Maintenance template page
@app.route('/maint')
def maint():
    return render_template('maintenance.html', logo=redirector_logo, team=redirector_team, email=redirector_email)

# Captures routes as defined in configuration file or if not deliver error page
@app.route('/<path:otherpath>')
def redirectfrom(otherpath):
    for redirect_route in dataread_records:
        # Check to see if otherpath equals one of the redirect_route.redirectfrom configured paths
        if otherpath == redirect_route.redirectfrom:
            if redirect_route.maintenance:
                logging.info(request.remote_addr + ' ==> maintenance: ' + redirect_route.redirectto)
                return redirect(url_for('maint'))
            else:
                if redirect_route.embed:
                    logging.info(request.remote_addr + ' ==> embedded: ' + redirect_route.redirectto)
                    return render_template('redirect.html', redirectto=redirect_route.redirectto) # If the target allows opening the site in an iFrame
                else:
                    logging.info(request.remote_addr + ' ==> direct: ' + redirect_route.redirectto)
                    return redirect(redirect_route.redirectto, code=302) # Use this just to redirect to the site
    return render_template('error.html', bad_path=otherpath, logo=redirector_logo, team=redirector_team, email=redirector_email)

# Run in debug mode if started from CLI
if __name__ == '__main__':
    app.run(debug=True)