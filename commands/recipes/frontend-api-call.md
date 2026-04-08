---
name: frontend-api-call
description: Make authenticated frontend API calls using browser cookies, with auto-detection of expiry and prompt for refresh
inputs: ["url", "method", "body"]
chain_to: null
chain_when: null
project: connected-project-phase2
---

## Cookie Storage

Cookies are stored at `/tmp/.linkedin-recruiter-cookies.txt` (ephemeral, cleared on reboot).

## Steps

1. **Check for saved cookies:**
   ```bash
   cat /tmp/.linkedin-recruiter-cookies.txt 2>/dev/null
   ```
   - If file exists and is non-empty → use it
   - If file missing or empty → ask user for a fresh browser curl (Step 4)

2. **Make the API call:**
   Use the saved cookies with the request. Required headers for talent-solutions-web API:
   ```bash
   CSRF_TOKEN=$(grep -o 'JSESSIONID="ajax:[^"]*"' /tmp/.linkedin-recruiter-cookies.txt | sed 's/JSESSIONID="//;s/"//')
   COOKIES=$(cat /tmp/.linkedin-recruiter-cookies.txt)

   curl -s '{{url}}' \
     -H 'accept: application/json' \
     -H 'content-type: application/json; charset=UTF-8' \
     -H "csrf-token: $CSRF_TOKEN" \
     -H 'x-restli-protocol-version: 2.0.0' \
     -H "x-restli-method: {{method}}" \
     -b "$COOKIES" \
     --data-raw '{{body}}'
   ```

3. **Check response for auth failure:**
   - If response contains `401`, `403`, `"loginRequired"`, `"CSRF"`, or HTML login page → cookies expired, go to Step 4
   - If response is valid JSON with `results` or expected data → success, done

4. **Prompt for fresh cookies:**
   Ask the user:
   > Cookies expired. Please:
   > 1. Open Chrome DevTools on any Recruiter page (https://www.linkedin.com/talent/...)
   > 2. Go to Network tab, find any API request (e.g., click on a candidate)
   > 3. Right-click the request → Copy → Copy as cURL
   > 4. Paste the curl here

5. **Extract and save cookies from the pasted curl:**
   Parse the `-b '...'` or `--cookie '...'` or `-H 'cookie: ...'` from the curl command.
   ```bash
   # Extract cookie string and save
   echo "COOKIE_STRING_HERE" > /tmp/.linkedin-recruiter-cookies.txt
   ```
   Also extract `JSESSIONID` for CSRF token.

6. **Retry the original call with fresh cookies** (go to Step 2)

## Common API Calls

### Move candidate (BATCH_PARTIAL_UPDATE)
```
URL: https://www.linkedin.com/talent/api/talentHiringProjectCandidates/?ids=List(urn%3Ali%3Ats_hiring_project_candidate%3A%28urn%3Ali%3Ats_contract%3A{{CONTRACT}}%2Curn%3Ali%3Ats_hire_identity%3A{{HI_ID}}%2Curn%3Ali%3Ats_hiring_project%3A%28urn%3Ali%3Ats_contract%3A{{CONTRACT}}%2C{{PROJECT_ID}}%29%29)&altkey=urn
Method: BATCH_PARTIAL_UPDATE
Body: {"entities":{"urn:li:ts_hiring_project_candidate:(urn:li:ts_contract:{{CONTRACT}},urn:li:ts_hire_identity:{{HI_ID}},urn:li:ts_hiring_project:(urn:li:ts_contract:{{CONTRACT}},{{PROJECT_ID}}))":{"patch":{"$set":{"candidateHiringState":"urn:li:ts_hiring_state:(urn:li:ts_contract:{{CONTRACT}},{{TARGET_STATE_ID}})"}}}}}
```

### Get candidate
```
URL: https://www.linkedin.com/talent/api/talentHiringProjectCandidates/?ids=List(urn%3Ali%3Ats_hiring_project_candidate%3A%28urn%3Ali%3Ats_contract%3A{{CONTRACT}}%2Curn%3Ali%3Ats_hire_identity%3A{{HI_ID}}%2Curn%3Ali%3Ats_hiring_project%3A%28urn%3Ali%3Ats_contract%3A{{CONTRACT}}%2C{{PROJECT_ID}}%29%29)&altkey=urn
Method: GET (no x-restli-method header needed)
Body: (none)
```

### List candidates in project
```
URL: https://www.linkedin.com/talent/api/talentHiringProjectCandidates?q=hiringProject&hiringProject=urn:li:ts_hiring_project:(urn:li:ts_contract:{{CONTRACT}},{{PROJECT_ID}})&count=100
Method: GET
Body: (none)
```

## URN Format Reference

Frontend uses `ts_` prefixed URN types:

| Frontend (ts-api) | Backend (mcm-mt) |
|-------------------|-----------------|
| `ts_contract` | `contract` |
| `ts_hire_identity` | `hireIdentity` |
| `ts_hiring_project` | `hiringProject` |
| `ts_hiring_state` | `candidateHiringState` |
| `ts_hiring_project_candidate` | `hiringProjectCandidate` |

## Expected Output

Success:
```json
{"results":{"urn:li:ts_hiring_project_candidate:(...)":{"status":204}},"errors":{}}
```

## On Failure

- 401/403/login redirect → cookies expired, prompt for fresh curl
- 422 → invalid URN format or state ID
- 500 → check ts-api logs, then mcm-mt logs
- If move succeeds (204) but no write-back → check mcm-mt prerequisites (know-011)
