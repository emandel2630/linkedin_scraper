
import os
from dotenv import load_dotenv
import openai
import time 
from fitTokenLimit import *
#https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb




def quant_achieve_profile(profileDict):
    quantAch = profileDict
    del quantAch[next(iter(profileDict))]["About"]
    del quantAch[next(iter(profileDict))]["Licenses_Certifications"]
    del quantAch[next(iter(profileDict))]["Skills"]
    del quantAch[next(iter(profileDict))]["Languages"]
    
    #delete keys with field as an empty dict
    quantAch = {key: value for key, value in quantAch.items() if value != {}}

    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["location"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["from_date"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["to_date"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["linkedin_url"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
        del quantAch[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        del quantAch[next(iter(profileDict))]["Educations"][str(i)]["institution_name"]
        del quantAch[next(iter(profileDict))]["Educations"][str(i)]["degree"]
        del quantAch[next(iter(profileDict))]["Educations"][str(i)]["from_date"]
        del quantAch[next(iter(profileDict))]["Educations"][str(i)]["to_date"]
        del quantAch[next(iter(profileDict))]["Educations"][str(i)]["associated_skills"]
    
    for i in range(1,len(profileDict[next(iter(profileDict))]["Volunteering_Experiences"].keys())+1):
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["organization"]
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["cause"]
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["from_date"]
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["to_date"]
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["duration"]
        del quantAch[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Publications"].keys())+1):
        del quantAch[next(iter(profileDict))]["Publications"][str(i)]["publisher"]
        del quantAch[next(iter(profileDict))]["Publications"][str(i)]["date"]
        del quantAch[next(iter(profileDict))]["Publications"][str(i)]["url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Patents"].keys())+1):
        del quantAch[next(iter(profileDict))]["Patents"][str(i)]["applicationNo"]
        del quantAch[next(iter(profileDict))]["Patents"][str(i)]["status"]
        del quantAch[next(iter(profileDict))]["Patents"][str(i)]["url"]
        del quantAch[next(iter(profileDict))]["Patents"][str(i)]["date"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Projects"].keys())+1):
        del quantAch[next(iter(profileDict))]["Projects"][str(i)]["from_date"]
        del quantAch[next(iter(profileDict))]["Projects"][str(i)]["to_date"]
        del quantAch[next(iter(profileDict))]["Projects"][str(i)]["url"]
        del quantAch[next(iter(profileDict))]["Projects"][str(i)]["association"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Honors_Awards"].keys())+1):
        del quantAch[next(iter(profileDict))]["Honors_Awards"][str(i)]["issuer"]
        del quantAch[next(iter(profileDict))]["Honors_Awards"][str(i)]["date"]
        del quantAch[next(iter(profileDict))]["Honors_Awards"][str(i)]["association"]
        del quantAch[next(iter(profileDict))]["Honors_Awards"][str(i)]["description"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Organizations"].keys())+1):
        del quantAch[next(iter(profileDict))]["Organizations"][str(i)]["from_date"]
        del quantAch[next(iter(profileDict))]["Organizations"][str(i)]["to_date"]
        del quantAch[next(iter(profileDict))]["Organizations"][str(i)]["association"]
        del quantAch[next(iter(profileDict))]["Organizations"][str(i)]["position"]

    
    return(quantAch)


def extract_quant_ach(profileDict):


    env_path= os.getcwd() + "/OpenAI_login.env"
    load_dotenv(env_path)

    openai.api_key = os.getenv('KEY')
    model_engine = "gpt-3.5-turbo-16k"

    profile_stripped = quant_achieve_profile(profileDict)
    max_tokens_limit = 15000
    profile_stripped = str(remove_highest_numbered_fields(profile_stripped,max_tokens_limit))
    fieldPrompt ="""
    Given the following profile describe all of the achievements this person has that explicitly provide some quantifiable measurement of success for example dollars earned or number of people helped in as few words as possible:
    Write it in this format: 
    <achievement 1>
    <achievement 2>

    If there is no valuable information just output "None"
    """ + profile_stripped

    for i in range(0,3):
        try:
            response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant focused on extracting useful information from resumes."},
                {"role": "user", "content": fieldPrompt},
            ],
            temperature=0,
            )

            response = response['choices'][0]['message']['content']
            break
        except:
            response = "timeout"
            time.sleep(5)

    return response



