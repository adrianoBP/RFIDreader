CREATE TABLE `rfids_authorizations` (
	`rfids_id`	INTEGER NOT NULL,
	`authorizations_id`	INTEGER NOT NULL,
	FOREIGN KEY(`rfids_id`) REFERENCES rfids(id),
	FOREIGN KEY(`authorizations_id`) REFERENCES authorizations(id),
	PRIMARY KEY (rfids_id, authorizations_id)
);
