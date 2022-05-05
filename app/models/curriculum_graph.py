
class CurruculumGraph:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver

    """
    Create a new standard curriculum - MODIFIED 
    """
    def create_standard_curr(self, curr, categories, semesters, prereqs, coreqs):
        # Save curriculum in database
        def create_curriculum(tx, curr, categories, semesters, prereqs, coreqs):
            return tx.run("""
                MERGE (c:Curriculum { id: $curr.id, name: $curr.name, program: $curr.program, user: $curr.user, length: $curr.length, credits: $curr.credits })
                
                WITH c
                
                UNWIND $semesters AS sem
                MERGE (s:Semester { id: sem.id, name: sem.name, year: sem.year } )
                MERGE (s)-[:FROM_CURRICULUM]->(c)
                
                WITH c, sem, s
                
                UNWIND sem.courses AS course
                OPTIONAL MATCH(co:Course {id: course.id})
                FOREACH (ignored IN CASE WHEN co IS NULL THEN [1] ELSE [] END  | 
                    CREATE(co:Course) SET co = course
                    MERGE (co)-[:FROM_SEMESTER]->(s)
                )

                WITH c

                UNWIND $categories AS cat
                MERGE (ca:Category { id: cat.id, name: cat.name } )
                MERGE (ca)-[:FROM_CURRICULUM]->(c)
                
                WITH DISTINCT cat, c, ca
                
                UNWIND cat.courses AS course
                OPTIONAL MATCH (cu:Course {id: course.id})
                FOREACH(ignored IN CASE WHEN cu IS NULL THEN [1] ELSE [] END |
                    CREATE (co:Course) SET co = course
                    MERGE (co)-[:FROM_CATEGORY]->(ca)
                )

                WITH c

                UNWIND $coreqs AS coreq 
                MATCH (c1:Course) WHERE c1.id = coreq.id
                MATCH (c2:Course) WHERE c2.id = coreq.co_id
                MERGE (c2)-[:CO_REQUISITE]->(c1)

                WITH c

                UNWIND $prereqs AS prereq 
                MATCH (c1:Course) WHERE c1.id = prereq.id
                MATCH (c2:Course) WHERE c2.id = prereq.pre_id
                MERGE (c2)-[:PRE_REQUISITE]->(c1)

                RETURN c
            """, curr=curr, categories=categories, semesters=semesters, prereqs=prereqs, coreqs=coreqs).single()

        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, curr=curr, categories=categories, semesters=semesters, prereqs=prereqs, coreqs=coreqs)
            return { "id": record["c"].id }



    """
    Create a new Custom curriculum 
    """
    def create_custom_curr(self, graph):
        # Save curriculum in database
        def create_curriculum(tx, graph):
            return tx.run("""
                UNWIND $graph AS curr
                MERGE (c:Curriculum { id: curr.id, name: curr.name,  program: curr.program, user: curr.user} )
                
                WITH c
                
                UNWIND $graph[0].semesters AS sem
                MERGE (s:Semester { id: sem.id, name: sem.name, year: sem.year } )
                MERGE (s)-[:FROM_CURRICULUM]->(c)

                FOREACH (course in sem.courses | 
                    CREATE(co:Course) SET co = course
                    MERGE (co)-[:FROM_SEMESTER]->(s)
                )

                RETURN c
            """, graph=graph).single()

        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, graph=graph)
            return { "id": record["c"].id }


    """
    Get years from a curriculum 
    """
    def get_curriculum(self, id):
        # Save curriculum in database
        def get_semesters(tx, id):
            result = list(tx.run("""
                MATCH (curr:Curriculum { id: $id})<-[:FROM_CURRICULUM]-(sem)
                RETURN DISTINCT sem
            """, id=id))

            if not result:
                res = None
            else:
                res = {"years": []}
                for row in result:
                    year = str(row[0].get("year"))
                    semesterId = row[0].get("id")
                    if year in res:
                        res[year]["semesters_ids"].append(semesterId)
                    else:
                        res["years"].append(year)
                        res[year] = { "id": "year_{}".format(year),
                                    "name": "Year {}".format(year),
                                    "semesters_ids": [semesterId] }

                    res[semesterId] = get_courses(tx, semesterId, row[0].get("name") )
                        
            return res

        def get_courses(tx, semesterId, semName):
            result = tx.run("""
                MATCH (sem:Semester { id:$semesterId})<-[:FROM_SEMESTER]-(course)
                RETURN DISTINCT course
            """, semesterId=semesterId)

            res = { "id": semesterId,
                    "name": semName,
                    "courses": []
                    }
            for row in result:
                res["courses"].append({
                    "id": row[0].get("id"),
                    "name": row[0].get("name"),
                    "code": row[0].get("code")
                })

            return res

        with self.driver.session() as session:
            semesters = session.write_transaction(get_semesters, id=id)
            return semesters