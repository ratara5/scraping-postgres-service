-- Create the table contacts
CREATE TABLE IF NOT EXISTS contacts (
    id_contact SERIAL PRIMARY KEY,
    name VARCHAR(255),
    phone_number VARCHAR(20)
);

-- Create the table roles
CREATE TABLE IF NOT EXISTS roles (
    id_role SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Create the table students
CREATE TABLE IF NOT EXISTS students (
    id_student SERIAL PRIMARY KEY,
    name VARCHAR(255),
    last_name VARCHAR(255),
    genre CHAR(1),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
    id_role INTEGER REFERENCES roles(id_role),
    id_contact INTEGER REFERENCES contacts(id_contact)
);

-- Create the table readings
CREATE TABLE IF NOT EXISTS readings (
    date DATE PRIMARY KEY,
    reading VARCHAR(100)
);

-- Create the table assignments
CREATE TABLE IF NOT EXISTS assignments (
    id_assignment SERIAL PRIMARY KEY,
    section VARCHAR(255),
    name VARCHAR(255),
    date DATE,
    CONSTRAINT "fk_fd"
        FOREIGN KEY ("date")
        REFERENCES readings ("date")
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

-- Create the table that associates students with assignments (many-to-many relationship)
CREATE TABLE IF NOT EXISTS students_assignments (
    id_student INTEGER, -- INTEGER REFERENCES students(id_student), -- it's redundant
    id_assignment INTEGER, -- INTEGER REFERENCES assignments(id_assignment), -- it's reduandant
    PRIMARY KEY ("id_student", "id_assignment"),
    room VARCHAR(20),
  CONSTRAINT "fk_STUDENTS_ASSIGNMENTS_STUDENTS1"
    FOREIGN KEY ("id_student")
    REFERENCES students ("id_student")
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT "fk_STUDENTS_ASSIGNMENTS_ASSIGNMENTS1"
    FOREIGN KEY ("id_assignment")
    REFERENCES assignments ("id_assignment")
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);