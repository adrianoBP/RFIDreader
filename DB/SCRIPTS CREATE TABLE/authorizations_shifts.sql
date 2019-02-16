CREATE TABLE `authorizations_shifts` (
	`authorizations_id`	INTEGER NOT NULL,
	`shifts_id`	INTEGER NOT NULL,
	FOREIGN KEY(`authorizations_id`) REFERENCES authorizations(id),
	FOREIGN KEY(`shifts_id`) REFERENCES shifts(id),
	PRIMARY KEY (authorizations_id, shifts_id)
);
