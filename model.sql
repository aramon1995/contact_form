CREATE TABLE contacts (
    CONTACT_NAME VARCHAR(100) PRIMARY KEY,
    BIRTHDATE DATE NOT NULL,
    CONTACT_TYPE ENUM('contact_type1', 'contact_type2','contact_type3'),
    PHONE VARCHAR(10),
    DESCR MEDIUMTEXT
)