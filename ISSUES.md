
## Issues Encountered
### Milestone-VP DB-Relationship
- Initializing `db` for each model using an independent database instances leads to unsynchronized data access.  `Resolved`
- Circular import issue where `db` was initiated in `app.py` and `models.py` import `db` from `app.py`, but `app.py` imports `models.py`. `Resolved`
- Could not delete a Spot that was empty but had been reserved in the past due to foreign key constraints in the Reservations table. `Resolved`

### Milestone-VP Auth-RBAC
- Used different routes for GET and POST requests for login and signup forms causing inconsistency while redirecting. `Resolved`
- Initially used `href='admin_signup.html'` which caused errors while being rendered by flask. Switched to runtime jinja templating to pass `href` values using `url_for` function. `Resolved`

### Milestone-VP Admin-Dashboard-Management
- Reservations table didn't allow deletion of a spot that had been reserved in the past due to foreign key constraints. `Resolved`
- Lot details being displayed varied in size depending on the number of spots in it. `Resolved`

### Milestone-VP User-Dashboard-Management
- Forgot to add `user_id` in url for the user's homepage. `Resolved`
- Loading reservations, users, lots, and spots for home page was inefficient (lazy loading each lot); added joinedload. `Resolved`
- Joinedload syntax issues couldn't be resolved; switched to raw SQL query. `Resolved`
- Calculation of price in `user_reserve_confirm.html` for Milestone-VP Cost-Calculation. `Resolved`

### Milestone-VP Summary-Users-Admin
- Unable to accommodate reservation history for users in `/adminuser` (added new route `/adminhistory`). `Resolved`
- Calculation of time parked in Jinja templating leading to errors as datetime wasn't in context. `Resolved`

### Milestone-VP Cost-Calculation
- Calculating duration as difference of leaving time and parking time was challenging in Jinja. `Resolved`

### Milestone-VP Search-Implemented
- Alignment issues. `Resolved`

### Milestone-VP Charts
- Jinja's `tojson` method converted `[]` to `'[]'`, leading to empty list checks failing. `Resolved`

### Milestone-VP Responsive-UI
- No issues faced as used Bootstrap styling was used from beginning of project.

### Milestone-VP Final-Submission
- Cleaned up code, fixed minor bugs.
