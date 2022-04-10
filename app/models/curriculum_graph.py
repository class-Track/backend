
class CurruculumGraph:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver

    """
    Create a new curriculum 
    """
    def create_curr(self, id, graph):
        # Save curriculum in database
        def create_curriculum(tx, id, graph):
            return tx.run("""
                UNWIND $graph AS curr
                CREATE (n:Curriculum)
                SET n = curr
                RETURN n
            """, id=id, graph=graph).single()
        # run create_curriculum
        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, id=id, graph=graph)

            return { "id": record["n"].id }
