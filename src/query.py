from neo4j import GraphDatabase

def start_database(uri, credentials):
    URI = uri
    AUTH = credentials 

    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def get_all_course_name(driver):
    with driver.session() as session:
        result = session.run("MATCH p=()-[:Has_Name_Of]->() RETURN p;")
        for record in result:
            path = record["p"]
            
            start_node = path.start_node
            end_node   = path.end_node

            course_id = start_node["CourseID"]
            course_name = end_node["CourseName"]

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
        course_names = []
        course_ids = course_id
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Has_Name_Of]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                course_name = end_node["CourseName"]

                course_names.append(course_name)

        return {
            'answer': f"""
                        The course with ID of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_ids)]))}\n\n 
                        Has course names respectively of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_names)]))}
                    """
        } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }
        
def get_credits_from_course_id(driver, course_id):
    with driver.session() as session:
        course_credits = []
        course_ids = course_id
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Has_Credits]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                credits_course = end_node["CourseCredits"]

                course_credits.append(credits_course)

        return {
            'answer': f"""
                        The course with ID of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_ids)]))}\n\n 
                        Has course credits respectively of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_credits)]))}
                    """
        } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }
        
def get_course_majors_from_course_id(driver, course_id):
    with driver.session() as session:
        course_majors = []
        course_ids = course_id
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Belongs_To_Major]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                majors = end_node["CourseMajor"]

                course_majors.append(majors)

        return {
            'answer': f"""
                        The course with ID of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_ids)]))}\n\n 
                        Belong to majors of following:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_majors)]))}
                    """
        } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }
        
def get_course_levels_from_course_id(driver, course_id):
    with driver.session() as session:
        course_levels = []
        course_ids = course_id
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Has_Course_Level_Of]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                levels = end_node["CourseLevel"]

                course_levels.append(levels)

        return {
            'answer': f"""
                        The course with ID of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_ids)]))}\n\n 
                        Belong to degree level of following:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_levels)]))}
                    """
        } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }
        
def get_course_description_from_course_id(driver, course_id):
    with driver.session() as session:
        course_ids = course_id
        course_names = []
        course_descriptions = []
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Has_Name_Of]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                course_name = end_node["CourseName"]

                course_names.append(course_name)
        for id_single in course_id:
            result = session.run("MATCH p = (:CourseID {CourseID: $course_id})-[:Described_As]->() RETURN p;", course_id=id_single)
            for record in result:
                path = record["p"]
                
                start_node = path.start_node
                end_node   = path.end_node

                course_id = start_node["CourseID"]
                course_description = end_node["CourseDescription"]

                course_descriptions.append(course_description)

            return {
                'answer': f"""
                        The course with ID and name of:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_ids)]))} {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_names)]))}\n\n 
                        Can be described as:\n
                        {("\n".join([f"{i+1}. {item}" for i, item in enumerate(course_descriptions)]))}
                    """
            } if course_id is not None else { 'answer': "There seems to be problem in the RAG" }
        
def get_course_id_from_course_name(driver, course_name):
    with driver.session() as session:
        course_names = course_name
        course_id_flattened = []
        course_id_list = []
        course_id_list_permanent = []
        for name_single in course_name:
            result = session.run('MATCH p = (:CourseName {CourseName: $course_name})-[:Identified_By_ID_Of]->() RETURN p', course_name=name_single)
            course_name = ""
            for record in result:
                path = record['p']

                start_node = path.start_node
                end_node = path.end_node

                course_name = start_node["CourseName"]
                course_id_list.append(end_node["CourseID"])
                course_id_list_permanent.append(end_node["CourseID"])
            course_id_flattened.append(", ".join(course_id_list))
            course_id_list = []
        return {
            'answer': f"""
                        The course with name of:\n
                        {("\n".join([f"{i+1}. {item} has IDs of {course_id_flattened[i]}" for i, item in enumerate(course_names)]))}
                    """
            ,'context': course_id_list_permanent
        } if course_name is not None else { 'answer': 'There seems to be problem in the RAG' }
    
def get_course_id_from_course_credits(driver, course_credits):
    with driver.session() as session:
        course_id_flattened = []
        course_id_list = []
        course_id_list_permanent = []
        le_course_credits = course_credits
        for credits_single in course_credits:
            result = session.run('MATCH p = (:Credits {CourseCredits: $course_credits})-[:Offered_To_Course]->() RETURN p', course_credits=int(credits_single))
            course_credits = ""
            for record in result:
                path = record['p']

                start_node = path.start_node
                end_node = path.end_node

                course_credits = start_node["CourseCredits"]
                course_id_list.append(end_node["CourseID"])
                course_id_list_permanent.append(end_node["CourseID"])
            course_id_flattened.append(", ".join(course_id_list))
            course_id_list = []
        return {
            'answer': f"""
                        The course with the amount of credits of:\n
                        {("\n".join([f"{i+1}. {item} has IDs of {course_id_flattened[i]}" for i, item in enumerate(le_course_credits)]))}
                    """
            ,'context': course_id_list_permanent
        } if course_credits is not None else { 'answer': 'There seems to be problem in the RAG' }
    
def get_course_id_from_course_majors(driver, course_majors):
    with driver.session() as session:
        course_id_flattened = []
        course_id_list = []
        course_id_list_permanent = []
        le_course_majors = course_majors
        for major_single in course_majors:
            result = session.run('MATCH p = (:CourseMajor {CourseMajor: $course_major})-[:Offers_Course_Of]->() RETURN p', course_major=major_single)
            course_majors = ""
            for record in result:
                path = record['p']

                print(path)

                start_node = path.start_node
                end_node = path.end_node

                course_majors = start_node["CourseMajor"]
                course_id_list.append(end_node["CourseID"])
                course_id_list_permanent.append(end_node["CourseID"])
            course_id_flattened.append(", ".join(course_id_list))
            course_id_list = []
        return {
            'answer': f"""
                        The course with the amount of credits of:\n
                        {("\n".join([f"{i+1}. {item} has IDs of {course_id_flattened[i]}" for i, item in enumerate(le_course_majors)]))}
                    """
            ,'context': course_id_list_permanent
        } if course_majors is not None else { 'answer': 'There seems to be problem in the RAG' }
    
def get_course_id_from_course_levels(driver, course_levels):
    with driver.session() as session:
        course_id_flattened = []
        course_id_list = []
        course_id_list_permanent = []
        le_course_levels = course_levels
        for level_single in course_levels:
            result = session.run('MATCH p = (:CourseLevel {CourseLevel: $course_level})-[:Offered_In_This_Level]->() RETURN p', course_level=level_single)
            course_levels = ""
            for record in result:
                path = record['p']

                start_node = path.start_node
                end_node = path.end_node

                course_levels = start_node["CourseLevel"]
                course_id_list.append(end_node["CourseID"])
                course_id_list_permanent.append(end_node["CourseID"])
            course_id_flattened.append(", ".join(course_id_list))
            course_id_list = []
        return {
            'answer': f"""
                        The course with the amount of credits of:\n
                        {("\n".join([f"{i+1}. {item} has IDs of {course_id_flattened[i]}" for i, item in enumerate(le_course_levels)]))}
                    """
            ,'context': course_id_list_permanent
        } if course_levels is not None else { 'answer': 'There seems to be problem in the RAG' }