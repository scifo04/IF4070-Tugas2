import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import query

def load_and_check_api():
    env_path = '../.env'
    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file.")
    
    return api_key

def create_client(base_url, api_key):
    return OpenAI(
        base_url=base_url,
        api_key=api_key,
        default_headers={'HTTP-Referer': "https://localhost:5000"}
    )

def prompt_to_query(prompt, client, need_prompt=False):
    user_prompt = """
    Obtain the entity of known information of one of these six entities and also the entity that want to be searched
    from the prompt (Prompt is in Indonesian):\n
    1. Course ID
    2. Course Name
    3. Course Credits
    4. Course Major
    5. Course Levels (Sarjana, Magister, or Doktor)
    6. Course Description\n\n

    This is the prompt: {prompt}\n\n

    Find the entity (Just the answer):\n
    {{"entity_info": (Entity of the Known Information), "entity_info_name": (Entity Info Name), "entity_target": (Entity That want to be search)}}
    """

    user_prompt = user_prompt.format(prompt=prompt)

    system_prompt = "You are the smartest AI assistant"

    final_prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=final_prompt
    )

    return {
        "prompt": prompt,
        "answer": response.choices[0].message.content
    } if need_prompt else { "answer": response.choices[0].message.content }

def process_query(answer, driver):
    try:
        raw = answer['answer']
        json_answer = json.loads(raw) 
        target = json_answer['entity_target']
        info = json_answer['entity_info']

        if target == 'Course Name':
            answer = query.get_course_name_from_course_id(driver, info)
        elif target == 'Course Credits':
            answer = query.get_credits_from_course_id(driver, info)
        elif target == 'Course Major':
            answer = query.get_course_majors_from_course_id(driver, info)
        elif target == 'Course Levels':
            answer = query.get_course_levels_from_course_id(driver, info)
        elif target == 'Course Description':
            answer = query.get_course_description_from_course_id(driver, info)
        else:
            answer = {
                'answer': 'There seems to be problem in the RAG'
            }
        
        return answer['answer']
    except Exception as _:
        return "Information is not found. Please re-enter the query"
    
def rag_style_answer(answer, client):
    user_prompt = """
    Decorate this answer like typical LLM answer its prompt but don't deviate too much from the answer's topic\n\n

    Prompt: {prompt}

    Answer: {{Answer here}}
    """

    user_prompt = user_prompt.format(prompt=answer)

    system_prompt = "You are the smartest AI assistant"

    final_prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=final_prompt
    )

    return response.choices[0].message.content