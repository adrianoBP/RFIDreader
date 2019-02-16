CREATE TABLE `accesses` (
	`id`	INTEGER NOT NULL,
	`logDateTime`	DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')),
	`rfids_id`	INTEGER NOT NULL,
	`rfidActive`	INTEGER NOT NULL DEFAULT 0,
	`processed`	BOOLEAN NOT NULL DEFAULT 0,
	PRIMARY KEY(id),
	FOREIGN KEY(`rfids_id`) REFERENCES rfids ( id )
);
