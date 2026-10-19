# Capstone 4 - AI Delivery Assurance & Test Engineering Copilot

## Package purpose
This dataset supports a 2026-style enterprise delivery-assurance capstone. It combines multi-document requirements, structured traceability, acceptance criteria, tests, executions, defects, change requests, release scope, and an optional mock test-runner tool surface.

The core challenge is to preserve business intent from requirement through evidence rather than simply generating test cases.

## Structured data
- requirements.csv: 135 requirements across 8 epics
- acceptance_criteria.csv: 421 acceptance criteria, including deliberately ambiguous examples
- user_stories.csv: 110 linked user stories
- api_endpoints.csv: 11 representative endpoints
- test_cases.csv: 183 existing tests with intentional coverage gaps
- traceability_links.csv: 183 requirement/acceptance/test links
- test_executions.csv: 569 historical executions
- defects.csv: 114 defects linked to tests and requirements
- requirement_changes.csv: 45 change requests
- release_scope.csv: 135 release-scope records
- document_registry.csv: 8 source documents with status/version metadata

## PDF corpus
The documents are intentionally overlapping and enterprise-style. Current and archived content coexist so retrieval must consider status/version, not similarity alone.

The release-governance document includes a workflow diagram so teams must consider ingestion of text, tables, and visuals.

## Developer aid
`developer_aid/golden_delivery_assurance_scenarios.csv` contains 30 evaluation scenarios spanning ambiguity, traceability, test generation, NFRs, version conflicts, change impact, agentic execution, defects, and release readiness.

## Optional tool layer
`api/mock_test_runner_contract.json` describes a small tool surface for optional agentic test execution. `api/openapi_sample.json` provides a machine-readable sample API contract.

## Intentional difficulty
The package includes:
- ambiguous acceptance criteria
- current vs archived conflicting guidance
- P0/P1 requirements with missing active tests
- tests that may become stale after requirement changes
- failed/blocked executions
- open defects of different severities
- requirements spread across business, API, security and NFR documents
- visual workflow content inside a PDF

Participants should be able to explain how they distinguish requirement quality, coverage, test quality, execution evidence and release readiness.
