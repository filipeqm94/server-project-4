-- DROP DATABASE chatter;
CREATE DATABASE chatter;
CREATE USER chatteruser WITH PASSWORD 'chatter';
GRANT ALL PRIVILEGES ON DATABASE chatter TO chatteruser;
ALTER USER chatteruser CREATEDB; -- to allow tests to run