-- The requirement's acceptance criteria.
SELECT a.external_id, a.status, a.criterion_type, a.criterion
FROM acceptance_criterion a
JOIN requirement r ON r.id = a.requirement_id
JOIN project p ON p.id = r.project_id
WHERE p.key = :project AND r.external_id = :requirement
ORDER BY a.external_id;
