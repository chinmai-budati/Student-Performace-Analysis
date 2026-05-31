CREATE DATABASE student_analytics_db;
USE student_analytics_db;

CREATE TABLE Students (
    id_student INT PRIMARY KEY,
    gender VARCHAR(10),
    region VARCHAR(50),
    highest_education VARCHAR(50),
    imd_band VARCHAR(20),
    age_band VARCHAR(20),
    num_of_prev_attempts INT,
    studied_credits INT,
    disability VARCHAR(10),
    final_result VARCHAR(20)
);

CREATE TABLE Courses (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    module_presentation_length INT,
    PRIMARY KEY (code_module, code_presentation)
);

CREATE TABLE Registrations (
    id_student INT,
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    date_registration INT,
    date_unregistration INT,
    PRIMARY KEY (id_student, code_module, code_presentation),
    FOREIGN KEY (id_student) REFERENCES Students(id_student),
    FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE Assessments (
    id_assessment INT PRIMARY KEY,
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    assessment_type VARCHAR(20),
    date INT,
    weight FLOAT,
    FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE Student_Results (
    id_assessment INT,
    id_student INT,
    date_submitted INT,
    is_banked INT,
    score FLOAT,
    PRIMARY KEY (id_assessment, id_student),
    FOREIGN KEY (id_assessment) REFERENCES Assessments(id_assessment),
    FOREIGN KEY (id_student) REFERENCES Students(id_student)
);

CREATE TABLE VLE_Materials (
    id_site INT PRIMARY KEY,
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    activity_type VARCHAR(50),
    week_from INT,
    week_to INT,
    FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);

CREATE TABLE Student_Clicks (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_student INT,
    id_site INT,
    date INT,
    sum_click INT,
    FOREIGN KEY (id_student) REFERENCES Students(id_student),
    FOREIGN KEY (id_site) REFERENCES VLE_Materials(id_site),
    FOREIGN KEY (code_module, code_presentation) REFERENCES Courses(code_module, code_presentation)
);
