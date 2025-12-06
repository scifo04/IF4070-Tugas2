import llm
import query

def retrieve():
    print("="*50)
    print("="*14,"WELCOME TO COURSE AI","="*14)
    print("="*50)
    prompt = input("Insert your prompt here: ")
    return prompt

def process_retrieval(prompt):
    driver = query.start_database("neo4j+s://4602ebc3.databases.neo4j.io", ('neo4j', 'VOMsGh-iOzq5Lnj0-Z_C0s3EF5eEIAke3S7U9VSVq2s'))

    key = llm.load_and_check_api()

    client = llm.create_client("https://openrouter.ai/api/v1", key)

    query_answer = llm.prompt_to_query(prompt, client)

    final_answer = llm.process_query(query_answer, driver)

    return final_answer

def main():
    inpute = retrieve()
    outpute = process_retrieval(inpute)
    print(outpute)

if __name__ == "__main__":
    main()