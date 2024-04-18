CREATE Table "users" (
    "id" UUID PRIMARY KEY,
    "first_name" TEXT,
    "last_name" TEXT,
    "email" TEXT UNIQUE,
    "password" TEXT,
    "profiles" TEXT,
    "is_admin" BOOLEAN DEFAULT FALSE,
    "is_verified" BOOLEAN DEFAULT FALSE,
    "otp" int DEFAULT 0,
    "otp_expiration_time" TIMESTAMPTZ DEFAULT null,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT null,
    "deleted_at" TIMESTAMPTZ DEFAULT null
);

CREATE INDEX ON "users" ("id");

CREATE INDEX ON "users" ("email");

CREATE INDEX ON "users" ("first_name");

CREATE INDEX ON "users" ("last_name");

CREATE Table "tracking" (
    "id" UUID PRIMARY KEY,
    "user_id" UUID,
    "image_input" TEXT,
    "image_output" TEXT,
    "service_type" TEXT,
    "credits" int,
    "response_time" TIMESTAMPTZ DEFAULT Now(),
    "status_code" int,
    "response" TEXT,
    "created_at" TIMESTAMPTZ DEFAULT Now()
);

ALTER TABLE
    "tracking"
ADD
    FOREIGN KEY ("user_id") REFERENCES "users" ("id");

SET timezone = 'UTC';

CREATE INDEX ON "users" ("id");