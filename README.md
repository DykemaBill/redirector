# Redirector

Python Flask server that redirects visitors to other web page URLs.

Lots still to-do:

- Rename about page to landing page
- Configure favicon
- Add prefix path checking that can direct to different targets for each configured redirect:
    Normal redirect: http://flaskserver:port/path/path -> http://someotherpath
    Prefix option: http://flaskserver:port/prefix/path/path -> http://somedifferentpathorport
- Add user authentication to configuration page
- Add redirect links list to landing page
- Split configuration and startup items from redirect items into separate logs
- Add reorder arrows to config page
- Add grouping option to config page
- Add navigation bar
- CSS clean-up for better responsiveness
- Test different configuration file write/read error scenarios