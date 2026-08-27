# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Course:** Software Engineering Lab  
**University:** PES University – Dept. of CSE  
**Problem Statement:** #07 – Hostel Maintenance & Issue Ticketing System  

---

## Overview

This lab involved converting the functional requirements from Lab 1 into an Agile backlog using Jira. We created Epics and User Stories, assigned story points, ran two sprints, and analysed progress using the Burndown Chart.

---

## Project Setup

- **Tool Used:** Jira (Company-managed, Scrum template)
- **Project Name:** Hostel-Ticketing
- **Board:** HT board

---

## Epics Created

| Epic ID | Epic Name | Priority |
|---------|-----------|----------|
| HT-1 | Ticket Submission & Reporting | High |
| HT-2 | Warden Dashboard & Dispatch | High |
| HT-3 | SLA Monitoring & Escalation | High |
| HT-4 | Resident Closure & Feedback | Medium |
| HT-5 | Reporting & Analytics | Low |

---

## User Stories

| Story ID | Title | Epic | Priority | Story Points |
|----------|-------|------|----------|--------------|
| HT-6 | Story 1.1: Submit Maintenance Ticket | HT-1 | High | 5 |
| HT-7 | Story 1.2: Select Issue Category | HT-1 | High | 3 |
| HT-8 | Story 1.3: Receive Unique Ticket ID | HT-1 | High | 2 |
| HT-9 | Story 1.4: View Ticket Status | HT-1 | Medium | 3 |
| HT-10 | Story 2.1: View Prioritised Ticket Queue | HT-2 | High | 5 |
| HT-11 | Story 2.2: Assign Staff to Ticket | HT-2 | High | 3 |
| HT-12 | Story 2.3: Update Ticket Status | HT-2 | High | 3 |
| HT-13 | Story 2.4: Geo-Tagged Room Map | HT-2 | Medium | 8 |
| HT-14 | Story 3.1: SLA Breach Alert | HT-3 | High | 5 |
| HT-15 | Story 3.2: View SLA Breach Report | HT-3 | Medium | 5 |
| HT-16 | Story 4.1: Digital Closure Sign-Off | HT-4 | Medium | 3 |
| HT-17 | Story 4.2: Rate Maintenance Quality | HT-4 | Low | 2 |
| HT-18 | Story 5.1: Monthly Ticket Report | HT-5 | Low | 5 |
| HT-19 | Story 5.2: Export Ticket Data as CSV | HT-5 | Low | 3 |

---

## Sprint Summary

### Sprint 1 – HT Sprint 1
- **Duration:** 1 week
- **Goal:** Complete core ticket submission and warden dispatch pipeline
- **Stories:** HT-6, HT-7, HT-8, HT-10, HT-11, HT-12, HT-14
- **Total Story Points:** 26
- **Status:** Completed

### Sprint 2 – HT Sprint 2
- **Duration:** 1 week
- **Goal:** Complete resident feedback and SLA reporting features
- **Stories:** HT-9, HT-13, HT-15, HT-16, HT-17
- **Total Story Points:** 21
- **Status:** Completed

---

## Burndown Charts

- Burndown charts were generated from **Reports > Burndown Chart** in Jira
- Both sprints showed completion of all stories within the sprint window
- Charts are included in the lab submission PDF

---

## Reflection

1. **Did your estimations reflect the actual effort?**  
   Mostly yes. Simpler stories were completed quickly and complex ones like the geo-tagged map (8 points) took more thought as expected.

2. **Was your backlog well-prioritized?**  
   Yes. High priority stories covering the core pipeline were placed in Sprint 1. Medium and Low priority features were deferred to Sprint 2.

3. **How did your simulated sprint align with your plan?**  
   Both sprints completed all selected stories. The Scrum board made it easy to track progress across To Do → In Progress → Done.

4. **What insights did the burndown chart give about your team's capacity?**  
   Team velocity was approximately 26 points (Sprint 1) and 21 points (Sprint 2), giving a good baseline for future sprint planning.

---

## Deliverables

- [x] Jira Backlog with Epics and User Stories
- [x] Story Point assignments
- [x] Sprint board screenshots (Active Sprint view)
- [x] Burndown Charts for Sprint 1 and Sprint 2
- [x] Reflection document (PDF)
- [x] Live Jira workspace demonstrated to instructor
