import sqlite3
conn = sqlite3.connect("../DB/accesses.sqlite")
c=conn.cursor()
res=c.execute('''

	SELECT accesses.id AS accesses_id,
		accesses.logDateTime AS accesses_logDateTime,
		rfids.code AS rfids_code,
		(CASE WHEN t2.authId IS null THEN 0 ELSE 1 END) AS accessAuthorized,
		t2.authId AS authorizations_id
	FROM rfids, accesses LEFT JOIN (
		SELECT accesses.id AS access_id, t1.authId AS authId
		FROM authorizations, rfids_authorizations, rfids, accesses, (
			SELECT authorizations.id AS authId,
				CAST(authorizations_days.days_id as string) AS dayId,
				strftime("%H-%M", shifts.startTime) AS shiftStart,
				strftime("%H-%M", shifts.endTime) AS shiftEnd
			FROM authorizations, authorizations_days, authorizations_shifts, shifts
			WHERE authorizations.id=authorizations_days.authorizations_id
				AND authorizations.id=authorizations_shifts.authorizations_id
				AND authorizations_shifts.shifts_id=shifts.id
			) AS t1
		WHERE t1.authId=rfids_authorizations.authorizations_id
			AND authorizations.id=rfids_authorizations.authorizations_id
			AND rfids_authorizations.rfids_id=rfids.id
			AND rfids.id=accesses.rfids_id

			AND strftime("%Y-%m-%d", accesses.logDateTime) BETWEEN strftime("%Y-%m-%d", authorizations.startDateTime) AND strftime("%Y-%m-%d", authorizations.endDateTime)
			AND strftime("%w", accesses.logDateTime) = t1.dayId
			AND strftime("%H-%M", accesses.logDateTime) BETWEEN t1.shiftStart AND t1.shiftEnd
			AND accesses.rfidActive=1

	) AS t2 ON accesses.id=t2.access_id
	WHERE rfids.id=accesses.rfids_id
	ORDER BY accessAuthorized, accesses_logDateTime

''')
for row in res:
	print row
conn.commit()
conn.close()
