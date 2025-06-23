# MAD1-vehicle-parking-app-v1
## Description
- A parking lot management website created using HTML CSS and Flask For MAD1 (BSCS2003P) project.
- Made Responsive with Bootstrap-5

## Issues Encountered
### Milestone-VP DB-Relationship
- initializing db for each model causing inconsistency in the database instances. `Resolved`
- circular import issue where db was initiated in app and models import db from app, but app imports models. `Resolved`
- cannot delete Spot that is empty, but had been reserved in the past due to foreign key constraints in Reservations table `Resolved`

### Milestone-VP Auth-RBAC
- used different routes for GET and POST requests for login and signup form causing inconsistency while redirecting `Resolved`
- initially used `href='admin_signup.html'` which causes errors while rendered by flask. switched to runtime jinja templating to pass href values using `url_for` function `Resolved`

### Milestone-VP Admin-Dashboard-Management
- Reservations table didn't allow deletion of a spot that had been reserved in the past due to foreign key constraints `Resolved`
- Lot details being displayed where varying in size depending on number of spots in it. `Resolved`

### Milestone-VP User-Dashboard-Management
- forgot to add user_id in url for user's homepage `Resolved`
- loading reservation, users, lots, and spots for home page takes time. added joinedload `Resolved`
- joinedload syntax issues couldn't be resolved. used raw SQL query. `Resolved`
- calculation of Price in `user_reserve_confirm.html` for Milestone-VP Cost-Calculation `Resolved`

### Milestone-VP Summary-Users-Admin
- unable to accomodate reservation history for users in `/adminuser` (added new route `/adminhistory`) `Resolved`
- calculation of time parked in jinja templating leading to errors as datetime wasn't in context `Resolved`

### Milestone-VP Cost-Calculation
- displaying price as difference of leaving timee and parking time was challenging in jinja `Resolved`

### Milestone-VP Search-Implemented
- alignment issues `Resolved`

### Milestone-VP Charts
- jinja's `tojson` method converted `[]` to `'[]'` leading to empty list checks failing `Resolved`


