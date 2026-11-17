-- The requirement itself.
SELECT r.external_id, r.title, r.priority, r.status, r.approval_status
FROM requirement r
JOIN project p ON p.id = r.project_id
WHERE p.key = :project AND r.external_id = :requirement;
