# redirector

Python Flask application that provides redirects from one URL to another with different configurable options

# Description

Server written in Python using Flask which provides configurable address redirection.  This application reads from a configuration file which can be used to customize the following:

- Support email address for your page
- Page logo for your organization
- Redirect URLs and their settings
- User accounts to manage redirects

# To-Do's for the author

- Configure favicon - DONE
- Made log rolling - DONE
- Add logo size to config file - DONE
- Add IE check - DONE
- Add Status page - DONE
- Add user authentication to configuration page - DONE
- Have user authentication check to see if accounts are approved - DONE
- Hide passwords in log - DONE
- Add page to request a new login where it creates the account unapproved - DONE
- Add check when adding new user to make sure it does not already exist - DONE
- Add page to approve, unapprove and delete logins - DONE
- Add more user fields such as name and email and clean-up - DONE
- Hash passwords rather than encoding them - DONE
- First login is automatically approved - DONE
- Allow users to change their own password - DONE
- Session timeout for logins - DONE
- Move logo into header area instead of above it in all pages - DONE
- Rename about page to landing page - DONE
- Change login post redirect to go to landing page - DONE
- Work on what happens if the configuration file cannot be found - DONE
- Add redirect info to landing page - DONE
- Add navigation menu to each page - DONE
- Add DB check for redirects to provide response based on a field value - STARTED
- DB check setup so a SQL connection failure allows page to load - STARTED
- Tighten-up login security
- Add reorder arrows to config page
- Add grouping option to config page
- CSS clean-up for better responsiveness, remove deprecated HTML and move to CSS
- Fix problem where special characters stored in config crashes decode process
- Fix problem where user session is left logged in but is deleted from the config
- Split configuration and startup items from redirect items into separate logs
- Add prefix path checking that can direct to different targets for each configured redirect:
    Normal redirect: http://flaskserver:port/path/path -> http://someotherpath
    Prefix option: http://flaskserver:port/prefix/path/path -> http://somedifferentpathorport
- Test different configuration file write/read error scenarios

# License

[MIT License 2020](https://mit-license.org), [Bill Dykema](https://github.com/DykemaBill).

![redirector_screenshot](https://github.com/DykemaBill/redirector/blob/master/redirectorSS.png)