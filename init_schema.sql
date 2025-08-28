CREATE TABLE process_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);
CREATE INDEX ix_process_categories_id ON process_categories (id);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR,
    "addPeople" BOOLEAN,
    "deletePeople" BOOLEAN,
    "editPeople" BOOLEAN,
    "editPassword" BOOLEAN,
    "addRole" BOOLEAN,
    "editRole" BOOLEAN,
    "shareChecklist" BOOLEAN,
    "shareAnyChecklist" BOOLEAN,
    "editChecklist" BOOLEAN,
    "editAnyChecklist" BOOLEAN,
    "deleteChecklist" BOOLEAN,
    "deleteAnyChecklist" BOOLEAN,
    "addChecklist" BOOLEAN,
    "createTime" TIMESTAMP,
    "updateTime" TIMESTAMP
);
CREATE INDEX ix_roles_id ON roles (id);

CREATE TABLE users (
    username VARCHAR NOT NULL,
    avatar VARCHAR,
    "roleId" INTEGER NOT NULL REFERENCES roles(id),
    "createTime" TIMESTAMP,
    "updateTime" TIMESTAMP,
    id UUID PRIMARY KEY,
    email VARCHAR(320) NOT NULL UNIQUE,
    hashed_password VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    is_verified BOOLEAN NOT NULL
);
CREATE INDEX ix_users_avatar ON users (avatar);
CREATE INDEX ix_users_username ON users (username);

CREATE TABLE processes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    category_id INTEGER REFERENCES process_categories(id),
    owner_id UUID NOT NULL REFERENCES users(id)
);
CREATE INDEX ix_processes_id ON processes (id);

CREATE TABLE process_instance_shares (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    process_id INTEGER REFERENCES processes(id),
    can_edit BOOLEAN,
    can_share BOOLEAN
);

CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    "order" INTEGER,
    process_id INTEGER REFERENCES processes(id)
);
CREATE INDEX ix_stages_id ON stages (id);

CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    completed BOOLEAN,
    "resourceUrl" VARCHAR,
    stage_id INTEGER REFERENCES stages(id)
);
CREATE INDEX ix_steps_id ON steps (id);
