CREATE TABLE checks (
	id SERIAL PRIMARY KEY,
	name VARCHAR,
	query VARCHAR,
	created TIMESTAMP DEFAULT now(),
	author VARCHAR,
	schedule VARCHAR
);

CREATE TABLE runs (
	id SERIAL PRIMARY KEY,
	check_id integer,
	start_dttm TIMESTAMP DEFAULT now(),
	end_dttm TIMESTAMP,
	status VARCHAR(20)
);

CREATE TABLE results (
	run_id integer,
	msg VARCHAR
);
