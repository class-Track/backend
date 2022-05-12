class CurruculumGraph:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver

    """
    Create a new standard curriculum 
    """
    def create_standard_curr(self, curr, dept, categories, semesters, prereqs, coreqs, cat_per_course):
        # Save curriculum in database
        def create_curriculum(tx, curr, dept,  categories, semesters, prereqs, coreqs, cat_per_course):
            return tx.run("""
                MERGE (c:Curriculum { curriculum_sequence: $curr.curriculum_sequence, name: $curr.name, deptCode: $curr.deptCode, user_id: $curr.user_id, length: $curr.length, credits: $curr.credits, degree_id:$curr.degree_id, degree_name:$curr.degree_name, department_id: $curr.department_id, department_name:$curr.department_name })
                
                WITH c
                
                UNWIND $semesters AS sem
                MERGE (s:Semester { id: sem.id, name: sem.name, year: sem.year } )
                MERGE (s)-[:FROM_CURRICULUM]->(c)
                
                WITH c, sem, s, sem.courses AS courses
                
                CALL apoc.do.when(size(courses) > 0, "UNWIND courses AS course
                    OPTIONAL MATCH(co:Course {course_id: course.course_id})
                    FOREACH (ignored IN CASE WHEN co IS NULL THEN [1] ELSE [] END  | 
                        MERGE (co:Course {classification: course.classification, credits: course.credits, course_id: course.course_id, department_id: course.department_id, id: course.id, name: course.name }) 
                        MERGE (co)-[:FROM_SEMESTER]->(s)
                    ) 
                    WITH c, course, s
                    MATCH(co:Course {course_id: course.course_id})
                    MERGE (co)-[:FROM_SEMESTER]->(s)
                    RETURN c", "", {courses:courses, s:s, c:c}) YIELD value

                WITH c
            """ 
            + ("""
                
                UNWIND $categories AS cat
                MERGE (ca:Category { id: cat.id, category_id: cat.category_id, classification: cat.classification, name: cat.name, credits: cat.credits } )
                MERGE (ca)-[:FROM_CURRICULUM]->(c)
                
                WITH DISTINCT cat, c, ca, cat.courses AS courses

                CALL apoc.do.when(size(courses) > 0, "UNWIND courses AS course
                    OPTIONAL MATCH (cu:Course {course_id: course.course_id})
                    FOREACH(ignored IN CASE WHEN cu IS NULL THEN [1] ELSE [] END |
                        MERGE (co:Course {classification: course.classification, credits: course.credits, course_id: course.course_id, department_id: course.department_id, id: course.id, name: course.name }) 
                        MERGE (co)-[:FROM_CATEGORY]->(ca)
                    ) 
                    WITH c, course, ca
                    MATCH(co:Course {course_id: course.course_id})
                    MERGE (co)-[:FROM_CATEGORY]->(ca)
                    RETURN c", "", {courses:courses, ca:ca, c:c}) YIELD value

                WITH c
            """ if categories else " ")
            +
            ("""
                UNWIND $coreqs AS coreq 
                MATCH (c1:Course) WHERE c1.id = coreq.id
                MATCH (c2:Course) WHERE c2.id = coreq.co_id
                MERGE (c2)-[:CO_REQUISITE {dept: $dept}]->(c1)

                WITH c
            """ if coreqs else " ")
            +
            ("""

                UNWIND $prereqs AS prereq 
                MATCH (c1:Course) WHERE c1.id = prereq.id
                MATCH (c2:Course) WHERE c2.id = prereq.pre_id
                MERGE (c2)-[:PRE_REQUISITE {dept: $dept}]->(c1)

                WITH c
            """ if prereqs else " ")
            +
            ("""
                UNWIND $cat_per_course AS cpc
                MATCH (c3:Course {course_id: cpc.id}) SET c3.category = cpc.category

                RETURN DISTINCT c.curriculum_sequence
            """ if cat_per_course else "DISTINCT RETURN c.curriculum_sequence")
        , curr=curr, dept=dept, categories=categories, semesters=semesters, prereqs=prereqs, coreqs=coreqs, cat_per_course=cat_per_course).single()

        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, curr=curr, dept=dept,  categories=categories, semesters=semesters, prereqs=prereqs, coreqs=coreqs, cat_per_course=cat_per_course)
            return { "id": record[0] }

    """
    Create a new Custom curriculum 
    """
    def create_custom_curr(self, curr, categories, semesters, cat_per_course):
        # Save curriculum in database
        def create_curriculum(tx, curr, categories, semesters, cat_per_course):
            return tx.run("""
                MERGE (c:Curriculum { curriculum_sequence: $curr.curriculum_sequence, name: $curr.name, deptCode: $curr.deptCode, user_id: $curr.user_id, length: $curr.length, credits: $curr.credits, degree_id:$curr.degree_id, degree_name:$curr.degree_name, department_id: $curr.department_id, department_name:$curr.department_name, isDraft: $curr.isDraft })
                
                WITH c
                
                UNWIND $semesters AS sem
                MERGE (s:Semester { id: sem.id, name: sem.name, year: sem.year } )
                MERGE (s)-[:FROM_CURRICULUM]->(c)
                
                WITH c, sem, s, sem.courses AS courses
                
                CALL apoc.do.when(size(courses) > 0, "UNWIND courses AS course
                    OPTIONAL MATCH(co:Course {course_id: course.course_id})
                    FOREACH (ignored IN CASE WHEN co IS NULL THEN [1] ELSE [] END  | 
                        MERGE (co:Course {classification: course.classification, credits: course.credits, course_id: course.course_id, department_id: course.department_id, id: course.id, name: course.name }) 
                        MERGE (co)-[:FROM_SEMESTER]->(s)
                    ) 
                    WITH c, course, s
                    MATCH(co:Course {course_id: course.course_id})
                    MERGE (co)-[:FROM_SEMESTER]->(s)
                    RETURN c", "", {courses:courses, s:s, c:c}) YIELD value

                WITH c
            """ 
            + ("""
                
                UNWIND $categories AS cat
                MERGE (ca:Category { id: cat.id, category_id: cat.category_id, classification: cat.classification, name: cat.name, credits: cat.credits } )
                MERGE (ca)-[:FROM_CURRICULUM]->(c)
                
                WITH DISTINCT cat, c, ca, cat.courses AS courses

                CALL apoc.do.when(size(courses) > 0, "UNWIND courses AS course
                    OPTIONAL MATCH (cu:Course {course_id: course.course_id})
                    FOREACH(ignored IN CASE WHEN cu IS NULL THEN [1] ELSE [] END |
                        MERGE (co:Course {classification: course.classification, credits: course.credits, course_id: course.course_id, department_id: course.department_id, id: course.id, name: course.name }) 
                        MERGE (co)-[:FROM_CATEGORY]->(ca)
                    ) 
                    WITH c, course, ca
                    MATCH(co:Course {course_id: course.course_id})
                    MERGE (co)-[:FROM_CATEGORY]->(ca)
                    RETURN c", "", {courses:courses, ca:ca, c:c}) YIELD value

                WITH c
            """ if categories else " ")
            +
            ("""
                UNWIND $cat_per_course AS cpc
                MERGE (c3:Course {course_id: cpc.id})
                ON MATCH
                    SET c3.category = cpc.category

                RETURN DISTINCT c.curriculum_sequence
            """ if cat_per_course else "DISTINCT RETURN c.curriculum_sequence")
        , curr=curr, categories=categories, semesters=semesters, cat_per_course=cat_per_course).single()

        with self.driver.session() as session:
            record = session.write_transaction(create_curriculum, curr=curr, categories=categories, semesters=semesters, cat_per_course=cat_per_course)
            return { "id": record[0] }

    """"
    Get courses Pre Requisistes
    """
    def get_pre_reqs(self, id, dept):
        # Get pre requisites
        def get_pre_reqs(tx, id, dept):
            if id == None:
                return []
            result = list(tx.run("""
                MATCH (c:Course {course_id: $course_id})<-[:PRE_REQUISITE {dept: $dept}]-(p)
                RETURN p.course_id AS id, p.classification AS code, p.name AS name
            """, course_id=int(id), dept=dept))

            return [ {"id": r.get("id"), "code": r.get("code"), "name": r.get("name")} for r in result ]

        with self.driver.session() as session:
            records = session.write_transaction(get_pre_reqs, id=id, dept=dept)
            return records
        
    """"
    Get courses Co Requisistes
    """
    def get_co_reqs(self, id, dept):
        # Get pre requisites
        def get_co_reqs(tx, id, dept):
            if id == None:
                return []
            result = list(tx.run("""
                MATCH (c:Course {course_id: $course_id})-[:CO_REQUISITE {dept: $dept}]-(p)
                RETURN p.course_id AS id, p.classification AS code, p.name AS name
            """, course_id=int(id), dept=dept))

            return [ {"id": r.get("id"), "code": r.get("code"), "name": r.get("name")} for r in result ]

        with self.driver.session() as session:
            records = session.write_transaction(get_co_reqs, id=id, dept=dept)
            return records

    """"
    Delete curriculum node and relationships
    """
    def delete_curriculum(self, id, deptCode):
        # Delete Custom curriculum
        def delete_custom_curriculum(tx, id):
            if id == None:
                return None
            result = (tx.run("""
                MATCH (c:Curriculum {curriculum_sequence: $curr_id})<-[:FROM_CURRICULUM | :FROM_CATEGORY]-(sem)
                WITH c, sem, c.curriculum_sequence AS id
                DETACH DELETE sem, c
                RETURN DISTINCT id
            """, curr_id=id)).single()

            return result.get('id')

        def delete_standard_curriculum(tx, id, dept):
            if id == None:
                return None
            result = (tx.run("""
                MATCH (c:Curriculum {curriculum_sequence: $curr_id})<-[:FROM_CURRICULUM | :FROM_CATEGORY]-(sem)
                WITH c, sem, c.curriculum_sequence AS id
                DETACH DELETE sem, c
                WITH id
                MATCH (c:Course)-[pre:PRE_REQUISITE {dept:$dept}]-(:Course)
                DELETE pre
                WITH id
                MATCH (c:Course)-[co:CO_REQUISITE {dept:$dept}]-(:Course)
                DELETE co
                RETURN DISTINCT id
            """, curr_id=id, dept=dept)).single()

            return result.get('id')

        with self.driver.session() as session:
            if deptCode:
                records = session.write_transaction(delete_standard_curriculum, id=id, dept=deptCode) 
            else :
                records = session.write_transaction(delete_custom_curriculum, id=id)
            return records

    """"
    Update a Custom curriculum
    """
    def update_custom_curriculum(self, curriculum_sequence, curr, categories, semesters, cat_per_course):
        self.delete_curriculum(curriculum_sequence)
        id = self.create_custom_curr(curr, categories, semesters, cat_per_course)
        return id

    """"
    Update a Standard curriculum
    """
    def update_standard_curriculum(self, curriculum_sequence, curr, categories, semesters, coreqs, prereqs, cat_per_course):
        self.delete_curriculum(curriculum_sequence)
        id = self.create_standard_curr(curr, categories, semesters, coreqs, prereqs, cat_per_course)
        return id
   
    """
    Get a curriculum 
    """
    def get_curriculum(self, id):
        # Get curriculum from db
        def get_semesters(tx, id):
            result = list(tx.run("""
                MATCH (curr:Curriculum { curriculum_sequence: $curriculum_sequence})<-[:FROM_CURRICULUM]-(sem: Semester)
                RETURN DISTINCT sem, curr
            """, curriculum_sequence=id))

            if not result:
                res = None
            else:
                curr = result[1][1]
                res = {
                    "credits": curr.get("credits"),
                    "name": curr.get("name"),
                    "curriculum_sequence": curr.get("curriculum_sequence"),
                    "degree_id": curr.get("degree_id"),
                    "degree_name": curr.get("degree_name"),
                    "department_id": curr.get("department_id"),
                    "department_name": curr.get("department_name"),
                    "deptCode": curr.get("deptCode"),
                    "length": curr.get("length"),
                    "year_list": { "id": "year_list",
                                      "name": "Year List",
                                      "year_ids": []
                                    }}

                dept = curr.get("deptCode")
            
                for row in result:
                    year = str(row[0].get("year"))
                    semesterId = row[0].get("id")
                    if year in res:
                        res[year]["semester_ids"].append(semesterId)
                    else:
                        res["year_list"]["year_ids"].append(year)
                        res[year] = { "id": "year_{}".format(year),
                                    "name": "Year {}".format(year),
                                    "semester_ids": [semesterId] }

                    res[semesterId] = get_courses(tx, semesterId, row[0].get("name"), year)

            get_categories(tx, id, res)
            get_all_course_info(tx, id, res, dept)
                        
            return res

        def get_courses(tx, semesterId, semName, year):
            result = tx.run("""
                MATCH (sem:Semester { id:$semesterId})<-[:FROM_SEMESTER]-(course)
                RETURN DISTINCT course
            """, semesterId=semesterId)

            res = { "id": semesterId,
                    "name": semName,
                    "year": year,
                    "list_type": "SEMESTER",
                    "courses": []
                    }
            for row in result:
                res["courses"].append({
                    "id": row[0].get("id"),
                    "course_id": row[0].get("course_id"),
                    "credits": row[0].get("credits"),
                    "name": row[0].get("name"),
                    "classification": row[0].get("classification"),
                    "department_id": row[0].get("department_id")
                })

            return res

        def get_categories(tx, id, res):
            result = list(tx.run("""
                MATCH (curr:Curriculum { curriculum_sequence: $id})<-[:FROM_CURRICULUM]-(cat: Category)
                RETURN DISTINCT cat.name AS name, cat.id AS id, cat.credits AS credits, cat.category_id AS category_id, cat.classification AS classification
            """, id=id))

            if result:
                res["category_list"] = {  "id": "category_list",
                                          "name": "Category List",
                                          "category_ids": [] }
                for cat in result:
                    id = cat.get("id")
                    res["category_list"]["category_ids"].append(id)
                    res[id] = {
                        "courses": [],
                        "credits": cat.get("credits"),
                        "id": id,
                        "name": cat.get("name"),
                        "classification": cat.get("classification"),
                        "category_id": cat.get("category_id"),
                        "list_type": "CATEGORY",
                    }
                    get_cat_courses(tx, id, res)
                        
            return res
            
        def get_cat_courses(tx, id, res):
            result = list(tx.run("""
                MATCH (cat:Category { id:$id})<-[:FROM_CATEGORY]-(c:Course)
                RETURN DISTINCT c.id AS id, c.credits AS credits, c.course_id AS course_id, c.name AS name, c.classification AS classification, c.department_id AS department_id
            """, id=id))

            if result:
                for row in result:
                    res[id]["courses"].append({
                        "id": row.get("id"),
                        "course_id": row.get("course_id"),
                        "name": row.get("name"),
                        "credits": row.get("credits"),
                        "classification": row.get("classification"),
                        "department_id": row.get("department_id"),
                    })

        def get_all_course_info(tx, curr_id, res, dept):
            result = list(tx.run("""
                MATCH (curr1:Curriculum { curriculum_sequence: $id})<-[:FROM_CURRICULUM]-(sem: Semester)<-[:FROM_SEMESTER]-(co: Course)

                UNWIND co AS course
                    OPTIONAL MATCH (c1:Course {course_id: course.course_id})<-[:PRE_REQUISITE {dept: $dept}]-(pre)
                    OPTIONAL MATCH (c2:Course {course_id: course.course_id})-[:CO_REQUISITE {dept: $dept}]-(coreq)
                    WITH co, pre, coreq
    
                    RETURN co.id AS id, co.course_id AS course_id, co.name AS name, co.category AS category, co.classification AS classification, co.credits AS credits, co.department_id AS department_id, (CASE WHEN pre IS NOT NULL THEN collect( DISTINCT {classification: pre.classification, credits:pre.credits, course_id:pre.course_id, department_id: pre.department_id, name: pre.name, id: pre.id}) ELSE [] END) AS prereqs, (CASE WHEN coreq IS NOT NULL THEN collect( DISTINCT {classification: coreq.classification, credits: coreq.credits, course_id:coreq.course_id, department_id: coreq.department_id, name: coreq.name, id: coreq.id}) ELSE [] END) AS coreqs
                UNION
                MATCH (curr2:Curriculum { curriculum_sequence: $id})<-[:FROM_CURRICULUM]-(cat: Category)<-[:FROM_CATEGORY]-(cu: Course)
                UNWIND cu AS course
                    OPTIONAL MATCH (c1:Course {course_id: course.course_id})<-[:PRE_REQUISITE {dept: $dept}]-(pre)
                    OPTIONAL MATCH (c2:Course {course_id: course.course_id})-[:CO_REQUISITE {dept: $dept}]-(coreq)
                    WITH cu, pre, coreq
                    
                    RETURN cu.id AS id, cu.course_id AS course_id, cu.name AS name, cu.category AS category, cu.classification AS classification, cu.credits AS credits, cu.department_id AS department_id, (CASE WHEN pre IS NOT NULL THEN collect( DISTINCT {classification: pre.classification, credits:pre.credits, course_id:pre.course_id, department_id: pre.department_id, name: pre.name, id: pre.id}) ELSE [] END) AS prereqs, (CASE WHEN coreq IS NOT NULL THEN collect( DISTINCT {classification: coreq.classification, credits: coreq.credits, course_id:coreq.course_id, department_id: coreq.department_id, name: coreq.name, id: coreq.id}) ELSE [] END) AS coreqs
            """, id=curr_id, dept=dept))
            if result:
                res['course_list'] = {
                    "id": "course_list",
                    "name": "Course List",
                    "course_ids": []
                }
                for course in result:
                    res['course_list']['course_ids'].append(course.get('id'))
                    res[course.get('id')] = {
                        "id": course.get("id"),
                        "course_id": course.get("course_id"),
                        "name": course.get("name"),
                        "credits": course.get("credits"),
                        "classification": course.get("classification"),
                        "department_id": course.get("department_id"),
                        "category": course.get('category'),
                        "prereqs": course.get('prereqs'),
                        "coreqs": course.get('coreqs')
                    }
            

        with self.driver.session() as session:
            curriculum = session.write_transaction(get_semesters, id=id)
            return curriculum
            