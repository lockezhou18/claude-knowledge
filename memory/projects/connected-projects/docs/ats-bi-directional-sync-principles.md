ATS Bi-Directional Sync Principles

Author : Sanjana Vohra

| Reviewer | Status |
| --- | --- |
| Aditya Hegde | Approved  Left Comments (9/29) |
| Yash Bhandari | ApprovedLeft some comments |
| Gaurav Sisodiya | Not started |
| Gaurav Chandak | Under review |
| Ritvik Kar | Under review – aligned on principles 1,2,3. #4 feels more tablestakes vs principles but agreed. |
| Tara Iyer | Under review  Responded to latest comments |
| Vineet Goyal | Approved |
| Piyush Masrani | Approved |
| NIRAV GOHEL | Approved |
| Yufei Wang | Approved |
| Si Chang | In progress |

## Introduction

With the Connected Projects charter moving LinkedIn Recruiter towards an all-in-one system for recruiters to manage sourcing, evaluation, & applicant management, bi-directional data syncs are at the forefront of the requirements to support seamless workflow between ATS & LinkedIn Recruiter. We should be able to provide near-realtime updates to keep the data at both ends in sync with limited manual intervention. The aspiration for realtime with <1sec for write confirmation & <10sec for read confirmation will be adjusted based on technical limitations as a best effort.

### Current Status

Connected Projects MVP & Fast Follow along with Enhanced Data Sync charters have been built with the following sync supports :

1. Sync Data from ATS to Recruiter, allow creation of Connected Projects & show the ATS data as part of Connected Projects
2. Build-Out Reads on data from partners, allowing merging & enhancement of ATS data from Build-In (EDS)
3. Application Evaluation Write Back for Ats Applicants - via both web-hook & Build-Out API
4. Existing 1-Click Export of Candidates via web-hook - no data sync-back confirmation on exported entity(s), and different partners may be handling it differently

Summary : Reads are supported for ATS entities via Build-In & Build-Out. Writes are supported for one LI-owned entity (LiHA Application Evaluation) via Build-In & Build-Out. Write is supported only for 1-Click Candidate Export via Build-In.

RSC systems today just export and forget about the entity. Current systems do not confirm whether an exported data (app eval or candidate) was synced back to RSC by the ATS via BI or BO.

### Long Term Vision

With Connected Projects Phase 2 & beyond, Integration Platform should be able to support near-realtime writes to ATS systems for new entities & updates to existing entities (use-case based per partner). Starting with Application Stages as part of Phase 2, this will expand to prospects, notes & tags, and maybe in the distant future to attribute level updates on ATS entities like candidate, application etc.

In order to support designing the Integration Platform for bi-directional data synchronization, this document captures the basic principles that should be followed for short term & long term design considerations.

Detailed design for Application Stage Bi-Directional Sync based on the following principles can be found here : [Application Stage Bi-Direction Sync](https://docs.google.com/document/d/1EX9Hg-os-nFKZCxRooqt_ear28Sf_bgpvQFRncuSZYw/edit?usp=sharing)

## Principles

The following design principles have been derived based on several investigations, design and product discussions. These are being set so that all technical & product designs in the future will be aligned with these principles in order to create a scalable and efficient system.

### ATS is the source of truth

* For all RSC entities (i.e. entities which the RSC system stores or manages throughout its workflows), ATS data should stay as the source of truth. An RSC record will be **created/updated only when the data is synced** **from the ATS** to RSC via BI or BO.
* **Integration\*Apis** for the respective entities should always **reflect the latest merged read from ATS SOT** by default. There should be additional ways to reflect the in-progress writes.
* Integration Platform will communicate the current status of the write request from read and write flows. Clients should define their own way to interpret the intermediate state of a write request which is pending confirmation from read flow. IP may offer a suggested interpretation, which is up to the clients to use. This may vary entity to entity.
* Each request and response to and from ATS should be logged. This is to complement request status with extra information. This can be used in future for various use cases like write after read, partial entity failures etc.

### Consecutive Record Level Updates

* **IP Proposal :** Do not accept further updates on a record until the first request for updating the same attribute is successfully sent to the partner, i.e. 2xx response from partner API.
  Eg. If an application stage change request A->B is in progress, client should not be able to send B->C since B is not the current state, and not even successfully written to the ATS yet.  **HP Preference :** Further changes to be allowed and forwarded to partner in case of updates to the same entity as an in-progress export request.

Eg. If an application stage change request A->B is in progress, client (HP) should be able to send B->C and C->D and IP should propagate it to the partner.
**Conclusive Product Alignment** : Allow consecutive updates for Phase 2 (since downstream partner writes might take up to a minute). Design should support flexibility to reject or disallow updates in future if downstream is facing high error rates or latency. This should be configurable per partner API.
([FAQ](#sy1xhherki79))

* Accept create use cases always - eg. creation of multiple applicationNotes can be done in parallel for the same application. Export of multiple prospects can be done for the same jobRequisition.
* Do not accept requests for creation of entities with *parent entity creation in progress*. Eg. if creation of a new application is in progress, we may not be able to update the stage or add a new note for it (since the AtsApplicationId doesn’t exist yet).
* Further in future, updates on same attributes should not be accepted while a request is in progress, eg. further updates on job description disabled until the first update is written successfully to the partner API. Or further updates on candidate address disabled until the first update is written successfully to the partner API. This is important lest it should leave the data in an inconsistent state.
* Considering these principles, details can be derived on a case to case basis.

### Clear Communication of Intermediate State

* Since data sync is **asynchronous** for both reads & writes, the system should be able to maintain **intermediate states for writes in-progress**.
* Integration platform should be able to give the **current state of an export request** to clients.
* Integration Platform should proactively **inform clients of changes to current state** of write requests (via events).

* Integration Platform will not make a decision for a success or failure of a request based on the intermediate states. IP will communicate the state changes, and it is up to the clients to interpret the intermediate states based on per entity/operation use case.
* Integration Platform should be able to have a **change log of all reads & writes** on a record in the order that they were reflected in the system. This may be used in the future for auditing or reporting purposes. This may even be used by clients for their interpretation.
* Integration Platform should be able to support a Request Dashboard in the future, i.e. a place to show all write requests for a particular company or data provider.
* Interim states to reflect :

![](data:image/png;base64...)

Write Back State Diagram

### Error Handling

* Following are the major error scenarios which should be captured as failures :
  1. **Write API failure** (terminal)

4/5xx response from partner API

* 1. **Data Overwritten** (non-terminal)

Data received from ATS while Write request was outgoing (i.e. REQUEST\_RECEIVED, REQUEST\_AT\_GATEWAY or PARTNER\_API\_RETRYING) is different from the export request data. This will happen if a conflicting data is received from ATS before getting a successful API response from ATS. **The write flow will still continue, and may reach a successful state**. (because the request might be in processing at the gateway, so it might still go through and succeed or fail depending on partner logic).
Eg. Current value : A, Export Request : B, current state : REQUEST\_AT\_GATEWAY
While B is outgoing, C is received from ATS.
This will result in the export request marked as DATA\_OVERWRITTEN.
The write request may still complete after this, leading to PARTNER\_API\_SUCCESS & then be read back from the partner leading to READ\_CONFIRMED.

| Timestamp | Action | SOT value | Export Request Status |
| --- | --- | --- | --- |
| T0 | A is read | A | - |
| T1 | Export Request sent for B | A | writeStatus = REQUEST\_AT\_GATEWAY readStatus = PENDING |
| T2 | C is read | C | writeStatus = REQUEST\_AT\_GATEWAY readStatus = DATA\_OVERWRITTEN |
| T3 | Export Request API for B completes | C | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_OVERWRITTEN |
| T4.a | B is read | B | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFIRMED |
| T4.b (before timeout) | C/D is read | C/D | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT |
| T4.c (timeout) | Timeout | C | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_EXPIRED |

* 1. **Read Conflict** (potential terminal)The data received from ATS (via BI or BO) after Write API success does not match the written data.
     Eg.
     Current value : A, Write Request : B, status : PARTNER\_API\_SUCCESS.
     C is received from ATS at time T1. This leads to export status being set to DATA\_READ\_CONFLICT, and the SOT value is now C.

**It is possible to receive matching data for the export request after some time within the time threshold,** leading to DATA\_READ\_CONFIRMED. This is to incorporate read after write consistency time gap for partners, as a write may take some time to be reflected on the partner reads, and may come a bit later.
Eg. time T2 : B is received from ATS
Current value : C, Write Request : B, previous\_status : DATA\_READ\_CONFLICT.
The new status will be set to DATA\_READ\_CONFIRMED.

**We will allow read matches to data until timeout**, i.e. match newly received data with an API succeeded export request until its timestamp passes the threshold timeout.

If a conflict occurs, the read status will remain DATA\_READ\_CONFLICT, even after timeout, to reflect that data was read but didn’t match. We won’t change it to DATA\_READ\_EXPIRED, as that status implies no data was read after the write API completed.

| Timestamp | Action | SOT value | Export Request Status |
| --- | --- | --- | --- |
| T0 | A is read | A | - |
| T1 | Export Request sent for B | A | writeStatus = REQUEST\_AT\_GATEWAY readStatus = PENDING |
| T2 | Export Request API for B completes | A | writeStatus = PARTNER\_API\_COMPLETED readStatus = PENDING |
| T3 | C is read | C | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT |
| T4 (before timeout) | B is read | B | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFIRMED (terminal state) |

Alternatively for a terminal state (no matches till timeout):

| Timestamp | Action | SOT value | Export Request Status |
| --- | --- | --- | --- |
| T0 | A is read | A | - |
| T1 | Export Request sent for B | A | writeStatus = REQUEST\_AT\_GATEWAY readStatus = PENDING |
| T2 | Export Request API for B completes | A | writeStatus = PARTNER\_API\_COMPLETED readStatus = PENDING |
| T3 | C is read | C | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT |
| T4 | D is read | D | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT |
| T5 | Time threshold reached | D | writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT (**terminal state now**) |
| T6 | B is read | B | **NO CHANGES** writeStatus = PARTNER\_API\_COMPLETED readStatus = DATA\_READ\_CONFLICT |

* 1. **Request Expired** (terminal)

After partner API succeeds, the request will be kept alive (actively matching and attributing to incoming data) for a certain time threshold. If no data is received in that period, whether matching or conflicting, the request will be marked as DATA\_READ\_EXPIRED.

This is based on a time-bound thresholdon an export request if the data is not reflected at the ATS within a certain time (even after retries - currently 5 retries with exponential backoff coefficient of 2 starting at 5sec). This threshold will vary with partner and usecase. This is a recommendation for the clients to handle such error scenarios and communicate appropriately to the user.
***Note*** : This is an error scenario, and may be due to high error rates or latencies at the partner. Monitoring should be added to alert if this is happening for a lot of requests - which would mean reliability issues at partner API level. This status is a recommendation for the clients to handle such error scenarios and communicate appropriately to the user.

* 1. **Partner Specific Data Validation Failure** (terminal)

Ideally, partner specific data validation should mostly be done by the partner, as they may keep changing and it is better to not have partner specific validation logic at gateway. There may still be some partner specific data validations, eg. one partner doesn’t allow updates on a certain field or doesn’t allow certain values to be set etc. These rules will be partner specific and if needed, should be handled appropriately at the client layer.

**Note** : In failure cases, it is possible that a subsequent read matches the now-failed write request. We do not want to flip the status of a write request from failed to success in this case.
It is possible to do this via offline reconciliation, but need product guidance on whether a failure should be allowed to be corrected to success. *Product feedback* : failure should not be corrected to a success if the data is received after a failure. It may be due to someone changing it at ATS end, and can not be attributed to the request from client(HP).

**Note** : It is possible in future that one entity export from clients leads to multiple requests at partner. This may bring in complex error scenarios, with partial success and failure. This would have to be handled appropriately at that point, holding and expanding the principles as defined here. It is out of scope at this stage.

**Note** : Stricter time threshold requirements may be needed for BuildIn partners for allowing Bi-Directional sync cc Ritvik Kar

Should EDS deauthorization terminate the export request? - Yes if the deauth happens before the data is sent to ATS..

## **FAQs**

* **Why can’t we reflect in-progress request records in RSC data?**
  + RSC data today is a ***proxy for ATS data*** and reflects the data received from ATS as-is. It is the true reflection of the ATS data within the LinkedIn ecosystem. If we redesign this to incorporate data updates/creates from requests that are outgoing to the partner, then it would become *very complex to distinguish between SOT data & the versions of the data that our clients (HP today, more in future) have attempted to change*. This becomes even more problematic when we go for attribute level updates in the future.
  + Partner BuildOut post *APIs are mostly asynchronous* in nature, implying that a successful response from the API is just an acknowledgement of the acceptance of the request for processing. It may or may not succeed, and the error rates & latencies depend on the partner & use case. With this low reliability downstream system, we can not know for sure that a 2xx response from a partner API will mean that the data is eventually synced back to RSC.
  + Partner writes may happen via *BuildIn or BuildOut*. Although with EDS our future proposals are to have more and more BuildOut integrations so we do not have to depend on BuildIn (which is - partner system proactively sending or receiving data), we will still have some partners who are on BuildIn and might not move to BuildOut (upcoming integration with Tracker). Moreover, BO integrations have a lot of friction from partners, so it may be quite some time until we reach a BO primary system.
    This makes our system tightly coupled with partner systems’ reliability, consistency & latency.
  + BuildIn latency for successful write requests will depend on partner sync latency, and *we will not even get externalEntityIds from buildIn write flow* - implying that the records would need to be created without the identifiers.
  + If we assume that records are inserted/updated in RSC data from write requests, eg. a candidate is exported - create an AtsCandidate from write flow itself (firstly, the existing tables won’t work because new AtsApplication or AtsCandidate can not be created without the atsApplicationId/atsCandidateId - the external ID at the ATS layer. Similar for other entities like Note), & its associated application, application stages, notes etc. Then we *need to support a cascaded rollback throughout the system to have eventual consistency with ATS data* - IP, HP & all future clients would have to be able to rollback the data to its original state in case of failure to read the data back from ATS.
    We are proposing to maintain this consistency by supporting clients with request statuses for both read and writes, and they can interpret the status on their own based on use case.
  + Why can’t we have a dummy IPUrn for in-progress requests?
    Current design of IP Urns is just a 1:1 mapping to the external identifiers : IPUrn= IntegrationContext + DataProvider + ExternalIds. ([ID Mapping - MVP Design](https://docs.google.com/document/d/1r_CKe6vN13kwZ8bA-4qK7m7WhiMQr3RISLO18A2fo7w/edit?usp=sharing))
    Dummy IP Urns as placeholders may lead to dangling records because of gaps in association with actual records coming in from the ATS probably later in the future after a failed write.
* **Why can’t we perform a read after a successful write API request?**

* + This is from the Greenhouse API :
    ![](data:image/png;base64...)
  + Most ATSes do not guarantee immediate read-after-write consistency, and can take some time to reflect the complete data on their systems. Furthermore, besides the good ones like GH, there are many systems with very low reliability and high latencies in data writes. Additionally, most partner APIs are not transactional in nature and represent best-effort at consuming the update.
  + That said, it can be done on a case to case basis if an ATS partner supports read after write consistency. This will reduce the time to confirm the data to immediate confirmation after a successful write.
* **Do partners offer some tiered APIs with varying reliability - transactional, best effort?**
  + ATS partners do not provide a guarantee on SLAs or transactionality on the APIs that they expose. That said, we are working with GH to get the expected P90 & P99 latency & error rates for their write APIs. More metrics will also be derived based on charter ramp for app eval writes.
  + Assuming the three tiers as :
    Tier 1 : transactional + rate limited
    Tier 2 : rate limit
    Tier 3 : best effort
    In the current state, most partner APIs lie in Tier 3. The APIs provided by most partners (including GH) are asynchronous, meaning that the response is an acknowledgment of the request and the actual processing happens afterwards.
    Our design can be extended to handle the different tiers as well, with read-after-write at gateway in case some APIs guarantee transactionality & hence read-after-write consistency as well.
* **How long can it take from a user updating a stage to getting a successful write response back to client (HP)?**
  + This will vary partner to partner - QPS restrictions, partner API latencies etc. Eg. Lever and Workable have better QPS limits than Greenhouse.
  + Considering the path from client (HP) to IP to RSC to gateway to external ATS system and back the same path to client (HP), this may take upto 100 seconds for GH writes (rough estimation - after nearline writes improvement). This is planned to be improved further based on partner negotiations.
* **How long will it take for the change in status to be reflected as SOT in Recruiter?**

Ref : [Bi-Directional Sync Latencies](https://docs.google.com/document/d/1OaWk5nDYlRjzecjgzceRUiEes48-XDTEk_GoYjxrrpw/edit?usp=sharing)

* **Why is it advised to wait till the data is read back (in best case) or at least written successfully at the partner system to perform further updates on the same entity attribute?**
  + There is a time gap between data updates at ATS and the data being received on RSC. The RSC data on which the user may be performing operations may itself be stale.
  + In case of write backs eg. stage updates, consider the case if RSC data is stage A and the user updates it to stage B. Assuming the request A->B is yet to be read back, and we allow the user to further change it to C, i.e. B->C. If the previous request is not reflected yet, the second request may be translated to A->C at the ATS instead of the intended A->B->C.
    Furthermore, stage changes are maintained in a historic record. This may cause inconsistencies in what is shown to the user vs the ATS SOT. This adds complexity to clients in handling error scenarios and supporting a clear communication to users on past requests failing.
  + These are error scenarios and not the majority case. But the designs should be able to handle these well without causing the data to be in an unexpected state.
  + Even the expectation of a user wanting to update the same attribute in the span of a few minutes is unlikely - and only needed in edge case scenarios, say the user put something by mistake & wants to correct it. Even in that case, it is better to give the user a reliable experience by allowing them to update only after the first update has gone through successfully, and reducing the chances of the data being in an inconsistent state.
* **What are the limitations from partner APIs at the gateway layer?**
  + *QPS restrictions* - Greenhouse offers very low QPS (5 currently) across all customers and APIs - read and write combined. There are ongoing negotiations with GH to increase the QPS limits, but it can be done only once we have enough traffic going to GH, hitting the QPS limits. Currently, BO requests are pooled for 15 minutes & planned to be decreased to 1 minute to hit the QPS limits & make a case with GH.
    Other partners may offer per customer QPS which will be better, but the rate at which BO calls can be made to the partner will always be restricted by the rate limits given by individual partners.
  + *Asynchronous APIs* : Most ATS partners have asynchronous buildout APIs for write use cases. This means that a successful API response from the partner implies an acknowledgement for processing the request, and does not guarantee that the request is processed successfully.
  + *Read after write consistency delays* : Most ATS partners do not offer immediate read after write consistency. With distributed systems, even if the APIs were synchronous, it would take some time for the data to reflect in all colos and be consistent with the requests. Example from GH API’s explicit callout [here](#mehrtgkw71hg).
* **Why do we need to have a DATA\_READ\_EXPIRY threshold?**
  + As called out, data read expired must not be a normal scenario, but an error case, where data isn’t received for the write request even after a certain threshold (TBD - Product).
  + This is required to have a definite time after which the read status of the request will be terminated, and not kept in data read pending state forever.

## Appendix

![](data:image/png;base64...)

![](data:image/jpeg;base64...)

![](data:image/png;base64...)

* + Furthermore, updates on an attribute like job description or candidate address must not be allowed to be overwritten because it might lead the data in an inconsistent state.
    Eg.
    - current SOT value T0 : “This is a job for software engineer”
    - HP update WIP T1 : “This is a job for senior software engineer”
    - HP update WIP T2 : “This is a job for senior software engineer in Bangalore”
    - ATS update - current SOT value T3 : “Software Engineer Role in Bangalore”
    - The final state will depend on the partner’s read after write consistency delays, errors, in addition to the time in the nearline system from HP to partner & back.
