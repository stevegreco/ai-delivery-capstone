-- Defects on the requirement, or on any test linked to it.
SELECT d.external_id, d.severity, d.status, rl.external_id AS release,
       t.external_id AS test_case, d.summary
FROM defect d
JOIN release rl ON rl.id = d.release_id
LEFT JOIN test_case t ON t.id = d.test_case_id
WHERE d.requirement_id = (SELECT r.id FROM requirement r JOIN project p ON p.id = r.project_id
                          WHERE p.key = :project AND r.external_id = :requirement)
   OR d.test_case_id IN (SELECT l.test_case_id FROM trace_link l
                         JOIN requirement r ON r.id = l.requirement_id
                         JOIN project p ON p.id = r.project_id
                         WHERE p.key = :project AND r.external_id = :requirement)
ORDER BY d.external_id;
