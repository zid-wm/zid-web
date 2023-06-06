# Changelog
The vZID ARTCC website code uses a calendar versioning system, with YY.M(M).PATCH as the standard format.
## v23.6.1
### Features
- Notification is sent to ATM/DATM/WM when a new visit request is submitted.
### Bug Fixes
- Fix login redirect URL constructor
- Fix display of visit requests for staff members
## v23.6.0
### Features
- Added "Become a Visitor" option to navbar when user is not logged in. Visitor request form prompts for VATSIM login prior to submission.
### Bug Fixes
- Fixed parsing of controller logon date/time which would occasionally lead to sessions not being logged properly
- Removed log entry when user logs in
## v23.5.1
### Bug Fixes
- Fixed staff comment submission form redirecting to the wrong URL
## v23.5.0
### Features
- Files page is now available to all website visitors (does not require login)
- Added the ability to display assistant staff roles (editable directly on user's profile by staff members)
- Make event banners clickable on the events page
- Staff comments can now be added to user profiles. Visible to ATM, DATM, TA, and WM. Comments can only be deleted by the original author.
### Bug Fixes
- Fix display of file names containing a forward slash (/)
- MAVP roster pull no longer throws error when a controller has rating <=1 and is not already in the database
- Event delete no longer throws ObjectNotFoundError when attempting to add action log entry
- Event times are more obviously shown in Zulu time
- Staff members editing another user's profile are no longer redirected to their own profile after making changes
### Other Notes
- Uploaded files currently require the uploader to attach the file extension to the description in order for the downloaded file to include this extension. We plan to switch from S3 to a local model storage for uploaded files to fix this issue.
- Event titles no longer display on the main events page. Title and edit/delete links are now located on the event details page.
## v23.1.0
Initial Release