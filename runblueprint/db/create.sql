-- The database creation script

-- The runners form data
CREATE TABLE runner_profile (
    id bigserial primary key,
    name text NOT NULL,
    race_dist integer,
    date_submitted timestamp default NULL
);
