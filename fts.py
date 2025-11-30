from sqlalchemy import text
from database import engine

def createTable(engine):
    with engine.begin() as conn:
        
    #     conn.execute(text("""DROP TABLE IF EXISTS books_fts;"""))
    #     conn.execute(text("""
    #         CREATE VIRTUAL TABLE books_fts 
    #         USING FTS5(title)
    # """))

        conn.execute(text("""INSERT INTO books_fts(title) SELECT title FROM books"""))


createTable(engine=engine)
# with engine.connect() as conn:
#     result = conn.execute(text("PRAGMA compile_options;")).fetchall()
#     print(result)


