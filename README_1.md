# Lab 1 - Requirements Engineering & UML Use Case Modelling

Problem Statement 07: Hostel Maintenance & Issue Ticketing System  
PES University, Dept. of CSE

## Files

- `01_Requirements_Table.docx` - 5 functional and 2 non-functional requirements, plus a traceability table
- `02_UseCase_Diagram.pdf` - the use case diagram
- `03_UseCase_Flow.docx` / `.pdf` - flow for UC-01 Log Maintenance Ticket
- `hostel_maintenance_usecase.drawio` - editable draw.io source
- `usecase_diagram.png` - image version of the diagram

## Actors

- Hostel Resident - raises tickets and signs off once the repair is done
- Maintenance Staff - works on assigned tickets and updates status
- Maintenance Warden - assigns staff and keeps an eye on SLA
- Notification Service - supporting actor, sends the SMS/email alerts

## Use Cases

| ID | Use Case |
|---|---|
| UC-01 | Log Maintenance Ticket |
| UC-02 | Review Resolution & Signoff |
| UC-03 | Assign Maintenance Staff |
| UC-04 | Track SLA |
| UC-05 | View Ticket History |
| UC-06 | Update Ticket Status |

Two extra use cases are used for the stereotypes:

- `<<include>>` Validate Ticket Details - always runs when UC-01 runs
- `<<extend>>` Send Escalation Alert - only runs when a high-priority ticket crosses 24 hours

## Opening the diagram

Go to app.diagrams.net, then File > Open From > Device and pick the `.drawio` file.
Export with File > Export as > PDF.
