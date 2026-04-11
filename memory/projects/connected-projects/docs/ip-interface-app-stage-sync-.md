IP Interface for Bi-Directional Sync

Author: Sanjana Vohra

| **Reviewer** | **Status** |
| --- | --- |
| Aditya Hegde | In progress  Left Comments (9/29) |
| Yufei Wang | In progress |
| Yash Bhandari | In progress |

## Problem Statement

In order to support Bi-Directional Syncs of Integration Entities, Integration APIs should define a clear interface for clients (HP) to do the following :

1. Online API : Request Upsert for an entity record. Partial updates, batch upserts not in scope for this phase.
2. Online & Offline : Check the status of the upsert request
3. Nearline : Async communication of updates in status of upsert request
4. Online & Offline : Fetch all export requests for an entity

Note : For sample APIs & request/response, we will be focusing on Application Stages for the scope of this document as part of Phase 2 requirements. The design will be extensible for other integration entities in the future.

This is a supporting document for the main design doc : [Application Stage Bi-Direction Sync](https://docs.google.com/document/d/1EX9Hg-os-nFKZCxRooqt_ear28Sf_bgpvQFRncuSZYw/edit?usp=sharing)

## Design

### Upsert

We have existing Integration APIs hosted for all integration entities in talent-partner-integration-mt, eg. [IntegrationApplicationStageApi](https://jarvis.corp.linkedin.com/codesearch/result/?name=IntegrationApplicationStageApi.proto&path=talent-partner-integrations-api%2Ftalent-partner-integrations-api%2Fsrc%2Fmain%2FserviceProto%2Fproto%2Fcom%2Flinkedin%2Ftalent%2Fpartner%2Fintegrations&reponame=linkedin-multiproduct%2Ftalent-partner-integrations-api). These support only getters & finders today.

The same APIs will be extended to support methods for upsert requests. The response will have a request ID for the write request which will be forwarded to the async workflow for writes. The request ID will be the unique identifier for the request throughout the pipeline from client(HP) to IP to gateway.

#### Request : IntegrationApplicationStageUpsertRequest

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| integrationApplicationUrn | IntegrationApplicationUrn | IP Urn of the application for which new stage is to be upserted |
| newIntegrationJobRequisitionStageUrn | IntegrationJobRequisitionStageUrn | IP Urn of the job requisition stage which should be set as the **new stage** for the given application. This is selected from the list of stages for the requisition which is associated with the given application. |
| actor | Urn (SeatUrn) | ViewerUrn of the user who performed this action. Maybe a seat. This will be used to validate the permissions for the operations on the application. |
| requestMetadata.clientEntityUrn |  | ClientEntityUrn associated with this request. |

#### Response : IntegrationApplicationStageUpsertResponse

The success response code will be *202 Accepted* indicating the request has been accepted and being processed asynchronously.

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| requestId | Long | Write Request ID |

### Request Status

![](data:image/png;base64...)

In alignment with [ATS Bi-Directional Sync Principles](https://docs.google.com/document/d/1M3U3ESnfyDtCD_G1Z6n0hTGJZktL8csxJ-N7gy0bhD8/edit?tab=t.0#bookmark=id.q63keu35kedr), the Request Status will be broken down into status of write request & read for the matching data. These will be defined as follows :

| **Write Status Value** | **Definition** |
| --- | --- |
| REQUEST\_RECEIVED | Request is received by Integration Platform. |
| REQUEST\_AT\_GATEWAY | Request has been sent to Gateway. |
| PARTNER\_DATA\_VALIDATION\_FAILURE | Partner specific data validation failed for the export request. |
| PARTNER\_API\_RETRYING | Gateway is retrying the partner API request after at least one failure. |
| PARTNER\_API\_FAILURE | Partner API has failed even after retries. |
| PARTNER\_API\_SUCCESS | Partner API has succeeded. |
| **Read Status Value** |  |
| DATA\_READ\_PENDING | Data has not been received from the partner yet. |
| DATA\_OVERWRITTEN | Data has been overwritten by something else received from ATS while the WRITE request to partner was in progress. |
| DATA\_READ\_CONFLICT | Data received from the partner does not match what was written in this request. [Potential Terminal State](https://docs.google.com/document/d/1M3U3ESnfyDtCD_G1Z6n0hTGJZktL8csxJ-N7gy0bhD8/edit?tab=t.0#bookmark=id.qnd22dh239tj) |
| DATA\_READ\_CONFIRMED | The data received from partner matches the export request. |
| DATA\_READ\_EXPIRED | No data has been received from the partner - neither matching nor conflicting - after the successful write API for a certain threshold of time (TBD time) |

#### Possible Status Combinations ([ref](https://docs.google.com/document/d/1M3U3ESnfyDtCD_G1Z6n0hTGJZktL8csxJ-N7gy0bhD8/edit?tab=t.0#bookmark=id.ahiekzcadfmm))

| **Read Status** | **Write Status** | **Description** | **Terminal State?** | **Recommended Action for Client** |
| --- | --- | --- | --- | --- |
| DATA\_READ\_PENDING | REQUEST\_RECEIVED | No data has been received from the partner for the record yet. | No | Inform the user that the request is being sent to ATS partner. No action required by the user. |
| REQUEST\_AT\_GATEWAY | No | No action needed generally, only FYI. Can be shown only if clients want to give detailed status updates to user. |
| PARTNER\_DATA\_VALIDATION\_FAILURE | Yes FAILURE | Failure due to invalid data. Retry with exact same data will most likely fail again. Show appropriate message to user. |
| PARTNER\_API\_RETRYING | No | No action needed generally, only FYI for clients. Can be communicated to user only if clients want to give detailed status updates to user. |
| PARTNER\_API\_FAILURE | Yes FAILURE | Partner API failed even after retries. Show failure to user and ask to retry. |
| PARTNER\_API\_SUCCESS | No | Partner API succeeded. For optimistic writes, indicate to the user that the data was sent to the ATS, awaiting confirmation. |
| DATA\_OVERWRITTEN | REQUEST\_RECEIVED | Data was overwritten by something else received from ATS while the WRITE request to partner was in progress. | No | No action needed generally, only FYI for clients. Can be communicated to user only if clients want to give detailed status updates to user. |
| REQUEST\_AT\_GATEWAY |
| PARTNER\_API\_RETRYING |
| PARTNER\_API\_SUCCESS | Partner API succeeded after the ReadStatus was set as DATA\_OVERWRITTEN | No |
| PARTNER\_API\_FAILURE | Partner API failed after the ReadStatus was set as DATA\_OVERWRITTEN | Yes | Partner API failed even after retries. Show failure to user and ask to retry. The failure *might* have been due to stale data, so it is possible that retries may fail as well. |
| DATA\_READ\_CONFIRMED | PARTNER\_API\_SUCCESS | Data received from the partner matches the exported values | Yes | Success. |
| DATA\_READ\_CONFLICT | Data received from the partner does not match the exported value | Not terminal until timeout. Possible to update to DATA\_READ\_CONFIRMED in future reads before timeout | The change was overwritten by the ATS and couldn’t be synced successfully. Suggest user to retry if they are not ok with current state. |
| DATA\_READ\_EXPIRED | No data has been received from the partner for the record for the threshold period of time. | Yes | Change couldn’t be confirmed from the ATS. Client may mark this as failed & suggest the user to retry. |

#### Method : IntegrationApplicationStageExportRequestApi.get

Read after write consistent. The entry will be first written to espresso, followed by returning it as part of the API response.

##### Request : GetRequestStatusRequest

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| requestId | Long | Write Request ID |

##### Response : GetRequestStatusResponse

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| requestId | Long | Write Request ID |
| payload.integrationApplicationUrn | IntegrationApplicationUrn | IP Urn of the application for which new stage is to be upserted |
| payload.newIntegrationJobRequisitionStageUrn | IntegrationJobRequisitionStageUrn | IP Urn of the job requisition stage which should be set as the new stage for the given application. This is selected from the list of stages for the requisition which is associated with the given application. |
| requestStatus.recommendedStatus | SUCCESS / FAILURE / INTERMEDIATE | Recommended status of the request based on read & write status |
| requestStatus.writeStatus | Enum :  REQUEST\_RECEIVED, REQUEST\_AT\_GATEWAY,  PARTNER\_DATA\_VALIDATION\_FAILURE, PARTNER\_API\_RETRYING, PARTNER\_API\_FAILURE, PARTNER\_API\_SUCCESS | Status of the export request write |
| requestStatus.readStatus | DATA\_READ\_PENDING,  DATA\_OVERWRITTEN, DATA\_READ\_CONFLICT, DATA\_READ\_CONFIRMED,  DATA\_READ\_EXPIRED | Status of the data confirmation of the exported values from ATS via ingested data |
| changeTimestamps | ChangeTimestamps (created, modified) | Change timestamps for the record |
| actor | Urn | ViewerUrn of the user who performed this action. May be a seat. |
| requestMetadata.clientEntityUrn |  | ClientEntityUrn associated with this request |

Same can be made available in an **offline dali view**.

#### Method : IntegrationApplicationStageExportRequestApi.findByCriteria

##### Request : FindByCriteriaRequest

| **Field** | **Sub-Field** | **Type** | **Remarks** | **Optional?** |
| --- | --- | --- | --- | --- |
| SearchQuery | integrationApplicationUrn | IntegrationApplicationUrn | Integration Application Urn to which the stage request is associated |  |
|  | clientEntityUrn |  | ClientEntityUrn to which the stage request is associated |  |
| paging |  | PagingContext |  |  |

##### Response : FindByCriteriaResponse

List of values :

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| requestId | Long | Write Request ID |
| integrationApplicationUrn | IntegrationApplicationUrn | IP Urn of the application for which new stage is to be upserted |
| newIntegrationJobRequisitionStageUrn | IntegrationJobRequisitionStageUrn | IP Urn of the job requisition stage which should be set as the new stage for the given application. This is selected from the list of stages for the requisition which is associated with the given application. |
| requestStatus.recommendedStatus | SUCCESS / FAILURE / INTERMEDIATE | Recommended status of the request based on read & write status |
| requestStatus.writeStatus |  | Status of the export request write |
| requestStatus.readStatus |  | Status of the data confirmation of the exported values from ATS via ingested data |
| changeTimestamps | ChangeTimestamps (created, modified) | Change timestamps for the record |
| actor | Urn | ViewerUrn of the user who performed this action. May be a seat or member depending on use case. |
| requestMetadata.clientEntityUrn |  | ClientEntityUrn associated with this request |

### Nearline Status Updates

Integration Platform will process all status updates on export requests in a nearline system which will translate them into the following event which can be consumed by IP Clients like HP.

#### IntegrationApplicationStageExportStatusEvent

| **Field** | **Type** | **Remarks** |
| --- | --- | --- |
| requestID | Long | Write Request ID |
| requestStatus.recommendedStatus | SUCCESS / FAILURE / INTERMEDIATE | Recommended status of the request based on read & write status |
| requestStatus.writeStatus | Enum :  REQUEST\_RECEIVED, REQUEST\_AT\_GATEWAY,  PARTNER\_DATA\_VALIDATION\_FAILURE, PARTNER\_API\_RETRYING, PARTNER\_API\_FAILURE, PARTNER\_API\_SUCCESS | Status of the export request write |
| requestStatus.readStatus | DATA\_READ\_PENDING,  DATA\_OVERWRITTEN, DATA\_READ\_CONFLICT, DATA\_READ\_CONFIRMED,  DATA\_READ\_EXPIRED | Status of the data confirmation of the exported values from ATS via ingested data |
| changeTimestamps | ChangeTimestamps (created, modified) | Change timestamps for the record |
| actor | Urn | ViewerUrn of the user who performed this action. May be a seat or member depending on use case. |
| requestMetadata.clientEntityUrn |  | ClientEntityUrn associated with this request |

## Appendix

[ATS Bi-Directional Sync Principles](https://docs.google.com/document/d/1M3U3ESnfyDtCD_G1Z6n0hTGJZktL8csxJ-N7gy0bhD8/edit?usp=sharing)

[Integrations API Interface](https://docs.google.com/document/d/1XSqmB5iK3DatMmV6cKIBUdU--OcSCpHDXT-Y9fYZshg/edit?usp=sharing)

[PRD: LinkedIn Connected Projects](https://docs.google.com/document/d/1vMl9WFSiUwM7Mm-8S3BqELgQXezSVR2KaD4vaFrJSMM/edit?usp=sharing)

[Connected Projects Phase 2 - Job Requisition Stage Sync Eng Design](https://docs.google.com/document/d/1HDhYoehkySr_Qgi09FI8cXSY4dFYubwNTmfPLHWZ4oc/edit?usp=sharing)

####
