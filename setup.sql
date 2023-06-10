-- This file is used to setup the database from scratch
CREATE TABLE ecoms (
    id BIGSERIAL PRIMARY KEY,
    website varchar(50) NOT NULL UNIQUE
);
CREATE TABLE executions (
    id BIGSERIAL PRIMARY KEY,
    ecom_id BIGINT NOT NULL REFERENCES ecoms(id) ON DELETE CASCADE,
    exec_datetime timestamptz NOT NULL DEFAULT NOW(),
    successful BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE items (
    id BIGSERIAL PRIMARY KEY,
    ecom_id BIGINT NOT NULL REFERENCES ecoms(id) ON DELETE CASCADE,
    name varchar(255) NOT NULL
);
CREATE TABLE execution_item_stocks (
    execution_id BIGINT NOT NULL REFERENCES executions(id) ON DELETE CASCADE,
    item_id BIGINT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    stock INT NOT NULL DEFAULT 1
);
INSERT INTO ecoms (website)
VALUES ('https://animextreme.ca'),
    ('https://server.gundamhangar.com'),
    ('https://niigs.ca'),
    ('https://www.gundamhobby.ca'),
    ('https://www.agesthreeandup.ca'),
    ('https://argamahobby.com');
/*
 Drop tables in this order if tearing down
 op.drop_table('execution_item_stocks')
 op.drop_table('items')
 op.drop_table('executions')
 op.drop_table('ecoms')
 */