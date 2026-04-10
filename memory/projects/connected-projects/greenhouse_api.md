# Greenhouse API Reference

## Overview
Greenhouse provides 3 APIs: **Harvest API** (admin), **Job Board API** (public), and **Webhooks** (events).

## Credentials
See `greenhouse-api` skill (`SKILL.md`) for sandbox tokens and login credentials — single source of truth.

## Harvest API (Main API)
- **Base URL**: `https://harvest.greenhouse.io/v1/`
- **Auth**: Basic Auth over HTTPS (API token as username, blank password)
- **Rate Limits**: Per 10-second windows, `X-RateLimit-Limit` / `X-RateLimit-Remaining` headers
- **Pagination**: `Link` header (RFC-5988), default 100/page, max 500. Params: `page`, `per_page`, `skip_count`

### Endpoints by Category

#### Applications (KEY for Connected Projects)
- `GET /applications` — List all applications
- `GET /applications/{id}` — Get application
- `DELETE /applications/{id}` — Delete application
- `POST /candidates/{id}/applications` — Add application
- `PATCH /applications/{id}` — Update application
- `POST /applications/{id}/advance` — Move to NEXT stage
- `POST /applications/{id}/move` — Move to SPECIFIC stage (same job)
- `POST /applications/{id}/transfer_to_job` — Move to different job
- `PATCH /applications/{id}/convert_prospect` — Convert prospect to candidate
- `POST /applications/{id}/hire` — Hire
- `POST /applications/{id}/reject` — Reject
- `PATCH /applications/{id}/reject` — Update rejection reason
- `POST /applications/{id}/unreject` — Unreject
- `POST /applications/{id}/attachments` — Add attachment

#### Job Stages (KEY for Connected Projects)
- `GET /job_stages` — List ALL job stages
- `GET /jobs/{id}/stages` — Stages for specific job
- `GET /job_stages/{id}` — Get single stage
- **NOTE**: Greenhouse does NOT support creating new stages via API

#### Candidates
- `GET /candidates` — List candidates
- `GET /candidates/{id}` — Get candidate
- `POST /candidates` — Create candidate
- `PATCH /candidates/{id}` — Edit candidate
- `DELETE /candidates/{id}` — Delete candidate
- `POST /candidates/{id}/notes` — Add note
- `POST /candidates/{id}/email_notes` — Add email note
- `POST /candidates/{id}/attachments` — Add attachment
- `POST /candidates/{id}/educations` — Add education
- `POST /candidates/{id}/employments` — Add employment
- `POST /candidates/{id}/prospect` — Add as prospect
- `PUT /candidates/{id}/anonymize` — Anonymize (GDPR)
- `PUT /candidates/merge` — Merge candidates
- `GET /candidates/{id}/activity_feed` — Activity feed

#### Jobs
- `GET /jobs` — List jobs
- `GET /jobs/{id}` — Get job
- `POST /jobs` — Create job
- `PATCH /jobs/{id}` — Update job
- `GET /jobs/{id}/hiring_team` — Get hiring team
- `PUT /jobs/{id}/hiring_team` — Replace hiring team
- `POST /jobs/{id}/hiring_team` — Add team members

#### Offers
- `GET /offers` — List offers
- `GET /applications/{id}/offers` — Offers for application
- `GET /applications/{id}/offers/current` — Current offer
- `PATCH /offers/{id}` — Update offer

#### Scorecards
- `GET /scorecards` — List scorecards
- `GET /applications/{id}/scorecards` — For application
- `GET /scorecards/{id}` — Get scorecard

#### Scheduled Interviews
- `GET /scheduled_interviews` — List interviews
- `GET /applications/{id}/scheduled_interviews` — For application
- `POST /scheduled_interviews` — Create interview
- `PATCH /scheduled_interviews/{id}` — Update
- `DELETE /scheduled_interviews/{id}` — Delete

#### Users
- `GET /users` — List users
- `GET /users/{id}` — Get user
- `POST /users` — Create user
- `PATCH /users/{id}` — Edit user
- `PATCH /users/{id}/disable` — Disable
- `PATCH /users/{id}/enable` — Enable

#### Other Resources
- **Departments**: CRUD at `/departments`
- **Offices**: CRUD at `/offices`
- **Sources**: `GET /sources`
- **Rejection Reasons**: `GET /rejection_reasons`
- **Close Reasons**: `GET /close_reasons`
- **Email Templates**: `GET /email_templates`
- **Custom Fields**: CRUD at `/custom_fields`
- **Tags**: CRUD at `/candidate_tags`, manage on candidates
- **Job Posts**: CRUD at `/job_posts`
- **Job Openings**: CRUD at `/openings`
- **Approvals**: CRUD at `/approvals`
- **Prospect Pools**: `GET /prospect_pools`
- **EEOC**: `GET /eeoc`, `GET /applications/{id}/eeoc`
- **Demographic Data**: Questions, answers, options at `/demographic_*`
- **Education Reference**: `/degrees`, `/disciplines`, `/schools`

### HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Unauthorized (bad API key) |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation error |
| 429 | Rate limited |
| 500 | Server error |

## Job Board API (Public)
- **Base URL**: `https://boards-api.greenhouse.io/v1/boards/{board_token}/`
- **Auth**: GET = none (public), POST = Basic Auth
- **Key Endpoints**:
  - `GET /jobs` — List job posts
  - `GET /jobs/{id}` — Job with application questions
  - `POST /jobs/{id}` — Submit application
  - `GET /offices`, `GET /departments` — Org structure
  - `GET /education/degrees|disciplines|schools` — Education data

## Webhooks
- **Auth**: HMAC-SHA256 signature verification via secret key
- **Retry**: Up to 7 retries over ~15 hours (1m, 15m, 60m, 120m, 240m, 480m)
- **Tracking**: `Greenhouse-Event-ID` header for deduplication

### Webhook Event Types
- **Application**: new_candidate_application, application_updated, application_deleted
- **Candidate**: candidate_stage_change, candidate_hired/unhired, candidate_rejected/unrejected, candidate_updated, candidate_deleted, candidate_merged, candidate_anonymized
- **Offer**: offer_created/updated/deleted/approved
- **Interview**: interview_deleted, scorecard_deleted
- **Job**: job_created/updated/deleted, job_approved, job_post_created/updated/deleted, job_stage_deleted
- **Organization**: department_deleted, office_deleted
- **Prospect**: prospect_created

### Key Webhook: candidate_stage_change
Most relevant for Connected Projects — fires when application moves between stages. Payload includes application ID, candidate ID, job info, and new stage details.

## Connected Projects Relevance
- **Stage sync**: `GET /jobs/{id}/stages` to fetch ATS stages; NO API to create new stages
- **Move candidates**: `POST /applications/{id}/move` with `from_stage_id` and `to_stage_id` body params
- **Advance candidates**: `POST /applications/{id}/advance` moves to next stage (no stage ID needed)
- **Inbound events**: `candidate_stage_change` webhook for real-time stage movement notifications
- **Candidate export**: `POST /candidates` + `POST /candidates/{id}/applications` to export sourced candidates
