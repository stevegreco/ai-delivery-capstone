-- Which releases the requirement is scoped into.
SELECT rl.external_id AS release, rs.in_scope, rs.release_blocking
FROM release_scope rs
JOIN requirement r ON r.id = rs.requirement_id
JOIN project p ON p.id = r.project_id
JOIN release rl ON rl.id = rs.release_id
WHERE p.key = :project AND r.external_id = :requirement
ORDER BY rl.external_id;
