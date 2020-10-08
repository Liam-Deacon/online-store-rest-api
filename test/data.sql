/* Add a test user - with sha256 hashed password of 'test' */
INSERT INTO users (username, password, email)
VALUES (
    'test',
    '$pbkdf2-sha256$29000$GiPk/H/P.R9jDOHcO6f0vg$d1hc5fqAKcY92Xpd9BccjpMzHSEVWKk4pIc4PN0HLCQ',
    'test@test.com'
);
VALUES (
    'testuser',
    '$pbkdf2-sha256$29000$GiPk/H/P.R9jDOHcO6f0vg$d1hc5fqAKcY92Xpd9BccjpMzHSEVWKk4pIc4PN0HLCQ',
    'testuser@test.com'
);

/* add a dummy gift list */
INSERT INTO gift_lists (id, user_id)
VALUES (1, 2);
INSERT INTO gift_lists (id, user_id)
VALUES (2, 1);

INSERT INTO gifts (id, item_id, list_id, available, purchased)
VALUES (1, 1, 1, 1, 0);
INSERT INTO gifts (id, item_id, list_id, available, purchased)
VALUES (2, 2, 1, 2, 0);