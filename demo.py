from llms.openai import Openai
from utils.prompt import get_prompt
from utils.excute import excute

model = Openai("gpt-3.5-turbo")
prompt = get_prompt()
db_path = 'database/database.sqlite'

print(f"[user] \n{prompt}")
messages = [{"role": "user", "content": prompt}]
while True:
    res = model.infer(messages)
    if "Query:" in res:
        print(f"[chatgpt]\n{res}")
        messages.append({"role": "system", "content": res})
        # exact query
        query_start = res.find("Query:") + len("Query:")
        query_end = res.find(";", query_start)
        query = res[query_start:query_end]
        query = query.replace("\n", " ").strip()

        # excute query
        column_names, results = excute(db_path, query)
        column_names = '\t'.join(column_names) + '\n'
        results = [str(t[0]) for t in results]
        results = '\t'.join(results)
        prompt = column_names + results
        input("============results============")
        print(prompt)
        messages.append({"role": "user", "content": prompt})\
        
    else:
        print("============report============")
        print(res)
        break
    
    
