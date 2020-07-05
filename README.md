# Redirector

Python Flask server that redirects visitors to other web page URLs.

Lots still to-do:

- Configure favicon - DONE
- Made log rolling - DONE
- Add logo size to config file - DONE
- Add IE check - DONE
- Add Status page - DONE
- Rename about page to landing page
- Add redirect links list to landing page
- Add user authentication to configuration page
- Work on what happens if the configuration file cannot be found
- Add DB check for each redirect to provide a different response based on a field value
- Add reorder arrows to config page
- Add grouping option to config page
- Add navigation bar
- CSS clean-up for better responsiveness, remove deprecated HTML and move to CSS
- Split configuration and startup items from redirect items into separate logs
- Add prefix path checking that can direct to different targets for each configured redirect:
    Normal redirect: http://flaskserver:port/path/path -> http://someotherpath
    Prefix option: http://flaskserver:port/prefix/path/path -> http://somedifferentpathorport
- Test different configuration file write/read error scenarios