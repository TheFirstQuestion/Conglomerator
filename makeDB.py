import sqlite3

conn = sqlite3.connect('conglomerator.db')

# TODO:
# add metadata

conn.execute(
    """
    CREATE TABLE files (
    id              INTEGER     PRIMARY KEY,
    originalName    VARCHAR     NOT NULL,
    systemName      VARCHAR     NOT NULL,
    systemType      VARCHAR     NOT NULL,
    parsedType      VARCHAR     NOT NULL
    );
    """
)

conn.execute(
    """
    CREATE TABLE projects (
    id          INTEGER     PRIMARY KEY,
    fileID      INTEGER     NOT NULL,
    name        VARCHAR     NOT NULL
    );
    """
)

conn.execute(
    """
    CREATE TABLE categories (
    id          INTEGER     PRIMARY KEY,
    fileID      INTEGER     NOT NULL,
    name        VARCHAR     NOT NULL
    );
    """
)

conn.commit()
conn.close()


# Testing purposes only
if __name__ == "__main__":
    conn = sqlite3.connect('conglomerator.db')
    #conn.execute('INSERT INTO `files` VALUES (6, "test.pdf", "pdf");')

    conn.commit()
    conn.close()
