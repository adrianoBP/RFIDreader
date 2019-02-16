CREATE TABLE `authorizations_days` (
	`authorizations_id`	INTEGER NOT NULL,
	`days_id` INTEGER NOT NULL,
	FOREIGN KEY(`authorizations_id`) REFERENCES authorizations(id),
	FOREIGN KEY(`days_id`)  REFERENCES days(id),
	PRIMARY KEY (authorizations_id, days_id)
);
