import os
import time

from dotenv import load_dotenv
from mistralai import Mistral
import pandas as pd
from bs4 import BeautifulSoup

# getting_data_from_glassdoor()


def ai_responses():
    load_dotenv()
    df_new = pd.DataFrame(columns=["Company", "Job Role"])
    key = os.getenv('API_KEY')
    agent = os.getenv('AGENT-ID')
    client = Mistral(api_key=key)
    df = pd.read_csv("output2.csv")
    for i in df.index:
        row = str(df.loc[i, "Company"]) + "\n" + str(df.loc[i, "Job Role"]) + "\n" + str(df.loc[i, "Description"])
        time.sleep(5)
        chat_response = client.agents.complete(
            agent_id="{}".format(agent),
            messages=[
                {
                    "role": "user",
                    "content": "{}".format(row),
                },
            ],
        )
        response = chat_response.choices[0].message.content
        if response == "No":
            continue
        else:
            if "," in response:
                company, job_role = response.split(",", 1)
            else:
                # Handle the case where there is no comma in the response
                company = response
                job_role = "Unknown"  # or handle differently based on your needs

            print(company, job_role)

            df_new.loc[len(df_new)] = [company, job_role]
    df_new.to_csv("JobsToApply.csv", index=False)



def converting_to_text():
    df = pd.read_csv("output.txt")
    for i in df.index:

        company_value = df.loc[i, "Company"]
        if isinstance(company_value, str):
            soup = BeautifulSoup(company_value, "html.parser")
            df.loc[i, "Company"] = soup.get_text()
        else:
            df.loc[i, "Company"] = ""

        job_role_value = df.loc[i, "Job Role"]
        if isinstance(job_role_value, str):
            soup = BeautifulSoup(job_role_value, "html.parser")
            df.loc[i, "Job Role"] = soup.get_text()
        else:
            df.loc[i, "Job Role"] = ""

        description_value = df.loc[i, "Description"]
        if isinstance(description_value, str):
            soup = BeautifulSoup(description_value, "html.parser")
            df.loc[i, "Description"] = soup.get_text()
        else:
            df.loc[i, "Description"] = ""
    df.to_csv("output2.csv", index=False)

if __name__ == "__main__":
    ai_responses()