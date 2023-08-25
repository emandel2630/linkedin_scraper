
import os
from dotenv import load_dotenv
import openai
import time
import nltk
from fitTokenLimit import *

#https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb


def exp_edu_profile(profileDict):
    expAndEdu = profileDict
    del expAndEdu[next(iter(profileDict))]["Licenses_Certifications"]
    del expAndEdu[next(iter(profileDict))]["Volunteering_Experiences"]
    del expAndEdu[next(iter(profileDict))]["Skills"]
    del expAndEdu[next(iter(profileDict))]["Projects"]
    del expAndEdu[next(iter(profileDict))]["Honors_Awards"]
    del expAndEdu[next(iter(profileDict))]["Organizations"]
    del expAndEdu[next(iter(profileDict))]["Languages"]
    del expAndEdu[next(iter(profileDict))]["Patents"]
    del expAndEdu[next(iter(profileDict))]["Publications"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["location"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["linkedin_url"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
        del expAndEdu[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        del expAndEdu[next(iter(profileDict))]["Educations"][str(i)]["linkedin_url"]

    return(expAndEdu)




def extract_field(profileDict):


    env_path= os.getcwd() + "/OpenAI_login.env"
    load_dotenv(env_path)

    openai.api_key = os.getenv('KEY')
    model_engine = "gpt-3.5-turbo"

    profile_stripped = exp_edu_profile(profileDict)

    # Maximum token limit
    max_tokens_limit = 15000

    # Removing subsections to fit under the token limit (based on highest numbers first)
    profile_stripped = str(remove_highest_numbered_fields(profile_stripped,max_tokens_limit))


    fieldPrompt ="""
    Given the following about, experiences, and education state what field the following person you may also state any concentration or focus as well. 
    Weigh more recent experiences more heavily. 
    Write it in this format: <Field> with a focus in <Concentration/Focus> \n\n
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

            firstSent = response['choices'][0]['message']['content'].split(".")[0]
            break
        except:
            firstSent = "Timeout"
            time.sleep(5)
        

    

    return firstSent



