-- QUERY 1: THE HIGH PERFORMERS
-- Hypothesis: Students with scores > 90 will have significantly higher click volumes.
SELECT 
    s.id_student,
    s.gender,
    s.highest_education,
    c.code_module AS course_name,
    r.score AS final_exam_score,
    COUNT(v.id_site) AS total_clicks
FROM students s
JOIN student_results r ON s.id_student = r.id_student
JOIN assessments a ON r.id_assessment = a.id_assessment
JOIN courses c ON a.code_module = c.code_module
LEFT JOIN student_clicks v ON s.id_student = v.id_student 
                           AND c.code_module = v.code_module
WHERE c.code_module = 'AAA'
GROUP BY 
    s.id_student, s.gender, s.highest_education, c.code_module, r.score
ORDER BY 
    final_exam_score DESC
LIMIT 20;

-- QUERY 2: THE AT-RISK STUDENTS
-- Hypothesis: Students with failing scores will show minimal platform engagement.
SELECT 
    s.id_student,
    s.gender,
    s.highest_education,
    c.code_module AS course_name,
    r.score AS final_exam_score,
    COUNT(v.id_site) AS total_clicks
FROM students s
JOIN student_results r ON s.id_student = r.id_student
JOIN assessments a ON r.id_assessment = a.id_assessment
JOIN courses c ON a.code_module = c.code_module
LEFT JOIN student_clicks v ON s.id_student = v.id_student 
                           AND c.code_module = v.code_module
WHERE c.code_module = 'AAA'
GROUP BY 
    s.id_student, s.gender, s.highest_education, c.code_module, r.score
ORDER BY 
    final_exam_score ASC
LIMIT 20;