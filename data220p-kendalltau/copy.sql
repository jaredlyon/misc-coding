SELECT
    state,
    institutional_control,
    COUNT(*) AS num_universities,
    AVG(tuition) AS avg_tuition,
    AVG(acceptance_rate) AS avg_acceptance_rate,
    AVG(enrollment) AS avg_enrollment
FROM usnews_university_rankings
GROUP BY state, institutional_control WITH ROLLUP;