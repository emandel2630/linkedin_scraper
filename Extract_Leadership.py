
import os
from dotenv import load_dotenv
import openai
import time 
from fitTokenLimit import *
#https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb


def leadership_profile(profileDict):
    leadershipProfile = profileDict
    del leadershipProfile[next(iter(profileDict))]["Skills"]
    del leadershipProfile[next(iter(profileDict))]["Publications"]
    del leadershipProfile[next(iter(profileDict))]["Patents"]
    del leadershipProfile[next(iter(profileDict))]["Projects"]
    del leadershipProfile[next(iter(profileDict))]["Languages"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["location"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["linkedin_url"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
        del leadershipProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]
            

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Educations"][str(i)]["grade"]
        del leadershipProfile[next(iter(profileDict))]["Educations"][str(i)]["linkedin_url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Licenses_Certifications"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["issuer"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["to_date"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["from_date"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["expired"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["credID"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["url"]
        del leadershipProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["associated_skills"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Volunteering_Experiences"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["cause"]
        del leadershipProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["to_date"]
        del leadershipProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["from_date"]
        del leadershipProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["duration"]
        del leadershipProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["url"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Honors_Awards"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Honors_Awards"][str(i)]["issuer"]
        del leadershipProfile[next(iter(profileDict))]["Honors_Awards"][str(i)]["date"]
        del leadershipProfile[next(iter(profileDict))]["Honors_Awards"][str(i)]["association"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Organizations"].keys())+1):
        del leadershipProfile[next(iter(profileDict))]["Organizations"][str(i)]["to_date"]
        del leadershipProfile[next(iter(profileDict))]["Organizations"][str(i)]["from_date"]
    
    return(leadershipProfile)

def extract_leadership(profileDict):


    env_path= os.getcwd() + "/OpenAI_login.env"
    load_dotenv(env_path)

    openai.api_key = os.getenv('KEY')
    model_engine = "gpt-3.5-turbo"

    profile_stripped = leadership_profile(profileDict)
    max_tokens_limit = 15000
    profile_stripped = str(remove_highest_numbered_fields(profile_stripped,max_tokens_limit))


    fieldPrompt ="""
    Given the following profile describe the leadership skills the person has in a few sentances making sure to site specific examples in the profile. Do this in sentance format not a numbered list. 
    If they have not stated anything that demonstrates leadership just output "None"
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
            time.sleep(5)

    return firstSent



