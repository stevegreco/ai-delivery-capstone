-- The coverage path (ADR 0002): trace_link -> test, with the AC it verifies (if any).
SELECT l.external_id AS link, l.status AS link_status,
       a.external_id AS acceptance_criterion,
       t.external_id AS test_case, t.status AS test_status
FROM trace_link l
JOIN requirement r ON r.id = l.requirement_id
JOIN project p ON p.id = r.project_id
JOIN test_case t ON t.id = l.test_case_id
LEFT JOIN acceptance_criterion a ON a.id = l.acceptance_criterion_id
WHERE p.key = :project AND r.external_id = :requirement
ORDER BY t.external_id;
