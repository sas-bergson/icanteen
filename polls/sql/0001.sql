BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "text" varchar(200) NOT NULL,
    "votes" integer NOT NULL);

--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "text" varchar(200) NOT NULL,
    "publication_date" datetime NOT NULL);
--
-- Add field question_id to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";

CREATE TABLE "polls_choice" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id_id" integer NOT NULL REFERENCES "polls_question" ("id"));

INSERT INTO "polls_choice" ("text", "votes", "question_id_id", "id")
    SELECT "text", "votes", NULL, "id" FROM "polls_choice__old";

DROP TABLE "polls_choice__old";

CREATE INDEX "polls_choice_e26d386a" ON "polls_choice" ("question_id_id");

COMMIT;
