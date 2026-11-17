-- Runs of the tests linked to the requirement, newest first per test.
SELECT t.external_id AS test_case, e.external_id, rl.external_id AS release,
       e.environment, e.executed_at, e.outcome
FROM test_execution e
JOIN test_case t ON t.id = e.test_case_id
JOIN release rl ON rl.id = e.release_id
WHERE t.id IN (SELECT l.test_case_id FROM trace_link l
               JOIN requirement r ON r.id = l.requirement_id
               JOIN project p ON p.id = r.project_id
               WHERE p.key = :project AND r.external_id = :requirement)
ORDER BY t.external_id, e.executed_at DESC;
