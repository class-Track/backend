
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
    def create_curr(self, graph, co_reqs, pre_reqs):
        # Save curriculum in database
        def create_curriculum(tx, graph, co_reqs, pre_reqs):
            return tx.run("""
                UNWIND $graph AS curr
                MERGE (c:Curriculum { name: curr.name,  program: curr.program, user: curr.user} )
                
                WITH c
                
                UNWIND $graph[0].semesters AS sem
                MERGE (s:Semester { id: sem.id, name: sem.name, year: sem.year } )
                MERGE (s)-[:FROM_CURRICULUM]->(c)

                FOREACH (course in sem.courses | 
                    CREATE(co:Course) SET co = course
                    MERGE (co)-[:FROM_SEMESTER]->(s)
                )

                WITH c

                UNWIND $co_reqs AS coreq 
                MATCH (c1:Course) WHERE c1.id = coreq.id
                MATCH (c2:Course) WHERE c2.id = coreq.co_requisite
                MERGE (c2)-[:CO_REQUISITE]->(c1)

                WITH c

                UNWIND $pre_reqs AS prereq 
                MATCH (c1:Course) WHERE c1.id = prereq.id
                MATCH (c2:Course) WHERE c2.id = prereq.pre_requisite
                MERGE (c2)-[:PRE_REQUISITE]->(c1)

                RETURN c
            """, graph=graph, co_reqs=co_reqs, pre_reqs=pre_reqs).single()

        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, graph=graph, co_reqs=co_reqs, pre_reqs=pre_reqs)
            return { "id": record["c"].id }