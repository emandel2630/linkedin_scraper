
import os
from dotenv import load_dotenv
import openai
import time 
from fitTokenLimit import *
#https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb


def exp_edu_org_profile(profileDict):
    expEduOrg = profileDict
    del expEduOrg[next(iter(profileDict))]["About"]
    del expEduOrg[next(iter(profileDict))]["Licenses_Certifications"]
    del expEduOrg[next(iter(profileDict))]["Volunteering_Experiences"]
    del expEduOrg[next(iter(profileDict))]["Honors_Awards"]
    del expEduOrg[next(iter(profileDict))]["Skills"]
    del expEduOrg[next(iter(profileDict))]["Projects"]
    del expEduOrg[next(iter(profileDict))]["Languages"]
    del expEduOrg[next(iter(profileDict))]["Patents"]
    del expEduOrg[next(iter(profileDict))]["Publications"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        if("Northeastern".lower() not in expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["institution_name"].lower()):
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]
        else:
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["location"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["linkedin_url"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
            del expEduOrg[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]
            

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        if("Northeastern".lower() not in expEduOrg[next(iter(profileDict))]["Educations"][str(i)]["institution_name"].lower()):
            del expEduOrg[next(iter(profileDict))]["Educations"][str(i)]
        else:
            del expEduOrg[next(iter(profileDict))]["Educations"][str(i)]["linkedin_url"]
    
    for i in range(1,len(profileDict[next(iter(profileDict))]["Organizations"].keys())+1):
        try:
            if("Northeastern".lower() not in expEduOrg[next(iter(profileDict))]["Organizations"][str(i)]["name"].lower() or "Northeastern".lower() not in expEduOrg[next(iter(profileDict))]["Organizations"][str(i)]["association"].lower()):
                del expEduOrg[next(iter(profileDict))]["Organizations"][str(i)]
            else:
                del expEduOrg[next(iter(profileDict))]["Organizations"][str(i)]["to_date"]
                del expEduOrg[next(iter(profileDict))]["Organizations"][str(i)]["from_date"]
        except:
            pass
    
    return(expEduOrg)

def extract_NU_Connection(profileDict):


    env_path= os.getcwd() + "/OpenAI_login.env"
    load_dotenv(env_path)

    openai.api_key = os.getenv('KEY')
    model_engine = "gpt-3.5-turbo"

    profile_stripped = exp_edu_org_profile(profileDict)
    max_tokens_limit = 15000
    profile_stripped = str(remove_highest_numbered_fields(profile_stripped,max_tokens_limit))


    fieldPrompt ="""
    Given the following profile describe all of the ways the following person is connected to Northeastern University in as few words as possible:
    Write it in this format: 
    <connection point 1>
    <connection point 2>

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

            firstSent = response['choices'][0]['message']['content']
            break
        except:
            firstSent = "timeout"
            print(firstSent)
            time.sleep(5)

    return firstSent



