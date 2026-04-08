# QProd Validation Workflow

End-to-end validation for talent-solutions-api changes: build, test, deploy to qprod, curli test, and debug.

## Step 1: Build & Test

```bash
mint test
```

- Runs full build + all unit tests
- Check output for `BUILD SUCCESSFUL` and test summary (e.g. `7516 tests, 0 failed`)
- If ConfigCompilationException occurs, try `mint update` first (pulls latest dependency versions with config fixes)
- Search Slack for the key error message if `mint update` doesn't help

## Step 2: QProd Deployment

### Setup (first time or after cleanup)
```bash
mint qprodSetup
```

### Start the server
```bash
mint qprodRun
```

### Verify startup
Do NOT use `curl localhost:1729` — it often returns 400. Instead check logs:
```bash
# Watch for "Start to listen at 1729" in the logs
tail -f /export/content/lid/apps/talent-solutions-api-frontend/dev-i001/logs/talent-solutions-api-frontend.log
```

Startup takes 2-5 minutes. Look for:
```
INFO [AvesServer] [...] Start to listen at 1729 for HTTP.
INFO [AvesServer] [...] Start to listen at 2302 for HTTPS.
```

### Stop the server
```bash
# Find and kill the Java process
ps aux | grep talent-solutions-api-frontend | grep -v grep
kill <PID>
```

## Step 3: Curli Testing via QProd

### Getting a curl command
1. Open `https://qprod.www.linkedin.com` in Chrome
2. Navigate to the page that calls the API endpoint you want to test
3. Open DevTools > Network tab
4. Find the API request, right-click > Copy > Copy as cURL

### Required headers for REST.li
```
-H 'accept: application/json'
-H 'x-restli-protocol-version: 2.0.0'
-H 'x-http-method-override: GET'
-H 'csrf-token: <from JSESSIONID cookie>'
```

### Example curl structure
```bash
curl -s 'https://qprod.www.linkedin.com/talent/api/<endpoint>' \
  -H 'accept: application/json' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -b '<cookies from browser>' \
  -H 'csrf-token: <csrf-token>' \
  -H 'x-restli-protocol-version: 2.0.0' \
  -H 'x-http-method-override: GET' \
  --data-raw '<field projections>'
```

### Real example: talentHiringProjects with field projections
From PR #8276 (ATS pipeline candidate count support):
```bash
curl -s 'https://qprod.www.linkedin.com/talent/api/talentHiringProjects/urn%3Ali%3Ats_hiring_project%3A(urn%3Ali%3Ats_contract%3A237044161%2C1430809796)' \
  -H 'accept: application/json' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -b '<cookies from qprod browser session including JSESSIONID, li_at, li_a, li_er, lror, etc.>' \
  -H 'csrf-token: ajax:<JSESSIONID value>' \
  -H 'origin: https://qprod.www.linkedin.com' \
  -H 'referer: https://qprod.www.linkedin.com/talent/hire/1430809796/manage/all' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...' \
  -H 'x-http-method-override: GET' \
  -H 'x-li-lang: en_US' \
  -H 'x-li-page-instance: urn:li:page:d_talent_projectsHome;...' \
  -H 'x-li-track: {"clientVersion":"1.9.2167","mpVersion":"1.9.2167","osName":"web",...}' \
  -H 'x-restli-protocol-version: 2.0.0' \
  --data-raw 'altkey=urn&decoration=%28entityUrn%2CcandidateCounts*%2C...%29'
```

Key observations from this example:
- `--data-raw` contains URL-encoded field projections (decoration parameter)
- The `csrf-token` header must match the `JSESSIONID` cookie value
- `x-http-method-override: GET` turns the POST into a GET (needed for large field projections)
- `x-li-track` includes client version info used for routing

### Parsing response
```bash
# Pretty-print JSON response
bash /tmp/curli.sh 2>&1 | python3 -m json.tool

# Extract specific field
bash /tmp/curli.sh 2>&1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(json.dumps(data.get('candidateCounts', []), indent=2))
"
```

## Step 4: LIX Override Testing

### How LIX overrides work
The `lror` cookie controls LIX overrides. Format:
```
lror=<lix.key.1>=<value1>&<lix.key.2>=<value2>
```

### Toggle a LIX value
Find the `lror` cookie in the curl command and change the value:
- `=control` — LIX disabled (default/control group)
- `=enabled` — LIX enabled (treatment group)

Example — change from control to enabled:
```
# Before
lror=talent-solutions-api.ats.pipeline.candidate.count.enabled=control

# After
lror=talent-solutions-api.ats.pipeline.candidate.count.enabled=enabled
```

### Best practice
Write the curl to a script file (e.g. `/tmp/curli_test.sh`) to avoid shell quoting issues with cookies:
```bash
cat > /tmp/curli_test.sh << 'SCRIPT'
curl -s 'https://qprod.www.linkedin.com/...' \
  -b '...; lror=...lix.key=enabled; ...' \
  ...
SCRIPT
bash /tmp/curli_test.sh
```

## Step 5: Debugging

### Server logs location
```
/export/content/lid/apps/talent-solutions-api-frontend/dev-i001/logs/talent-solutions-api-frontend.log
```

### Search for errors
```bash
# Search for specific error patterns
grep -i "Error in decorating\|Error fetching\|NPE\|NullPointer" \
  /export/content/lid/apps/talent-solutions-api-frontend/dev-i001/logs/talent-solutions-api-frontend.log | tail -10
```

### Common debug pattern: Empty response due to recover()
Many binder methods use `.recover()` to swallow exceptions and return empty results:
```java
.recover(e -> {
    log.error("Error in decorating candidateCounts: {}", e.getMessage());
    return new CandidateCountArray();
});
```

If a field is unexpectedly empty in the API response:
1. Check the server logs for the corresponding error message
2. The stack trace / error message reveals the actual exception
3. Common cause: NPE from missing fields on backend data objects (e.g., `getData()` returning null)
4. Fix: Add null-safety checks (`hasData()`, `hasXxx()`) before accessing nested fields

### Session expiry
If curl returns an HTML login page instead of JSON, the qprod session cookies have expired. Re-login at `https://qprod.www.linkedin.com` and copy fresh cookies from DevTools.

## Common Issues

| Issue | Solution |
|-------|----------|
| `ConfigCompilationException` during `mint qprodRun` | Run `mint update`, then retry. Search Slack for the error key. |
| `curl localhost:1729` returns 400 | Use `qprod.www.linkedin.com` via browser instead |
| Server takes long to start | Normal — 2-5 minutes. Check logs, not localhost. |
| QProd curl returns HTML login page | Session expired. Re-login at qprod.www.linkedin.com |
| Empty array in response but no client error | Check server logs for `.recover()` swallowed exceptions |
| Python pipe error on qprodRun | Ignore — server usually starts fine despite this error |

## Reference PR

**PR #8276** — ATS pipeline candidate count support (https://github.com/linkedin-multiproduct/talent-solutions-api/pull/8276)

This PR demonstrated the full validation cycle:
1. `mint test` — 7516 tests passed
2. `mint qprodRun` — deployed to qprod on port 1729
3. Curli with `lror` cookie `ats.pipeline.candidate.count.enabled=control` — verified main pipeline counts work, ATS stages excluded
4. Curli with `lror` cookie `=enabled` — initially returned empty `candidateCounts` (bug!)
5. Debugged via server logs: found NPE in `HiringCandidateFacetCountFormatter` — `getData()` null for ATS pipeline items
6. Fixed with `hasData()` null-safety checks, rebuilt, redeployed
7. Re-tested with `=enabled` — 35 candidate count entries returned correctly (main + ATS pipeline)
