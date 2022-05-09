
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
            """ 
            + ("""
                
                UNWIND $categories AS cat
                MERGE (ca:Category { id: cat.id, name: cat.name } )
                MERGE (ca)-[:FROM_CURRICULUM]->(c)
                
                WITH DISTINCT cat, c, ca, cat.courses AS courses

                CALL apoc.do.when(size(courses) > 0, "UNWIND courses AS course
                    OPTIONAL MATCH (cu:Course {id: course.id})
                    FOREACH(ignored IN CASE WHEN cu IS NULL THEN [1] ELSE [] END |
                        CREATE (co:Course) SET co = course
                        MERGE (co)-[:FROM_CATEGORY]->(ca)
                    )", "", {courses:courses, ca:ca}) YIELD value

                WITH c 
            """ if categories else " ")
            +
            """
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

    """"
    Get courses Pre Requisistes
    """
    def get_pre_reqs(self, id):
        # Get pre requisites
        def get_pre_reqs(tx, id):
            if id == None:
                return []
            result = list(tx.run("""
                MATCH (c:Course {course_id: $course_id})<-[:PRE_REQUISITE]-(p)
                RETURN p.course_id AS id, p.classification AS code, p.name AS name
            """, course_id=int(id)))

            return [ {"id": r.get("id"), "code": r.get("code"), "name": r.get("name")} for r in result ]

        with self.driver.session() as session:
            records = session.write_transaction(get_pre_reqs, id=id)
            return records
        
    """"
    Get courses Co Requisistes
    """
    def get_co_reqs(self, id):
        # Get pre requisites
        def get_co_reqs(tx, id):
            if id == None:
                return []
            result = list(tx.run("""
                MATCH (c:Course {course_id: $course_id})<-[:CO_REQUISITE]-(p)
                RETURN p.course_id AS id, p.classification AS code, p.name AS name
            """, course_id=int(id)))

            return [ {"id": r.get("id"), "code": r.get("code"), "name": r.get("name")} for r in result ]

        with self.driver.session() as session:
            records = session.write_transaction(get_co_reqs, id=id)
            return records

    """
    Get years from a curriculum 
    """
    def get_curriculum(self, id):
        # Get curriculum from db
        def get_semesters(tx, id):
            result = list(tx.run("""
                MATCH (curr:Curriculum { id: $id})<-[:FROM_CURRICULUM]-(sem: Semester)
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

                    res[semesterId] = get_courses(tx, semesterId, row[0].get("name"))

            get_categories(tx, id, res)
                        
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
                    "id": row[0].get("course_id"),
                    "name": row[0].get("name"),
                    "code": row[0].get("classification")
                })

            return res

        def get_categories(tx, id, res):
            result = list(tx.run("""
                MATCH (curr:Curriculum { id: $id})<-[:FROM_CURRICULUM]-(cat: Category)
                RETURN DISTINCT cat.name AS name, cat.id AS id
            """, id=id))

            if result:
                res["categories"] = []
                for row in result:
                    id = row.get("id")
                    res["categories"].append(id)
                    
                    get_cat_courses(tx, id, res)
                        
            return res

        def get_cat_courses(tx, id, res):
            result = list(tx.run("""
                MATCH (cat:Category { id:$id})<-[:FROM_CATEGORY]-(c:Course)
                RETURN DISTINCT c.course_id AS id, c.name AS name, c.classification AS code
            """, id=id))

            if result:
                res[id] = []
                for row in result:
                    res[id].append({
                        "id": row.get("id"),
                        "name": row.get("name"),
                        "code": row.get("code")
                    })

            

        with self.driver.session() as session:
            curriculum = session.write_transaction(get_semesters, id=id)
            return curriculum