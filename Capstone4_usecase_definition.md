# Capstone 4 — AI Delivery Assurance & Test Engineering Copilot
## Use Case Definition

## 1. Purpose

This capstone focuses on building an AI-powered Delivery Assurance and Test Engineering Copilot.

The business objective is to help engineering, product, QA, and delivery teams preserve business intent from requirements through testing and release readiness.

The solution should work across:

- business requirements
- user stories
- acceptance criteria
- API specifications
- non-functional requirements
- test cases
- test execution results
- defects
- release scope
- requirement changes
- traceability links

The key idea is not simply to generate test cases.

The capstone should demonstrate how AI can help answer:

> Are the requirements clear?

> Are the requirements testable?

> Does every important requirement have sufficient test coverage?

> What changed?

> Which tests are now impacted?

> Which failed tests or open defects threaten release readiness?

> Can we trace business intent all the way to validation evidence?

This guide explains the supplied data, the expected business behavior, and how the information is intended to work together.

It intentionally stops short of prescribing the technical implementation.

---


# 1A. Why This Capstone Matters

This capstone is intentionally broader than "AI generates test cases."

The enterprise problem is that business intent is frequently fragmented across requirements, user stories, acceptance criteria, API contracts, non-functional requirements, test assets, defects, change requests, and release evidence. A delivery team may have all of those artifacts and still be unable to answer a simple executive question with confidence:

> "Are we ready to release, and what evidence supports that conclusion?"

The value of the capstone is therefore the full delivery-assurance chain:

```text
Business Intent
      |
      v
Requirement Quality
      |
      v
Traceability
      |
      v
Test Coverage
      |
      v
Execution Evidence
      |
      v
Defects / Change Impact
      |
      v
Release Readiness
```

AI is useful here because much of the delivery estate is semi-structured or unstructured, terminology varies between teams, and important relationships are not always explicitly encoded.

The strongest implementation should demonstrate that AI can help teams:

- find ambiguous or incomplete requirements before they become expensive defects
- connect business intent to acceptance criteria and tests
- identify missing or weak coverage
- detect when a requirement change makes an existing test stale
- combine functional, API, security, and non-functional evidence
- distinguish historical evidence from evidence valid for the current release
- explain why a release is considered ready, risky, or not ready
- do this across different project artifact formats without rewriting the core application

The key learning objective is:

> **AI should preserve business intent from requirement to evidence, not simply produce more artifacts.**

---

# 1B. Dataset Package Structure

The supplied ZIP contains one **reference delivery package** plus three **onboarding/generalization packages**.

The main structure is:

```text
Capstone4_AI_Delivery_Assurance_Test_Engineering_Dataset/
|
|-- README.md
|-- schema_ddl.sql
|
|-- data/
|   |-- requirements.csv
|   |-- acceptance_criteria.csv
|   |-- user_stories.csv
|   |-- api_endpoints.csv
|   |-- test_cases.csv
|   |-- traceability_links.csv
|   |-- test_executions.csv
|   |-- defects.csv
|   |-- requirement_changes.csv
|   |-- release_scope.csv
|   `-- document_registry.csv
|
|-- documents/
|   |-- 01_Commerce_Platform_Product_Requirements.pdf
|   |-- 02_Payments_Refunds_Functional_Specification.pdf
|   |-- 03_Identity_Access_API_and_Security_Specification.pdf
|   |-- 04_Checkout_UI_and_Acceptance_Standards.pdf
|   |-- 05_Release_Governance_and_Test_Strategy.pdf
|   |-- 06_Non_Functional_Requirements_and_SLOs.pdf
|   |-- 07_Change_Request_and_Release_Impact_Bundle.pdf
|   `-- 98_ARCHIVED_Checkout_Requirements_v1.pdf
|
|-- api/
|   |-- openapi_sample.json
|   `-- mock_test_runner_contract.json
|
|-- samples/
|   |-- payment_authorization_request.json
|   `-- payment_authorization_response.json
|
|-- developer_aid/
|   `-- golden_delivery_assurance_scenarios.csv
|
|-- Set_A_Jira_Product_Delivery/
|-- Set_B_Kanban_Service_Modernization/
`-- Set_C_Feature_Portfolio_Mobile_Banking/
```

If the ZIP was created on macOS, it may also contain `__MACOSX` folders or `.DS_Store` files. These are operating-system packaging artifacts and are **not part of the capstone data model**. They can be ignored.

---

# 1C. How the Package Is Intended to Be Used

The main `data/`, `documents/`, `api/`, and `samples/` folders form the **reference project**.

The recommended development sequence is:

```text
Reference Project
      |
      v
Build common ingestion and normalization
      |
      v
Build delivery-assurance capabilities
      |
      v
Validate against Golden scenarios
      |
      v
Onboard Set A
      |
      v
Onboard Set B
      |
      v
Onboard Set C
```

Set A, Set B, and Set C are not intended to become three separate hard-coded applications.

They exist to test whether the architecture generalizes.

The expected principle is:

> **A new project should be onboarded through mapping, configuration, adapters, or normalization - not by adding project-specific business logic to the core application.**

The core application should operate on a common internal delivery model.

A useful conceptual model is:

```text
External Artifact
      |
      v
Source Adapter / Parser
      |
      v
Field / Terminology Mapping
      |
      v
Normalized Delivery Model
      |
      +--> Requirement Analysis
      +--> Traceability
      +--> Test Coverage
      +--> Change Impact
      +--> Release Readiness
```

For example, the reference package may use:

```text
requirement_id
```

while another project may use:

```text
Issue Key
Feature Code
Card ID
Story Ref
```

Those differences should be handled at the onboarding boundary.

They should not require a rewrite of the traceability or release-readiness engine.

---

# 1D. Root-Level Files

## `README.md`

The README is the package orientation document.

It describes:

- the purpose of the dataset
- the approximate size of the structured data
- the role of the PDF corpus
- the Golden evaluation scenarios
- the optional test-runner tool layer
- the intentional difficulty built into the package

Participants should read it before loading the data.

## `schema_ddl.sql`

This file provides a starter relational schema for the reference structured data.

Its purpose is to make it easier to load the supplied CSV files into a relational database.

The schema is a **starting representation**, not a requirement that the final solution must use a relational database for every capability.

For example, a team may choose to use:

- relational tables for structured lifecycle data
- a vector index for documents
- a graph structure for traceability
- another storage approach where justified

---

# 1E. The `data/` Directory

The `data/` directory is the structured delivery-lifecycle evidence for the reference commerce project.

It should be treated as one connected dataset rather than a collection of unrelated CSV files.

## `requirements.csv`

Represents the approved or candidate business/system requirements.

Use it as a primary business-intent source and one of the main traceability anchors.

## `acceptance_criteria.csv`

Contains acceptance criteria associated with requirements or stories.

Some criteria are intentionally weak or ambiguous.

Use this file to test requirement-quality and testability analysis.

## `user_stories.csv`

Contains implementation-facing stories linked to higher-level business intent.

Use it to bridge requirements and delivery work.

## `api_endpoints.csv`

Contains a structured inventory of representative application endpoints.

Use it to connect functional requirements to API behavior and to support API-oriented test generation.

This file is different from `api/openapi_sample.json`:

- `api_endpoints.csv` is structured delivery metadata.
- `openapi_sample.json` is a machine-readable API contract.

## `test_cases.csv`

Contains the existing validation assets.

The dataset intentionally includes coverage gaps.

Do not assume that every requirement has a sufficient test or that every existing test is still valid.

## `traceability_links.csv`

Contains explicit relationships among lifecycle artifacts.

Use it as the starting traceability graph/model.

A team should also be able to detect where relationships are absent, stale, or inconsistent.

## `test_executions.csv`

Contains historical execution evidence.

Use it to distinguish:

```text
Test exists
```

from:

```text
Test passed for the relevant release/build
```

## `defects.csv`

Contains defects associated with tests and/or requirements.

Use defect severity, status, and relationships as part of delivery-readiness reasoning.

## `requirement_changes.csv`

Contains requirement-change events.

Use it for impact analysis and stale-test detection.

The important question is not only:

> "What changed?"

but:

> "Which stories, acceptance criteria, tests, APIs, defects, and release decisions are affected?"

## `release_scope.csv`

Defines which requirements/features are relevant to a release.

Use it as the boundary for readiness analysis.

A defect or uncovered requirement outside the current release should not necessarily have the same effect as one inside the release.

## `document_registry.csv`

Contains metadata describing the PDF corpus.

Use it to preserve information such as:

- document identity
- status
- version
- current/archive state
- domain
- release context

This is particularly important for preventing archived guidance from being selected simply because it is semantically similar to the user's question.

---

# 1F. The `documents/` Directory - Documents 01 through 98

The numbered documents are the unstructured source-of-truth material for the **reference commerce project**.

The numbering does not mean they must always be processed in numerical order.

The numbers make the role of each document easy to identify and preserve source references.

## Document 01 - `01_Commerce_Platform_Product_Requirements.pdf`

### Purpose

This is the high-level product and business-requirement source for the commerce platform.

It covers areas such as:

- checkout business rules
- order lifecycle
- notification expectations
- exceptions and open questions
- relationship between product intent and delivery evidence

### How it should be used

Use this document as a primary source for:

- business intent
- feature requirements
- release context
- requirement clarification
- business-rule traceability

The application should be able to associate structured requirements back to evidence in this source where appropriate.

---

## Document 02 - `02_Payments_Refunds_Functional_Specification.pdf`

### Purpose

This document describes functional behavior for payments and refunds.

It covers areas such as:

- payment authorization
- refund processing
- asynchronous states
- idempotency
- failure and recovery behavior
- audit evidence

### How it should be used

Use it when generating or evaluating:

- payment tests
- refund tests
- negative paths
- timeout/retry behavior
- idempotency tests
- state-transition tests

It is more detailed than the high-level product requirements and therefore demonstrates why delivery assurance often needs evidence from multiple sources.

---

## Document 03 - `03_Identity_Access_API_and_Security_Specification.pdf`

### Purpose

This document provides identity, access, API-security, and authorization requirements.

It covers areas such as:

- authentication
- token behavior
- step-up authentication
- authorization
- failure modes
- security test expectations

### How it should be used

Use it to enrich security-oriented test design and ensure that functional tests do not ignore access-control requirements.

For example, a business flow may be functionally correct but still fail delivery assurance if unauthorized access is possible.

---

## Document 04 - `04_Checkout_UI_and_Acceptance_Standards.pdf`

### Purpose

This document describes UI behavior and acceptance expectations for checkout.

It covers areas such as:

- validation behavior
- error presentation
- transaction uncertainty
- accessibility acceptance
- acceptance evidence

### How it should be used

Use it when assessing whether acceptance criteria and test cases adequately cover:

- user-visible validation
- failure messages
- uncertain transaction states
- accessibility behavior
- UI-level acceptance evidence

This document helps demonstrate that requirements are not limited to backend/API behavior.

---

## Document 05 - `05_Release_Governance_and_Test_Strategy.pdf`

### Purpose

This is the delivery-governance document.

It defines expectations around:

- traceability
- delivery-assurance workflow
- coverage and quality gates
- AI-assisted test generation
- execution evidence
- release-readiness decisions

It also contains a **workflow diagram**.

### How it should be used

This document is especially important because it provides governance rules for interpreting the rest of the evidence.

For example, it helps answer:

- What level of traceability is expected?
- What evidence is sufficient?
- What quality gates apply?
- How should AI-generated tests be governed?
- When should a release be considered ready or not ready?

### Visual workflow requirement

The workflow diagram must be treated as knowledge, not decoration.

A text-only ingestion pipeline may miss or weaken the meaning of:

- stage sequence
- decision points
- quality gates
- pass/fail branches
- exception paths

A team should preserve the workflow meaning in a retrievable representation and retain source/page metadata so the result can be cited back to the PDF.

---

## Document 06 - `06_Non_Functional_Requirements_and_SLOs.pdf`

### Purpose

This document contains non-functional requirements and service-level objectives.

It includes areas such as:

- performance targets
- availability
- resiliency
- observability
- capacity
- degradation behavior

### How it should be used

Use it to ensure the application does not interpret "test coverage" as only functional test coverage.

For example, a checkout feature may pass all business-function tests but still be unready because latency, reliability, or observability requirements are not satisfied.

---

## Document 07 - `07_Change_Request_and_Release_Impact_Bundle.pdf`

### Purpose

This document represents change-governance and impact-analysis material.

It includes changes affecting:

- API contracts
- business rules
- non-functional expectations
- release impact

### How it should be used

Use it to drive change-impact analysis.

The application should identify which downstream artifacts may need reassessment when a requirement changes.

Conceptually:

```text
Change
  |
  +--> Requirement
  +--> Story
  +--> Acceptance Criteria
  +--> API
  +--> Test
  +--> Execution Evidence
  +--> Release Readiness
```

---

## Document 98 - `98_ARCHIVED_Checkout_Requirements_v1.pdf`

### Purpose

This is intentionally archived historical guidance.

It exists to test whether retrieval and reasoning distinguish **current approved requirements** from **obsolete but semantically similar requirements**.

The archived document contains legacy checkout guidance that is no longer valid for current release decisions.

### How it should be used

It should remain available to the retrieval system so the team can prove that:

- the document can be found
- its archive status is known
- current-vs-archived metadata influences retrieval and reasoning
- archived content does not silently override current approved guidance

The goal is not to delete archived evidence.

The goal is to use it correctly.

---

# 1G. The `api/` Directory

The `api/` directory contains two different types of contracts.

They should not be confused.

## `openapi_sample.json`

### What it represents

This file describes the **application being tested**.

It is an OpenAPI-style machine-readable contract for representative commerce endpoints such as:

- cart validation
- checkout submission
- payment authorization
- payment lookup
- refund creation
- refund lookup
- authentication/token behavior
- step-up authentication
- order creation

It includes information such as:

- HTTP method
- endpoint
- operation identifier
- representative response codes
- required headers such as `Idempotency-Key`

### How it should be used

The application can use this contract to:

- understand API surface area
- relate API operations to requirements
- generate candidate API tests
- identify negative/error conditions
- check response-code expectations
- reason about idempotency
- support impact analysis when API behavior changes

Conceptually:

```text
Requirement
   +
OpenAPI Contract
   +
Security / Functional Specification
        |
        v
Candidate API Tests
```

This file is **not the AI tool interface**.

It describes the system under test.

---

## `mock_test_runner_contract.json`

### What it represents

This file describes an **optional testing tool surface available to the AI application**.

It contains representative tools such as:

- `get_test_case`
- `get_requirement_trace`
- `run_test_case`
- `run_test_suite`
- `get_execution_result`
- `create_defect_draft`

It also describes risk levels and whether confirmation is required.

### How it should be used

This contract supports the optional agentic extension of the capstone.

Conceptually:

```text
AI Delivery Assurance Copilot
        |
        v
Approved Test Tool
        |
        v
Test Runner / Test Management System
        |
        v
Execution Result
        |
        v
Delivery Evidence
```

The distinction is:

```text
openapi_sample.json
    -> describes the APPLICATION being tested

mock_test_runner_contract.json
    -> describes the TESTING TOOL the copilot may call
```

A team does not need to hard-code these exact files.

In a real project:

- OpenAPI may come from Swagger, API Gateway, source control, or an engineering portal.
- Test execution may be provided by Playwright, Selenium, Postman/Newman, Jenkins, Azure DevOps, GitHub Actions, a test-management product, or another approved platform.

The architecture should use adapters or connectors so those systems can be replaced without rewriting the core delivery-assurance logic.

---

# 1H. The `samples/` Directory

The `samples/` directory contains representative API payloads.

## `payment_authorization_request.json`

Provides an example request payload for a payment-authorization scenario.

## `payment_authorization_response.json`

Provides an example response payload.

### Why these files matter

An API contract defines schema and operation behavior, but real examples help the AI system and developer understand:

- representative field values
- realistic payload shape
- expected relationships between request and response
- candidate test data
- boundary or invalid-input variants

These samples can be used as additional evidence during API test generation.

They should not be treated as the only valid payloads.

---

# 1I. The `developer_aid/` Directory

## `golden_delivery_assurance_scenarios.csv`

This file contains the Golden evaluation scenarios.

Its purpose is to evaluate the solution against expected delivery-assurance behavior.

The Golden set covers areas such as:

- ambiguity detection
- missing acceptance criteria
- missing test coverage
- traceability
- stale-test detection
- change impact
- current-vs-archived retrieval
- test generation
- non-functional requirements
- failed execution interpretation
- defect impact
- release readiness
- optional agentic test execution

This file should primarily be treated as **evaluation evidence**, not as content that is blindly retrieved to answer user questions.

A team should be able to report performance against the Golden scenarios and compare model/configuration choices.

---

# 1J. Set A, Set B, and Set C - Why They Exist

Set A, Set B, and Set C are deliberately different from the reference project.

Their purpose is to prove that the solution is a reusable **delivery-assurance platform**, not a script that only understands the original filenames and column names.

A strong solution should be able to onboard these sets by changing:

- source adapters
- mapping/configuration
- terminology mapping
- metadata rules

without changing the core logic for:

- requirement quality
- traceability
- test coverage
- impact analysis
- release readiness

These sets can be used as **generalization tests** after the main solution works on the reference dataset.

---

# 1K. Set A - Jira Product Delivery

## Purpose

Set A simulates a team whose delivery process is centered around Jira-style work items.

It tests whether the application can work when the main delivery language is:

- Epic
- Story / issue key
- parent relationship
- issue link
- fix version
- Jira status
- Jira priority

rather than the reference dataset's exact schema.

## Contents

### `jira_issues.csv`

Contains Jira-like issues with fields such as:

- Issue Key
- Issue Type
- Parent
- Summary
- Description
- Priority
- Status
- Fix Version
- Assignee

The application should map these fields into its common requirement/story model.

### `jira_issue_links.csv`

Contains relationships among issues.

Examples include links such as:

```text
implements
```

Use this file to build or enrich traceability relationships.

### `feature_requirements.pdf`

Provides the unstructured feature/business context for the Jira project.

The application should combine the PDF with structured Jira exports rather than treating either one as complete by itself.

### `test_cases.xlsx`

Contains the project's test assets in spreadsheet form.

This intentionally differs from the reference package's CSV representation.

The ingestion layer should normalize it into the common test-case model.

### `release_scope.csv`

Defines which Jira epics/features are in scope and their criticality.

Use it for release-readiness boundaries.

### `api_contract.json`

Provides a small API contract for the Jira-oriented project.

It includes representative checkout and refund endpoints.

Use it to demonstrate that API test generation should work with a different project contract, not only the reference `openapi_sample.json`.

## What Set A should prove

Set A should prove that:

> A Jira export with different field names can be mapped into the same requirement, traceability, test-coverage, and release-readiness capabilities without modifying the core engine.

---

# 1L. Set B - Kanban Service Modernization

## Purpose

Set B simulates a team that does not organize delivery primarily around Jira epics/stories.

Instead, it uses a Kanban board and work-item flow.

It tests whether the application can understand delivery intent when the core vocabulary is:

- Card
- Lane
- Work Type
- Feature
- State
- Blocked
- Definition of Done

## Contents

### `kanban_board.xlsx`

Represents the current Kanban board.

Fields include concepts such as:

- Card ID
- Lane
- Work Type
- Feature
- Priority
- State
- Blocked
- Definition of Done

The application should map Kanban cards into the common delivery model.

### `work_item_history.csv`

Contains state-transition history for the Kanban cards.

Use it to understand lifecycle movement and historical delivery context.

### `test_results.csv`

Contains test execution evidence associated with Kanban cards.

Use it to connect work items with validation evidence.

### `defects.csv`

Contains defects related to Kanban cards.

Use it to assess risk and readiness.

### `acceptance_and_flow_policy.pdf`

Provides the project's acceptance and workflow rules.

This document helps determine what "done" or "acceptable" means in the Kanban environment.

### `release_notes.pdf`

Provides release-oriented context.

Use it to relate completed work and evidence to the delivery/release view.

## What Set B should prove

Set B should prove that:

> The core delivery-assurance model is not dependent on Scrum/Jira terminology.

A card can still represent business intent, acceptance expectations, validation evidence, defects, and release impact.

---

# 1M. Set C - Feature Portfolio / Mobile Banking

## Purpose

Set C simulates a feature-centric product organization in a mobile-banking domain.

It uses different terminology and different file formats from both the reference project and Sets A/B.

The key vocabulary includes:

- Feature Code
- Capability
- Release Train
- Business Priority
- Story Ref
- Feature Ref
- Regression Case
- Change Ref

## Contents

### `feature_catalog.csv`

Contains feature-level portfolio information.

Fields include:

- Feature Code
- Capability
- Outcome
- Release Train
- Business Priority
- Lifecycle

Use it as the feature/business-intent layer.

### `user_story_export.json`

Contains user stories as JSON rather than CSV.

Each story is associated with a feature and includes persona, intent, and acceptance hints.

Some acceptance hints are deliberately weak, such as:

```text
easy and quick
```

Use these to test ambiguity/testability analysis.

### `regression_suite.csv`

Contains regression-test assets linked to features.

Use it for test coverage and historical validation.

### `release_scope.xlsx`

Defines feature-level release scope and required evidence.

It includes concepts such as:

- Train
- Feature
- Required Evidence
- Gate
- Owner

Use it for readiness decisions.

### `change_requests.csv`

Contains feature-level change requests.

Use it for change-impact analysis.

### `product_feature_brief.pdf`

Provides unstructured product context for the mobile-banking feature portfolio.

### `nfr_and_security_requirements.pdf`

Contains non-functional and security requirements.

This separation is intentional.

The application should combine feature, functional, security, and NFR evidence rather than assuming everything is in one source.

## What Set C should prove

Set C should prove that:

> The same delivery-assurance capabilities can operate in a different domain, with feature-centric terminology and a mixture of CSV, JSON, XLSX, and PDF inputs.

---

# 1N. Recommended Use of Set A, B, and C During the Capstone

A useful validation sequence is:

## Stage 1 - Reference Dataset

Build and validate the initial application using the main commerce dataset.

Demonstrate:

- requirement quality
- retrieval
- traceability
- coverage analysis
- test generation
- change impact
- release readiness

## Stage 2 - Set A

Onboard Jira-style artifacts.

Record:

- mappings required
- configuration required
- parser/adapter changes
- whether any core business logic had to change

The target is **no project-specific core logic change**.

## Stage 3 - Set B

Onboard the Kanban project.

This tests whether the architecture has accidentally assumed that every requirement must look like a Jira story.

## Stage 4 - Set C

Onboard the feature-centric mobile-banking project.

This tests both:

- terminology generalization
- domain generalization
- multi-format ingestion

## Expected demonstration

A team should be able to say:

> "The reference project, Jira project, Kanban project, and feature-portfolio project all normalize into the same delivery-assurance model. We changed adapters and mappings, but not the core analysis engine."

That is a much stronger enterprise architecture demonstration than supporting only the supplied reference files.

---

# 1O. Input Contract / New Project Onboarding

The supplied files are one example of a delivery package.

The application should be designed to accept equivalent business artifacts from another project.

## Minimum useful input set

A new project should normally provide enough information to establish:

1. business intent / requirements
2. acceptance expectations or equivalent
3. existing test assets
4. release or delivery scope

## Additional enterprise inputs

Where available, the onboarding process should also support:

- functional specifications
- API contracts
- non-functional requirements
- security requirements
- execution results
- defects
- change requests
- document metadata
- lifecycle history
- release gates

## Common internal model

External artifacts should be normalized into common concepts such as:

```text
Requirement / Feature
User Story / Work Item
Acceptance Criterion
API / Interface
Test Case
Test Execution
Defect
Change
Release
Source Document
Traceability Link
```

The external name does not have to match the internal name.

For example:

```text
Jira Epic
Kanban Card
Mobile Feature
Business Requirement
```

may all represent different levels of delivery intent.

The onboarding layer should map them appropriately.

## What should not happen

The following pattern is discouraged:

```text
if project == "Jira":
    use_jira_business_logic()

if project == "Kanban":
    use_kanban_business_logic()

if project == "MobileBanking":
    use_mobile_banking_business_logic()
```

Instead:

```text
Source-specific parser/mapping
          |
          v
Common Delivery Model
          |
          v
Shared Delivery-Assurance Logic
```

Project-specific handling belongs at the integration and mapping boundary unless the business semantics genuinely require a different rule.

---

# 1P. What the Team Should Be Able to Explain in the Final Defense

The final technical defense should include answers to questions such as:

1. What is your canonical delivery-assurance model?
2. How do you map new project artifacts into it?
3. How do you distinguish requirement, story, feature, card, and acceptance criterion?
4. How do you preserve source provenance?
5. How do you handle current vs archived documents?
6. How do you represent traceability?
7. How do you decide whether a test is stale?
8. How do you combine functional, API, security, and NFR evidence?
9. How do you prevent AI-generated tests from silently redefining business intent?
10. What changes were required to onboard Set A?
11. What changes were required to onboard Set B?
12. What changes were required to onboard Set C?
13. Did any of those onboarding exercises require core business-logic changes?
14. How do you know the system's release-readiness conclusion is correct?
15. What evidence and evaluation results support that conclusion?


# 2. Business Scenario

A product organization is preparing releases for a commerce platform.

The delivery lifecycle includes:

```text
Business Requirement
      |
      v
User Story
      |
      v
Acceptance Criteria
      |
      v
Test Scenario / Test Case
      |
      v
Test Execution
      |
      v
Defect / Evidence
      |
      v
Release Readiness
```

In real delivery environments, this chain frequently breaks.

Examples include:

- a requirement exists but has no acceptance criteria
- acceptance criteria are subjective or not testable
- tests exist but are not linked back to the requirement
- a requirement changes but impacted tests are not updated
- a critical test fails but release status still appears healthy
- archived requirements conflict with current requirements
- non-functional requirements exist separately from functional requirements
- API requirements are documented in a different source than UI requirements
- a defect exists but its relationship to a release-critical requirement is unclear

The goal of the capstone is to use AI to identify and reduce these gaps.

---

# 3. Core Capstone Capabilities

The solution should support several related delivery-assurance capabilities.

## 3.1 Requirement Understanding

The solution should be able to understand requirements from structured and unstructured sources.

It may need to identify:

- requirement identifier
- business objective
- functional area
- priority
- release
- dependencies
- actors
- expected behavior
- constraints
- ambiguity
- missing information

The objective is to improve requirement quality before downstream test generation.

---

## 3.2 Requirement Quality Analysis

The system should identify requirements or acceptance criteria that may be:

- ambiguous
- incomplete
- contradictory
- difficult to test
- missing measurable outcomes
- missing negative/error behavior
- missing security considerations
- missing boundary conditions

For example:

> "The checkout page should be fast and user friendly."

is not directly testable.

The application should be able to identify why and suggest the type of clarification needed.

---

## 3.3 Traceability

Traceability is the core of this capstone.

The system should help connect:

```text
Requirement
    |
    v
Acceptance Criterion
    |
    v
Test Case
    |
    v
Execution Result
    |
    v
Defect / Evidence
```

This should enable questions such as:

- Which requirements have no test coverage?
- Which acceptance criteria have no linked test?
- Which tests validate REQ-104?
- Which requirements are affected by defect DEF-207?
- Which release-critical requirements currently have failed tests?
- Which tests became stale after a requirement change?

---

## 3.4 Test Generation

The application should be able to generate candidate test scenarios or test cases from requirements and acceptance criteria.

Useful test categories may include:

- happy path
- negative path
- boundary conditions
- validation errors
- authorization
- security
- API behavior
- data conditions
- failure scenarios
- non-functional expectations

Generated tests should remain traceable to the requirement or acceptance criterion that motivated them.

The objective is not simply to create a large number of tests.

The objective is to create useful, relevant, reviewable test coverage.

---

## 3.5 Change Impact Analysis

Requirement changes are an important part of the dataset.

When a requirement changes, the solution should help identify:

- impacted user stories
- impacted acceptance criteria
- impacted test cases
- potentially stale tests
- affected API behavior
- affected release scope
- open defects that may need reassessment

Conceptually:

```text
Requirement Change
       |
       v
Identify Changed Intent
       |
       v
Trace Dependencies
       |
       v
Find Impacted Tests
       |
       v
Reassess Coverage
       |
       v
Update Readiness
```

---

## 3.6 Delivery / Release Assurance

The solution should use test results, defects, priority, and traceability to help assess release readiness.

The application may need to identify:

- uncovered critical requirements
- failed tests tied to P0/P1 requirements
- blocked tests
- open severe defects
- missing evidence
- stale tests after a requirement change
- unresolved requirement ambiguity

A release should not be considered ready simply because many tests passed.

The quality of the traceability and the importance of the remaining failures matter.

---

# 4. Structured Data

The package contains structured data representing the delivery lifecycle.

---

## 4.1 `requirements`

### What it contains

This table represents business or system requirements.

Typical fields may include:

- requirement ID
- title
- description
- domain
- priority
- release
- status
- source document
- owner
- risk classification

### Function of the table

This is the primary business-intent layer.

It supports questions such as:

- What is the requirement?
- How important is it?
- Which release contains it?
- Is it currently active?
- Which business area does it affect?

Requirements should act as one of the principal traceability anchors.

---

## 4.2 `user_stories`

### What it contains

This table contains implementation-facing user stories.

Typical information may include:

- story ID
- linked requirement
- persona
- desired capability
- business outcome
- release
- status

### Function of the table

User stories provide a bridge between higher-level requirements and implementable delivery work.

They may expose gaps where a business requirement has not been translated into delivery scope.

---

## 4.3 `acceptance_criteria`

### What it contains

This table contains acceptance criteria linked to requirements or stories.

Typical information may include:

- criterion ID
- linked requirement/story
- acceptance statement
- quality flag
- ambiguity indicator
- testability indicator
- status

### Function of the table

Acceptance criteria define what success should mean.

The supplied data intentionally includes some weak or ambiguous examples.

Participants should consider how AI can identify where criteria need clarification before reliable tests can be generated.

---

## 4.4 `test_cases`

### What it contains

This table represents existing test cases.

Typical information may include:

- test case ID
- title
- test type
- preconditions
- steps
- expected result
- automation status
- priority
- lifecycle status

### Function of the table

This table represents the current validation asset base.

Participants should not assume that all test cases are complete, current, or correctly linked.

The system should be able to reason about missing or weak coverage.

---

## 4.5 `traceability_links`

### What it contains

This table links lifecycle artifacts.

Examples may include:

```text
Requirement -> Acceptance Criterion
Acceptance Criterion -> Test Case
Requirement -> Test Case
Test Case -> Defect
```

### Function of the table

This table forms the starting point for the delivery traceability model.

Participants may use it to identify:

- missing links
- broken chains
- orphan requirements
- orphan tests
- incomplete validation paths

The traceability model may be represented in a relational, graph, or other suitable structure.

---

## 4.6 `test_executions`

### What it contains

This table represents execution results for test cases.

Typical information may include:

- execution ID
- test case ID
- release/build
- execution date
- result
- environment
- duration
- evidence reference

Possible results may include:

- PASS
- FAIL
- BLOCKED
- NOT_RUN

### Function of the table

Execution results provide actual validation evidence.

This table allows the application to distinguish between:

> "A test exists"

and:

> "The requirement has successfully passed validation for the current release."

---

## 4.7 `defects`

### What it contains

This table contains defects discovered during validation.

Typical information may include:

- defect ID
- linked test
- severity
- priority
- status
- release
- summary
- owner

### Function of the table

Defects provide an important input to release readiness.

A release may have broad test coverage but still be unsuitable for release because a failed test is linked to an unresolved high-severity defect.

---

## 4.8 `requirement_changes`

### What it contains

This table represents changes made to requirements.

Typical information may include:

- change ID
- requirement ID
- old behavior
- new behavior
- change reason
- effective release
- change date
- review status

### Function of the table

This table is used for impact analysis.

When a requirement changes, existing tests should not automatically be assumed to remain valid.

The application should help identify which artifacts may need review.

---

## 4.9 `release_scope`

### What it contains

This table defines which requirements or capabilities belong to a release.

Typical fields may include:

- release identifier
- requirement
- feature
- criticality
- planned status
- readiness state

### Function of the table

Release scope provides the boundary for readiness analysis.

It allows the system to distinguish between:

- an issue that matters to the current release
- an issue that belongs to a future release

---

## 4.10 `api_endpoints`

### What it contains

This table describes application APIs.

Typical information may include:

- endpoint
- HTTP method
- service
- authentication requirement
- related requirement
- request/response behavior
- status

### Function of the table

This table supports API-oriented test generation and traceability.

It also allows participants to connect functional requirements to API behavior rather than treating all requirements as UI requirements.

---

## 4.11 `document_registry`

### What it contains

This table describes the supplied document corpus.

Typical fields may include:

- document ID
- title
- document type
- version
- current/archived status
- effective date
- domain
- release
- classification

### Function of the table

The registry provides retrieval metadata and helps the application distinguish:

- current documents
- archived documents
- domain-specific documents
- release-specific guidance

---

# 5. Unstructured Document Corpus

The package includes several PDF documents representing different delivery artifacts.

These include:

- Commerce Platform Product Requirements
- Payments & Refunds Functional Specification
- Identity, Access, API & Security Specification
- Checkout UI & Acceptance Standards
- Release Governance & Test Strategy
- Non-Functional Requirements & SLOs
- Change Request & Release Impact Bundle
- an archived Checkout Requirements document

The corpus is intentionally distributed.

A complete answer may require combining evidence from more than one document.

For example:

- a functional requirement may exist in the Product Requirements document
- the API behavior may exist in the API specification
- the performance requirement may exist in the NFR/SLO document
- the release rule may exist in the Test Strategy document

This is intentional.

---

# 6. Current vs Archived Requirements

The corpus contains archived material.

Archived requirements may be semantically similar to current requirements but contain outdated behavior.

The solution should not blindly use the most semantically similar source.

It should consider document status, version, and effective context.

For example:

```text
Current Requirement v3
       +
Archived Requirement v1
```

If the two conflict, current approved guidance should normally take precedence.

The application should preserve enough source metadata to explain why a source was selected.

---

# 7. Requirement Intelligence

The capstone should support requirement analysis before downstream test generation.

A useful conceptual flow is:

```text
Requirement
    |
    v
Understand Intent
    |
    v
Check Completeness
    |
    v
Check Ambiguity
    |
    v
Check Testability
    |
    v
Identify Missing Information
    |
    v
Generate Clarification / Recommendation
```

The system may classify a requirement as:

- READY
- CLARIFICATION_REQUIRED
- CONFLICT_FOUND
- INCOMPLETE
- NOT_TESTABLE

The exact implementation is left to the team.

---

# 8. Example of Ambiguous Acceptance Criteria

Consider:

> "Checkout should be fast and user friendly."

The statement has two major problems.

### "Fast"

Fast is not measurable unless a threshold is defined.

A better criterion may require:

- a response-time threshold
- a percentile
- a defined workload
- a specific environment

### "User friendly"

This is also subjective unless translated into measurable usability or workflow expectations.

The application should not silently invent business requirements.

It should identify the ambiguity and request clarification or propose a reviewable improvement.

---

# 9. Traceability Model

Traceability is expected to be a first-class capability.

Conceptually:

```text
REQ-104
   |
   +--> AC-104-1
   |       |
   |       +--> TC-204
   |               |
   |               +--> EXEC-881 : PASS
   |
   +--> AC-104-2
           |
           +--> TC-205
                   |
                   +--> EXEC-882 : FAIL
                               |
                               +--> DEF-311
```

This allows the application to answer questions such as:

> Is REQ-104 fully validated?

The answer is not determined merely by whether one linked test passed.

The full chain matters.

---

# 10. Missing Coverage

The supplied data includes requirements that do not have complete test coverage.

The application should identify gaps such as:

```text
Requirement
     |
     v
Acceptance Criteria
     |
     X
No Test Case
```

or:

```text
Requirement
     |
     X
No Acceptance Criteria
```

or:

```text
Requirement
     |
     v
Test Case
     |
     X
No Current Execution Evidence
```

Coverage should therefore be more meaningful than simply counting test cases.

---

# 11. Test Generation

AI-generated test cases should be grounded in the source requirement and related evidence.

For example:

```text
Requirement
+
Acceptance Criteria
+
API Specification
+
Security Constraint
       |
       v
Candidate Test Cases
```

Generated tests should be clearly marked as generated/recommended until reviewed or approved.

Participants should think about quality rather than volume.

Useful questions include:

- Does this test validate a specific requirement?
- Is the expected result measurable?
- Are important negative cases included?
- Are boundary conditions represented?
- Is authorization/security behavior covered?
- Is the test redundant with an existing test?

---

# 12. API Test Generation

The package includes API endpoint information and API-oriented source material.

A requirement may imply tests such as:

- valid request
- invalid request
- missing authentication
- unauthorized role
- invalid data
- duplicate request
- idempotency
- boundary values
- expected error codes
- response schema validation

The application may generate candidate API tests where appropriate.

---

# 13. Non-Functional Requirements

Not all requirements are functional.

The corpus includes non-functional expectations such as:

- performance
- availability
- reliability
- security
- scalability
- recovery behavior

These requirements may require different validation strategies.

For example:

```text
Functional:
"User can submit an order."

Non-Functional:
"Checkout API p95 latency must remain below the approved threshold."
```

The system should avoid treating both as identical test-generation problems.

---

# 14. Change Impact Analysis

A requirement change should trigger analysis of downstream artifacts.

For example:

```text
REQ-220 changed
     |
     +--> Story US-410
     |
     +--> AC-220-1
     |
     +--> TC-701
     |
     +--> TC-702
     |
     +--> API /checkout
```

The application should help determine whether linked tests remain valid.

Possible outputs may include:

- NO_IMPACT
- REVIEW_REQUIRED
- TEST_UPDATE_REQUIRED
- NEW_TEST_REQUIRED
- REQUIREMENT_CONFLICT

The exact labels are not prescribed.

---

# 15. Stale Test Detection

An existing test may have passed previously but still become stale after a requirement change.

This creates an important distinction:

```text
Historical PASS
        !=
Current Requirement Coverage
```

The application should use requirement-change context and traceability to identify tests that may need review.

---

# 16. Delivery Readiness

A delivery-readiness assessment should combine several factors.

Conceptually:

```text
Release Scope
    +
Requirement Quality
    +
Traceability Coverage
    +
Test Execution
    +
Defects
    +
Requirement Changes
       |
       v
Delivery Readiness
```

Possible readiness states may include:

- READY
- READY_WITH_RISK
- NOT_READY
- REVIEW_REQUIRED
- INSUFFICIENT_EVIDENCE

The team may define its own model but should be able to explain it.

---

# 17. Example Release Readiness Question

A stakeholder asks:

> "Can we release checkout this Friday?"

A useful answer should not simply say:

> "92% of tests passed."

Instead, the system should consider:

- whether all P0/P1 requirements are covered
- whether linked critical tests passed
- whether tests are stale after recent requirement changes
- whether blocked tests exist
- whether severe defects remain open
- whether the release-scope requirements have sufficient evidence

The response should provide evidence for the conclusion.

---

# 18. Release Governance Workflow Diagram

The Release Governance and Test Strategy document contains a workflow diagram.

The visual should be treated as part of the knowledge source rather than as decoration.

The developer should preserve the meaning of:

- stage sequence
- decision points
- release gates
- pass/fail paths
- approval or exception paths

A conceptual ingestion approach is:

```text
PDF Page
   |
   +--> Text
   |
   +--> Tables
   |
   +--> Workflow Diagram
              |
              v
      Interpret / Describe
              |
              v
      Structured or Text Representation
              |
              v
      Preserve Page / Section Metadata
              |
              v
      Retrieval
```

The capstone does not prescribe whether the developer uses:

- document-layout extraction
- a vision-capable model
- caption/context extraction
- a graph representation
- a textual workflow representation

The important requirement is that the workflow logic remains retrievable and traceable to the source.

---

# 19. Golden Delivery Assurance Scenarios

The package contains a set of Golden Delivery Assurance scenarios.

These scenarios represent expected behavior for important use cases.

They may test:

- requirement ambiguity detection
- missing acceptance criteria
- missing test coverage
- traceability
- stale-test detection
- change impact
- archived/current document handling
- test generation
- failed test interpretation
- defect impact
- release readiness
- non-functional requirements

The golden set should be used during development and evaluation.

---

# 20. Evaluation

Evaluation should assess more than language quality.

Useful dimensions include:

### Requirement Analysis

- ambiguity detection accuracy
- missing-information detection
- conflict detection
- requirement classification

### Retrieval

- correct source selection
- current vs archived handling
- evidence recall
- citation quality

### Traceability

- correct requirement/test links
- missing-link detection
- stale-link detection
- impacted-artifact identification

### Test Generation

- requirement coverage
- correctness
- non-redundancy
- negative-path coverage
- expected-result quality
- reviewer acceptance

### Delivery Assurance

- readiness decision correctness
- critical-risk detection
- defect impact reasoning
- evidence completeness

---

# 21. Multi-Model Evaluation

The capstone should compare at least two model choices.

Potential evaluation dimensions include:

- requirement-understanding quality
- structured-output reliability
- test-generation quality
- traceability reasoning
- latency
- token usage
- cost
- consistency

The team should be able to defend which model or model combination is best suited to the workload.

---

# 22. TokenOps

The application should measure the cost of its AI workflows.

Relevant token sources may include:

- system instructions
- requirement context
- retrieved documents
- acceptance criteria
- API specifications
- related test cases
- change history
- test execution evidence
- model output

Useful metrics may include:

- tokens per requirement analyzed
- tokens per generated test
- tokens per impact analysis
- tokens per readiness assessment
- latency
- model cost
- cost per accepted test recommendation
- cost per correctly assessed release scenario

The objective is to understand the cost/quality trade-off rather than simply minimize token usage.

---

# 23. Observability

The solution should provide enough operational evidence to understand how an answer or decision was produced.

Useful information may include:

- trace ID
- user question
- retrieved sources
- requirement IDs
- acceptance criteria used
- test cases considered
- traceability path
- requirement changes considered
- model
- token use
- latency
- generated recommendation
- final readiness state

This is important for:

- debugging
- audit
- model evaluation
- quality review
- stakeholder trust

---

# 24. Optional Agentic Validation

The capstone may include an agentic extension.

For example:

```text
Requirement
    |
    v
Identify Candidate Tests
    |
    v
Select Approved Automated Test
    |
    v
Invoke Test Runner
    |
    v
Read Execution Result
    |
    v
Update Delivery Evidence
```

This should be treated as an optional extension rather than the core requirement.

The central value of the capstone remains delivery assurance and traceability.

---

# 25. Human Review

Human review remains important.

The application may recommend:

- rewritten acceptance criteria
- new test cases
- changed traceability links
- requirement clarifications
- release-risk conclusions

These recommendations should remain reviewable.

The AI should not silently redefine business intent.

---

# 26. Example End-to-End Scenario

A requirement changes from:

> "Refunds may be submitted within 30 days."

to:

> "Refunds may be submitted within 14 days for standard customers and 30 days for premium customers."

The application may need to:

1. Detect the changed business rule.
2. Find related user stories.
3. Find related acceptance criteria.
4. Find tests that assume a single 30-day rule.
5. Identify those tests as potentially stale.
6. Recommend new boundary cases.
7. Identify API tests that may be affected.
8. Check whether current release scope includes the feature.
9. Reassess coverage.
10. Explain the impact with traceable evidence.

This is more valuable than simply generating another test case.

---

# 27. What the Capstone Should Demonstrate

At completion, the team should be able to demonstrate that the solution can:

1. Ingest and understand multiple delivery artifacts.
2. Identify ambiguous or incomplete requirements.
3. Retrieve current requirements while avoiding inappropriate archived guidance.
4. Connect requirements, acceptance criteria, tests, executions, and defects.
5. Identify missing test coverage.
6. Generate relevant candidate test scenarios.
7. detect stale tests after requirement changes.
8. perform change-impact analysis.
9. assess delivery/release readiness using evidence.
10. explain why a requirement or release is considered at risk.
11. evaluate AI quality using a Golden scenario set.
12. compare model choices.
13. measure TokenOps.
14. provide traceable operational evidence.

---

# 28. Implementation Freedom

The capstone intentionally does not prescribe:

- database platform
- vector store
- graph database
- embedding model
- LLM provider
- agent framework
- RAG framework
- test-management platform
- UI framework
- observability platform

Teams should choose appropriate technologies and be able to explain their decisions.

The emphasis is on:

- preserving business intent
- requirement quality
- traceability
- test relevance
- change impact
- evidence-based readiness
- evaluation
- explainability
- sound engineering decisions

rather than on using a particular technology stack.
