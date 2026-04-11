Connected Projects Phase 2

- Job Requisition Stage Sync

## Authors

* Yufei Wang (yfwang@linkedin.com)

# Reviewer

| **Approval Role** | **Person (LDAP)** | **Review Status** |
| --- | --- | --- |
| LTS | Xiaoyang Gu | Not Started |
| Hiring Solutions | Xie Lu | Not Started |
| Hiring Platform | Si Chang | Not Started |
| Hiring Platform | Xiaoguang Wang | Not Started |
| Integration Platform | Aditya Hegde | In Progress |
| Integration Platform | Sanjana Vohra | In Progress |
| BuildOut Gateway | Gaurav Sisodiya | Not Started |

# Problem Statement

Enterprise customers increasingly seek unified Talent Acquisition (TA) platforms to streamline their hiring workflows, yet LinkedIn Recruiter risks being viewed solely as a sourcing tool. Today, over 80% of these customers rely on external Applicant Tracking Systems (ATS) as the system of record for job requisitions and applicant management. This disconnected setup creates inefficient workflows, fragmented data, and duplicate tasks between LinkedIn and ATS systems. To address these issues, [**Connected Projects**](https://docs.google.com/document/d/1vMl9WFSiUwM7Mm-8S3BqELgQXezSVR2KaD4vaFrJSMM/edit?tab=t.0) was launched as a key initiative to integrate ATS requisitions with LinkedIn Hiring Projects, enabling recruiters to manage sourcing, applicant evaluation, and pipeline stages in one platform. [**Connected Projects Phase 2: Bidirectional Sync**](https://docs.google.com/document/d/1vMl9WFSiUwM7Mm-8S3BqELgQXezSVR2KaD4vaFrJSMM/edit?tab=t.0#heading=h.vlpnn6ez9g6) of this initiative builds on top of foundational MVP and Phase 1 capabilities by focusing on real-time updates and bi-directional synchronization, ensuring ATS and LinkedIn data remain aligned with minimal manual intervention.

# Product Requirements

**Connected Projects Phase 2: Bidirectional Sync** delivers seamless pipeline and stage synchronization between LinkedIn Hiring Platform and ATS workflows by introducing the following capabilities:

### Pipeline Synchronization

* + Surface ATS requisition stages within the Connected Project pipeline, ensuring ATS is the priority system for maintaining stage accuracy and preserving all candidate stage history.

### Bidirectional Updates

* + Synchronize new ATS stages automatically with Hiring Platform pipelines.
  + Enable Hiring Platform introduced stages to sync back to the ATS, contingent on the ATS’s API support for new stage creation (e.g., Greenhouse currently does not support this).

### Enhanced Stage Management

* + Allow recruiters and LinkedIn Hiring Assistant (LiHA) to move sourced candidates and applicants through ATS-representative stages in Connected Projects.

### Real-Time Updates

* + Reflect candidate stage updates originating in either ATS or LinkedIn Recruiter in the counterpart system to keep hiring workflows in sync.

### Centralized Candidate History

* + Provide complete stage movement history for candidates across the “Most Recent Activity” and “Projects” tabs within LinkedIn Recruiter, as well as in RSC Profile Widgets.

### Unified Reporting

* + Showcase ATS stages in pipeline and activity reports, capturing stage change actions initiated in either ATS or Hiring Platform.

This comprehensive bidirectional synchronization ensures up-to-date, consistent pipelines between LinkedIn and ATS, reducing manual effort while empowering recruiters with reliable data to make timely decisions.

# Architecture

The diagram presents the overall architecture and its principal components. All microservices shown are either pre‑existed or were delivered with the Connected Projects MVP. For Phase 2, we will extend the existing system with minimal, targeted changes to support the required functionalities.

![](data:image/png;base64...)

*Pic 1: Overview of the Architecture with Major Service Components*

At the core, hp-ats-integration-mt orchestrates between the Hiring Platform (HP) and the Integration Platform (IP), which interfaces with ATS partners. It serves two roles:

(1) a data sync pipeline that consumes IntegrationEntityReadyEvent from IP to create/update corresponding HP entities;

(2) an API server (e.g., /connectedProjectsApi) used by HP systems to create and fetch Connected Projects and related data. With phase 2, all the updates initiated from HP that need to be written back to ATS will be hosted in this service (shown in red).

The service coordinates via gRPC with HP backend systems, by calling mcm-mt for hiringProject and hiringPipeline operations and IP backend systems talent-partner-integrations-mt for partner‑facing APIs such as entity mapping and requisition stages.

Recruiter interactions occur in talent-solutions-web, which invokes talent-solutions-api for connection with backend logic. Stage changes initiated in Recruiter are written back to partners through new IP‑backed APIs. A periodic mcm-offline reconciliation flow compares HP and IP data and, on inconsistencies, publishes IntegrationEntityReadyEvent via KafkaPushJob for the data sync pipeline.

Overall, the architecture demonstrates a modular design with clear responsibilities across services to enable bidirectional stage sync and a unified Connected Project experience.

# User Flows

## Initial Sync of Job Requisition Stages

![](data:image/png;base64...)

*Pic 2: Design Mock for Connected Project Creation Modal*

This picture shows the latest design mock for connected project creation modal. There is a new section added to the existing flow, which is the “ATS pipeline automation settings”. This is similar to the autoPipeline feature we have today for sourcing hiring pipeline, where for example if a recruiter sends an InMail to a candidate, if autoPipeline enabled, the candidate gets moved into “Contacted” state automatically. This “ATS pipeline automation settings” can be set for each Connected Project, where users can specify which ATS stage applicants are moved to when the recruiter sends them an InMail. We plan to support two automations for now, one is when InMails are sent to ATS applicants, the other is when applicants reply to the InMail. Users can set or unset each individual automation, and from the dropdown list, we show all the stages associated with the job requisition, for which the Connected Project is created off. Also note that this setting is independent of the contract level autoPipeline setting.

![](data:image/png;base64...)

*Pic 3: Flow Chart for Connected Project Creation with Job Req Stages Sync*

Step 1 is ts-web will call talent-middleware-api a new API to fetch all stages for specified job requisition, which will in turn call the corresponding backend new API to get the data. This will populate the dropdown list for all possible job requisition stages the user can select from.

Before that, our system will do our suggestions for users, which is not shown in the mock. For each of the automation, we will pick one job requisition stage for the user by mapping the stage names against our HireStatusType. If users find our suggestion accurate, it can save users a couple clicks, and finish project creation faster. This is shown by step 2, 3, 4 and 5. Ts-web will call a new method we support in /talentConnectedProjects to get atsPipelineAutomationSuggestions for specified job requisition and hiring project. Ts-api will call a new method we support in /hpIntegrationStageMappingApi to findOrCreate stageMapping for the job requisition and contract. Hp-ats-integration-mt on receiving this call, will first look up the DB table in HiringPlatformIntegrationDB, if stageMappings have been created, it will return directly; otherwise, it will call LLM backed API /processStageMappingApi in talent-copilot-service to get a mapping between job requisition stage name and candidateHiringStateUrn, and store it in HiringPlatformIntegrationDB for reusability.

Once users finalize the selection and click the “Connect Project” button, we will trigger the connected project creation flow as what is happening today, just in addition, pass along the ATS pipeline automation settings. This is shown by step 6, 7, 8, 9 and 10. Ts-web will call /talentConnectedProjects create method, and ts-api will call /connectedProjectsApi create method. We will update both the frontend and backend connectedProject data model to carry the atsPipelineAutomationSettings information. In addition to what is happening today during connectedProject creation to get integrationJobRequisition, update hiringProject and store entityMapping between the two, we will call the new API /integrationJobRequisitionStageApi to get all stages belong to the job requisition in step 8, then call /candidateHiringPipelines in step 9 to create a new hiringPipeline instance with one hiringState for each jobRequisitionStage as a non-global state. We will store the newly created candidateHiringPipelineUrn in a new field of hiringProject named atsPipelineUrn. Then we will call /integrationEntityUrnToClientEntityUrnMappingApi in step 8 to create entityMapping for each pair of candidateHiringStateUrn and integrationJobRequisitionStageUrn present in the pipeline. Lastly, in step 10, we will store the atsPipelineAutomationSettings by calling /hiringProjectPreferences in hire-access-control as a project level setting.

## Move ATS Applicants in Recruiter

![](data:image/png;base64...)

*Pic 4: Design Mock for Pipeline Page and Change Applicant Stage*

This picture shows the latest design mock for pipeline page and changing of ATS applicant stage within Recruiter. For all Connected Projects, on the left rail, we will show the HP sourcing stages first. These are the same stages as it in all other Recruiter projects, which are from the one hiring pipeline template shared by the contract. The behavior of the HP sourcing stages for Connected Projects will be consistent with the existing Recruiter projects. HP sourcing stages are followed by all stages synced from the ATS job requisition in their own section. On the right hand side, it is showing some ATS applicants, who can only be moved into stages synced from ATS, rather than any HP sourcing stages. This is to avoid the applicant stage going out of sync between HP and ATS, as most major ATS that we are partnering with do not support creating new stages by API. When ATS applicants move to a different ATS stage within Recruiter, we will sync this stage movement to ATS via a new write back API supported by IP.

![](data:image/png;base64...)

*Pic 5: Flow Chart for Applicant Stage Movement in Pipeline*

Step 1 and 2 shows the flow for displaying the new section of stages synced from ATS, where ts-web will call /talentHiringProjects get method, and ts-api will call /h iringProjects to get fully decorated atsPipeline with an array of candidateHiringState items.

Step 3, 4, 5 and 6 shows the flow when moving ATS applicants into a different ATS synced stage within Recruiter. Ts-web will call /talentHiringProjectCandidates and ts-api will call /hiringProjectCandidates to partialUpdate the candidateHiringState value. Before recording the state change, mcm-mt will detect if the state change is in a Connected Project, and will call a new API in hp-ats-integration-mt to write back the state change on hiringProjectCandidate. Then hp-ats-integration-mt will look up the entityMapping table for both the application and jobRequisitionStage, and translate into IP terms and call a new write back method in /integrationApplicationStageApi. If the write back fails, we will fail the state update itself on hiringProjectCandidate.

## Move Sourced Candidates in Recruiter

![](data:image/png;base64...)

*Pic 6: Design Mock for Pipeline Page and Change Sourced Candidate Stage*

This picture shows a similar page as previous for hiring pipeline within a Connected Project. On the right hand side, it is showing some sourced candidates instead, who can be moved across the pipeline to any HP sourcing stages or stages synced from ATS. We have a contract level (or contract+ATS level, TBD) setting of “export sourced candidate to ATS pipeline stages”. If the setting is turned on, and the user has unused credit towards one click export, when sourced candidate is moved from an HP sourcing stage into a stage synced from ATS, we will perform one click export on the candidate to the associated job requisition in ATS. The credit usage for the current period towards one click export is displayed on the page above the candidate section.

![](data:image/png;base64...)

*Pic 7: Flow Chart for Candidate Stage Movement in Pipeline*

Step 1 and 2 shows the flow to surface the one click export credit limit and usage for the viewer seat of the current month. Today, the limit is enforced on seat level by utilizing the fuseCounts service. However, users aren’t aware of the usage numbers until the limit is hit. We will need to expose a new API for ts-web to surface it to users.

Step 3 ~ 9 shows the flow to move a sourced candidate from an HP sourcing stage to an ATS synced stage. Step 3, 4 and 5 is consistent with moving stages for applicants synced from ATS.

From hp-ats-integration-mt, it will detect if this is a sourced candidate or a synced applicant, and handle differently. Step 6, it will check the setting of “export sourced candidate to ATS pipeline stages”. Depending on if it will be a contract level setting or contract+ATS level setting, we will store it in hire-access-control or a new DB table that we support from HiringPlatformIntegrationDB. If the setting is turned on, we will call ats-middleware to export the candidate through one click export, whose functionality will also need some updates. One is to move the fuseCounts enforcement from API layer to backend. The other is to support exporting the stage information to the prospect in ATS.

## User Add/Delete/Update Stage in ATS

![](data:image/png;base64...)

*Pic 8: Example UX from Greenhouse to Update Job Req Stage*

User experience and functionality supported would be different for each partner ATS. This picture shows the Greenhouse UX as an example for updating job requisition stages in ATS. From this screen, users can add a stage, remove a stage or update type, name, ordering of a stage.

![](data:image/png;base64...)

*Pic 9: Flow Chart for Syncing Updates of Job Req Stage from ATS*

When such updates happen in ATS, IP will receive it through build-out and send IntegrationEntityReadyEvent from talent-partner-integrations-nearline. Which our data sync pipeline in hp-ats-integration-mt will consume, and we will retrieve corresponding entityMapping, compare the stage entities between HP and IP. Then update entityMapping and candidateHiringState accordingly.

# Major Components to Change

## Sync ATS Job Requisition Stages

1. Update /hiringProjects resource and DB table to support a new field as atsPipelineUrn, which stores the Urn of the CandidateHiringPipeline instance created from ATS job requisition stages.
2. Update /candidateHiringStates resource and DB table to support a new field to differentiate ATS synced states.
3. Update /candidateHiringStates resource and DB table to support non-global pipeline state for states synced from ATS job requisition stages.
4. Update /connectedProjectsApi creation flow to handle getting a list of ATS stages and creating CandidateHiringPipeline instances with non-global pipeline states.
5. Update data sync pipeline to handle update/addition/deletion of a job requisition stage.
6. Update /talentHiringProjects in ts-api to display ATS stages.

## Sync Candidate State Movements

1. Update HiringProjectCandidate resource, when applicants in Connected Projects change pipeline state, also call write back API (new) in hp-ats-integration-mt.
2. Support write back API in hp-ats-integration-mt for each entity that can be written back to ATS, and call corresponding write back API in IP (talent-partner-integrations-mt).
3. Update ApplicationStage data sync pipeline, to move HiringProjectCandidate to proper HP stage.
4. Update data sync pipeline to support syncing of application stage history to HP.

## ATS Pipeline Automation

1. Update /connectedProjectsApi to carry information of “ATS pipeline automation” settings.
2. Update autoPipeline handling logic to move applicants down the atsPipeline based on the “ATS pipeline automation” settings.
3. Update HiringProjectPreference data model, API and DB table in hire-access-control to persist user’s automation preferences per hiring project.
4. Update /hpIntegrationStageMappingApi and /processStageMappingApi to be able to take a list of ATS stages (or raw strings) and a list of HP states and suggest mapping between the two lists. [P1]
5. Update /processStageMappingApi logic to be able to map to more HireStatusType. [P1]
6. Need to handle old stageMappings stored.

## Export Sourced Candidates

1. New resource and DB table to read/write contract + ATS level setting “export sourced candidates to ATS pipeline stages”.
2. Update ts-api to support read/write of the setting.
3. Logic in /connectedProjectCandidatesApi to handle exporting sourced candidates with stage information.

## Offline Validation and Fix Flow

1. Build offline flow to calculate consistency on job requisition stages.
2. Build offline flow to calculate consistency on application stage history.

# Dependencies

1. New API /integrationJobRequisitionStageApi to get and findByJobRequisition for job requisition stage data.
2. New API /talentIntegrationJobRequisitionStages to findByJobRequisition for job requisition stage data.
3. Send IntegrationEntityReadyEvent with entity IntegrationJobRequisitionStage when job requisition stage is added/deleted/updated in ATS.
4. Update /integrationEntityUrnToClientEntityUrnApi and underlying storage to support mapping between IntegrationJobRequisitionStageUrn and CandidateHiringStateUrn.
5. Build-out to have JobRequisitionStage data ingested from ATS.
6. Offline dataset available for JobRequisitionStage and Mapping.
7. New method in API /integrationApplicationStageApi to support write back of application stage movement from HP.
8. Build-out to have the stage movement reflected in ATS.
9. New API /talentExportCandidateCredits in talent-middleware-api to surface the monthly credit usage toward one click export for logged-in user.
10. Update one click export to support prospect stage update.

# Appendix

## Implementation details

talent-solutions-api

ConnectedProject.proto

- atsPipelineAutomationSettings

/talentConnectedProjects

@Action getAtsPipelineAutomationSuggestions(HiringProjectUrn, IntegrationJobRequisitionUrn)



hp-ats-integration-mt:

ConnectedProject.proto

- atsPipelineAutomationSettings

/hpIntegrationStageMappingApi

@Action findOrCreateByJobRequisition(IntegrationJobRequisitionUrn, ContractUrn)

/applicationStageApi

partialUpdate(hiringProjectCandidateUrn, candidateHiringStateUrn)



mcm-mt:

HiringProject.proto

- atsPipelineUrn



hire-access-control:

[HiringProjectPreference.proto](https://jarvis.corp.linkedin.com/codesearch/result/?name=HiringProjectPreference.proto&path=hire-access-control-api%2Frest-api%2Fsrc%2Fmain%2FdataProto%2Fproto%2Fcom%2Flinkedin%2Fhire%2Fpreference&reponame=linkedin-multiproduct%2Fhire-access-control-api)

- atsPipelineAutomationPreferenceValue


