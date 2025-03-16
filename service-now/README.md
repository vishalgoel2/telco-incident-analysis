## Prompt

Create a simplified version of a ServiceNow-like incident management tool in React + TypeScript with the following requirements:
1. Two views:
   * List View: Displays a list/table of incidents with columns for incident ID, description, and status (open/in-progress/closed).
   * Details View: Shows additional details such as actions taken, resolution, and RCA. Include basic styling for the UIs.
2. List view:
   * Clicking on an incident ID opens the details view for that incident, and the URL updates to include the incident ID.
   * Include a "New Incident" button that opens a dialog to input the description and actions taken, along with a submit button.
   * Add a search box and sorting functionality if easily achievable. Consider using an out-of-the-box table or list component.
3. Details view:
   * If the status is "open," display only the incident ID, description, actions taken, and status.
   * If the status is "closed," additionally display the RCA and resolution.
   * If the status is "in progress," show the RCA and resolution along with buttons to accept or edit.
   * Clicking the edit button makes the RCA and resolution fields editable with text areas and provides options to save or cancel.
4. APIs (using FastAPI in Python):
   * `GET /incidents`: Retrieve all incidents including all details.
   * `POST /incidents`: Insert a new incident with description and actions taken (ID auto-generated).
   * `PUT /incidents`: Update RCA and resolution.
5. Database:
   * Use SQLite to support the APIs.
   * Table name: `INCIDENT`.
   * Columns: `id` (auto-generated), `description` (text, not null), `actions_taken` (text, not null), `rca` (text), `resolution` (text), `status` (OPEN|IN_PROGRESS|CLOSED).