from neo4j import GraphDatabase

def start_database(uri, credentials):
    URI = uri
    AUTH = credentials 

    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    print("Connected to Neo4j!")

    return driver

def get_all_course_name(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Has_Name_Of]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            course_name = end_node["Course Name"]

            print(course_id, "->", course_name)

def get_all_course_credits(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Has_Credits]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            credits_course = end_node["CourseCredits"]

            print(course_id, "->", credits_course)

def get_all_course_majors(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Belongs_To_Major]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            majors = end_node["CourseMajor"]

            print(course_id, "->", majors)

def get_all_course_levels(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Has_Course_Level_Of]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            course_level = end_node["CourseLevel"]

            print(course_id, "->", course_level)

def get_all_course_description(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Described_As]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            course_description = end_node["CourseDescription"]

            print(course_id, "->", course_description)

def get_course_name_from_course_id(driver, course_id):
    with driver.session() as session:
        result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Has_Name_Of]->() RETURN p;", course_id=course_id)
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            course_name = end_node["Course Name"]

            return {
                'answer': f"The name of the course with ID of {course_id} is {course_name}"
            } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }