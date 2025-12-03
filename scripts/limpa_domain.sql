SELECT id, active, "name" FROM "domain" d ORDER BY "name";

@set domain_id=''


-- SEQUENCES
DELETE FROM domain_and_table_sequence WHERE domain_id IN (:domain_id);
DELETE FROM domain_sequence WHERE domain_id IN (:domain_id);


-- TAG
DELETE FROM tag WHERE domain_id IN (:domain_id);


-- TIMELINE EVENT
DELETE FROM timeline_event_user WHERE timeline_event_id IN (SELECT id FROM timeline_event WHERE domain_id IN (:domain_id));
DELETE FROM timeline_event WHERE domain_id IN (:domain_id);


-- TOKEN
DELETE FROM "token" WHERE user_id IN (SELECT id FROM "user" WHERE domain_id IN (:domain_id));


-- USER
DELETE FROM "grant" WHERE user_id IN (SELECT id FROM "user" WHERE domain_id IN (:domain_id));
DELETE FROM "user" WHERE domain_id IN (:domain_id);


-- DOMÍNIO
UPDATE "domain" SET logo_id = NULL WHERE id IN (:domain_id);
DELETE FROM image WHERE id IN (SELECT id FROM file_infosys WHERE domain_id IN (:domain_id));
DELETE FROM file_infosys fi WHERE domain_id IN (:domain_id);
DELETE FROM domain_address WHERE domain_id IN (:domain_id);
DELETE FROM domain_contact WHERE domain_id IN (:domain_id);
DELETE FROM "domain" WHERE id IN (:domain_id);
