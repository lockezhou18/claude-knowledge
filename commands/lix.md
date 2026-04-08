---
name: lix
description: Manage LinkedIn Experiments (LiX) — evaluate treatments, create lix keys, create iterations, list keys for an MP
inputs: ["subcommand", "args"]
---

# LiX Management Skill

Manage LinkedIn Experiments (LiX) from Claude. Supports eval, iterate, create, and show.

## Subcommands

### `eval <key>` — Check what treatment a user gets

Wraps `lix-cli`. Quick check of current treatment value.

```bash
lix-cli <key> [-l <ldap>] [-mp <multiproduct>] [-f <fabrics>]
```

**Examples:**
- `/lix eval talent.connected.project.phase2.enabled`
- `/lix eval talent.connected.project.phase2.enabled -l bizhou -mp hp-ats-integration-mt`

**Steps:**
1. Run `lix-cli` with the provided key and any flags
2. Report the treatment value
3. If `control` or empty, note that the lix may not be ramped for this user/context

**KNOWN LIMITATION:** `lix-cli` only evaluates with `entity=urn:li:corpuser:<ldap>`.
It CANNOT evaluate lixes targeted by `dataProvider`, `contractUrn`, `enterpriseAccount`, etc.
For those, use one of:
- **TReX Treatment Lookup UI**: https://trex.corp.linkedin.com/trex/member-treatments
  (enter key + custom entity URN like `urn:li:developerApplication:225950754`)
- **Direct lix-proxy curl** (corp fabric only):
  ```bash
  curl -s "https://lix-proxy.corp.linkedin.com/corp-lca1/lix-proxy/lixTreatments/<KEY>?entity=<ENTITY_URN>" \
    --cacert /etc/lipki/ca-bundle.crt
  ```
  Note: returns `{"treatment":"<value>","segment":<n>}`. Corp fabric only — prod fabric unreachable from Mac.
- **Prod shell**: SSH to a prod shell and curl lix-proxy from there for prod fabric evaluation.

Also: `-f prod-ltx1` flag tries to connect directly to prod hosts which are unreachable from Mac — it will error and default to `control`.

---

### `iterate <testId>` — Create a TReX iteration (experiment)

The high-value command. Creates an iteration on an existing TReX test via the lix-gui V3 API.

**API:** `POST https://trex.corp.linkedin.com/lix-gui/api/v3/experiments/`

Note: The V3 endpoint is `/api/v3/experiments/` (NOT `/api/v3/tests/{testId}/experiments`).
The `testId` goes in the request body.

**Auth:** TReX SSO cookies stored at `/tmp/.trex-cookies.txt`

**Steps:**

1. **Parse arguments:**
   - `testId` (required) — numeric TReX test ID (from the URL, e.g., 2081614185)
   - `--targeting` / `-t` — targeting type: `all`, `id` (default: `all`)
   - `--target-entity` — entity type for ID targeting: `contractUrn`, `developerApplication`, `member`, `enterpriseAccount`, etc.
   - `--target-ids` — comma-separated target IDs (required if targeting = id)
   - `--treatment` — treatment value name (default: "enabled")
   - `--pct` — treatment percentage for the 'all' segment (default: 100)
   - `--description` / `-d` — iteration description

2. **Check for saved TReX cookies:**
   ```bash
   cat /tmp/.trex-cookies.txt 2>/dev/null
   ```
   - If missing or empty → prompt user (Step 6)

3. **Build the selectorSpec JSON:**

   The V3 API uses `selectorSpec` (a JSON string), NOT raw DSL. The server generates the DSL from it.
   The `selectorSpec` is a JSON object with a `selectors` array. Each selector has:
   - A type discriminator (via Java polymorphism — `SelectorRampUp`, `SelectorIds`, `SelectorPredefined`, `SelectorAdvanced`)
   - An `allocationList` array of `{name, percentage}` objects

   **For `all` targeting (simple ramp, 100% enabled):**
   ```json
   {
     "selectors": [
       {
         "type": "RAMPUP",
         "allocationList": [{"name": "enabled", "percentage": 100}]
       }
     ]
   }
   ```

   **For `all` targeting with partial ramp (e.g., 50%):**
   ```json
   {
     "selectors": [
       {
         "type": "RAMPUP",
         "allocationList": [{"name": "control", "percentage": 50}, {"name": "enabled", "percentage": 50}]
       }
     ]
   }
   ```

   **For ID-based targeting (e.g., specific contracts):**
   ```json
   {
     "selectors": [
       {
         "type": "IDS",
         "ids": [2043270072],
         "allocationList": [{"name": "enabled", "percentage": 100}]
       },
       {
         "type": "RAMPUP",
         "allocationList": [{"name": "control", "percentage": 100}]
       }
     ]
   }
   ```

   Also build segment names:
   - For `all` targeting: one segment named "Base Segment" with baselineVariant "control"
   - For ID targeting: two segments — "Target Segment" (baselineVariant "control") + "Default Segment" (baselineVariant "control")

4. **Build the request body:**
   ```json
   {
     "testId": <testId>,
     "description": "<description>",
     "selectorSpec": "<selectorSpec JSON string — must be stringified, not nested>",
     "segments": [
       {"name": "Base Segment", "baselineVariant": "control"}
     ],
     "enableReporting": false,
     "tracking": false,
     "utcReportEnabled": false,
     "useCorpSelector": false
   }
   ```

   IMPORTANT: `selectorSpec` must be a **stringified JSON string**, not a nested JSON object.
   Use `JSON.stringify()` equivalent — escape quotes, etc.

5. **Make the API call:**
   ```bash
   COOKIES=$(cat /tmp/.trex-cookies.txt)

   curl -s "https://trex.corp.linkedin.com/lix-gui/api/v3/experiments/" \
     -X POST \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -b "$COOKIES" \
     --data-raw '<request body from step 4>'
   ```

   Check response:
   - `200`/`201` → success, extract experiment ID from response
   - `401`/`403` → cookies expired, go to Step 6
   - `400` → bad request, show error details (likely selectorSpec format issue)
   - `404` → testId not found

6. **Prompt for fresh TReX cookies (if needed):**
   > TReX cookies needed. Please:
   > 1. Open any TReX page (e.g., https://trex.corp.linkedin.com/trex/test/{testId})
   > 2. Open Chrome DevTools → Network tab
   > 3. Refresh the page, find any request to `trex.corp.linkedin.com`
   > 4. Right-click → Copy → Copy as cURL
   > 5. Paste it here

   Extract cookies from the pasted curl (look for `-b '...'`, `--cookie '...'`, or `-H 'cookie: ...'`).
   Save to `/tmp/.trex-cookies.txt`.
   Retry Step 5.

7. **Report result:**
   - Print the iteration/experiment ID
   - Print URL: `https://trex.corp.linkedin.com/trex/test/{testId}/iteration/{experimentId}`
   - Remind: "Iteration created in DRAFT state. Go to TReX to request approval and activate."

**Common targeting patterns for HP team:**
- By contract: `--targeting id --target-entity contractUrn --target-ids 2043270072`
- By data provider: `--targeting id --target-entity developerApplication --target-ids 225950754`
- All traffic at 100%: `--targeting all --pct 100`
- All traffic at 50%: `--targeting all --pct 50`

**FIRST-USE CALIBRATION:**
The selectorSpec JSON format above is reverse-engineered from `lix-gui` Java source code
(ExperimentReqObj.java, Selectors.java, SelectorIds.java, SelectorRampUp.java).
If the API rejects the payload on first use:
1. Open Chrome DevTools on the TReX UI
2. Create an iteration manually
3. Capture the actual POST request body from the Network tab
4. Update this skill's selectorSpec format to match

The key source files in `lix-gui` for reference:
- `ExperimentReqObj.java` — request body model
- `ExperimentV3ReqObj.java` — V3 variant (ignores `spec`, requires `selectorSpec`)
- `ExperimentResourceV3.java` — V3 REST endpoint at `/api/v3/experiments/`
- `ExperimentUtils.java` — `buildExperimentSpec(selectorSpec)` builds DSL from selectorSpec
- `Selectors.java` — `fromJson(selectorSpec)` parses the JSON

---

### `create <key>` — Create a new lix key in TReX

Creates a new lix test (not an iteration) via TReX API.

**API:** `POST https://trex.corp.linkedin.com/lix-gui/api/v3/tests`

**Auth:** TReX SSO cookies (same as iterate)

**Steps:**

1. **Parse arguments:**
   - `key` (required) — lix key name (e.g., `talent.my.new.feature.enabled`)
   - `--mp` / `-p` — multiproduct name(s) (required)
   - `--description` / `-d` — description (required)
   - `--owners` / `-o` — comma-separated owner LDAPs (minimum 3, required)
   - `--crew` / `-c` — crew ID (optional, default: 394 for our team)
   - `--fabric` / `-f` — PROD or EI (default: PROD)

2. **Check for saved TReX cookies** (same pattern as iterate)

3. **Make the API call:**
   ```bash
   COOKIES=$(cat /tmp/.trex-cookies.txt)

   curl -s "https://trex.corp.linkedin.com/lix-gui/api/v3/tests" \
     -X POST \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -b "$COOKIES" \
     --data-raw '{
       "testkey": "<key>",
       "description": "<description>",
       "fabric": "PROD",
       "group": "OTHER",
       "testType": "FEATURE_RAMP",
       "multiproducts": ["<mp>"],
       "owners": ["<owner1>", "<owner2>", "<owner3>"],
       "entities": ["member", "guest"],
       "testIntent": "A/B Testing and Feature Ramping",
       "owningCrewId": "<crew_id>"
     }'
   ```

4. **Report result** with test ID and URL

---

### `show <mp>` — List lix keys for a multiproduct

No auth needed — uses the public LiX external API.

**API:** `GET https://lix.corp.linkedin.com/api/external/tests?q=list&...`

**Steps:**

1. **Parse arguments:**
   - `mp` (required) — multiproduct name
   - `--fabric` / `-f` — PROD or EI (default: PROD)
   - `--filter` — optional keyword filter on results

2. **Make the API call:**
   ```bash
   curl -s "https://lix.corp.linkedin.com/api/external/tests?q=list&fields=testkey&mpNames=List(${mp})&fabrics=List(${fabric})&start=0&count=100000&states=List(DRAFT,SUBMITTED,APPROVED,ACTIVE)" \
     --cacert /export/apps/openssl/ssl/cert.pem
   ```

3. **Parse and display results:**
   - List all lix keys, optionally filtered
   - Show total count
   - If `--filter` provided, only show keys containing the filter string

---

## Cookie Storage

TReX cookies stored at `/tmp/.trex-cookies.txt` (ephemeral, cleared on reboot).
Separate from recruiter cookies (`/tmp/.linkedin-recruiter-cookies.txt`).

## TReX API Reference (reverse-engineered from lix-gui source)

| Operation | Endpoint | Auth | Method |
|-----------|----------|------|--------|
| Create test | `/lix-gui/api/v3/tests` | SSO cookie or apiKey+username | POST |
| Create iteration | `/lix-gui/api/v3/experiments/` | SSO cookie or apiKey+username | POST |
| Update iteration | `/lix-gui/api/v3/experiments/{experimentId}/` | SSO cookie | PUT |
| Activate iteration | `/lix-gui/api/v3/experiments/{experimentId}/activating` | SSO cookie | PUT |
| Delete test | `/trex-mt/rest/testsApi/deleteTest` | SSO cookie or apiKey+username | POST |
| List keys (no auth) | `lix.corp.linkedin.com/api/external/tests?q=list&...` | SSL cert only | GET |

## Notes

- The V3 create experiment API is **deprecated** in favor of trex-api (per code comments), but still functional.
- Iterations are created in DRAFT state. They need approval workflow to become ACTIVE.
- The `lix-gui` API accepts both SSO cookie auth and API key auth (`apiKey` + `username` headers).
  For API key auth, you need a KMS secret. The LLS team uses `urn:li:kmsSecret:8ce5fed4-b0d8-47b3-9b8f-4f28266dfda6`.
  Our team would need our own KMS secret for non-interactive use.
