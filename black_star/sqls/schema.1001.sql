BEGIN TRANSACTION;
ALTER TABLE "ufiles" RENAME TO 'ufiles_ME_TMP';
CREATE TABLE "ufiles" (
"id" INTEGER NOT NULL,
"name" VARCHAR(200),
"url" VARCHAR(200),
"description" TEXT,
"created" DATETIME,
"filename" VARCHAR(255),
"filesize" BIGINT,
"mimetype" VARCHAR(100),
"download" BOOLEAN,
"linkable" BOOLEAN,
"password" VARCHAR(200),
"homeshow" BOOLEAN,
"expire_at" DATETIME,
PRIMARY KEY (id),
UNIQUE (url),
CHECK (download IN (0, 1)),
CHECK (homeshow IN (0, 1))
);
INSERT INTO "ufiles"  ("id", "name", "url", "description", "created", "filename", "filesize", "mimetype", "download", "linkable", "password", "homeshow") SELECT "id", "name", "url", "description", "created", "filename", "filesize", "mimetype", "download", "linkable", "password", "homeshow" FROM "ufiles_ME_TMP";
DROP TABLE "ufiles_ME_TMP";
COMMIT;
