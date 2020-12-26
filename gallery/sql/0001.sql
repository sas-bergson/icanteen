BEGIN;
--
-- Create model Category
--
CREATE TABLE "gallery_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(256) NOT NULL UNIQUE, "slug" varchar(50) NULL UNIQUE, "path_to_icture" varchar(256) NOT NULL, "created" datetime NOT NULL, "last_updated" datetime NOT NULL, "views" integer NOT NULL);
--
-- Create model Product
--
CREATE TABLE "gallery_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "designation" varchar(256) NOT NULL UNIQUE, "slug" varchar(50) NULL UNIQUE, "description" text NOT NULL, "packaging" varchar(256) NOT NULL, "price" decimal NOT NULL, "path_to_icture" varchar(256) NOT NULL UNIQUE, "created" datetime NOT NULL, "last_updated" datetime NOT NULL, "views" integer NOT NULL, "category_id_id" integer NOT NULL REFERENCES "gallery_category" ("id"));
CREATE INDEX "gallery_product_2d5f8f90" ON "gallery_product" ("category_id_id");
COMMIT;
