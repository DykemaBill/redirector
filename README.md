# Redirector

Python Flask server that redirects visitors to other web page URLs.

Lots still to-do:

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
- Add redirect links list to landing page
- Tighten-up login security
- Add DB check for redirects to provide a different response based on a field value
- Add reorder arrows to config page
- Add grouping option to config page
- Add navigation bar
- CSS clean-up for better responsiveness, remove deprecated HTML and move to CSS
- Fix problem where special characters stored in config crashes decode process
- Fix problem where user session is left logged in but is deleted from the config
- Split configuration and startup items from redirect items into separate logs
- Add prefix path checking that can direct to different targets for each configured redirect:
    Normal redirect: http://flaskserver:port/path/path -> http://someotherpath
    Prefix option: http://flaskserver:port/prefix/path/path -> http://somedifferentpathorport
- Test different configuration file write/read error scenarios