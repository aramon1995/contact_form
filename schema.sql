CREATE TABLE contacts (
    id int PRIMARY KEY AUTO_INCREMENT,
    contact_name VARCHAR(100),
    birthdate DATE NOT NULL,
    contact_type ENUM('contact_type1', 'contact_type2','contact_type3') NOT NULL,
    phone VARCHAR(10),
    descr MEDIUMTEXT
)