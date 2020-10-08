/* Add a test user - with sha256 hashed password of 'test' */
INSERT INTO users (username, password, email)
VALUES (
    'test',
    '$pbkdf2-sha256$29000$GiPk/H/P.R9jDOHcO6f0vg$d1hc5fqAKcY92Xpd9BccjpMzHSEVWKk4pIc4PN0HLCQ',
    'test@test.com'
);