import os
from dotenv import load_dotenv
import openai
import time 
from fitTokenLimit import *

def suitability_clean(profileDict):
    cleanProfile = profileDict

    ######### Delete whole sections ########
    # del cleanProfile[next(iter(profileDict))]["About"]
    # del cleanProfile[next(iter(profileDict))]["Experiences"]
    # del cleanProfile[next(iter(profileDict))]["Educations"]
    # del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"]
    # del cleanProfile[next(iter(profileDict))]["Volunteering_Experiences"]
    # del cleanProfile[next(iter(profileDict))]["Honors_Awards"]
    # del cleanProfile[next(iter(profileDict))]["Organizations"]
    # del cleanProfile[next(iter(profileDict))]["Skills"]
    # del cleanProfile[next(iter(profileDict))]["Publications"]
    # del cleanProfile[next(iter(profileDict))]["Patents"]
    # del cleanProfile[next(iter(profileDict))]["Projects"]
    # del cleanProfile[next(iter(profileDict))]["Languages"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["from_date"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["location"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_name"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
        del cleanProfile[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]
            

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Educations"][str(i)]["from_date"]
        del cleanProfile[next(iter(profileDict))]["Educations"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Educations"][str(i)]["associated_skills"]
        del cleanProfile[next(iter(profileDict))]["Educations"][str(i)]["grade"]
        del cleanProfile[next(iter(profileDict))]["Educations"][str(i)]["linkedin_url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Licenses_Certifications"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["issuer"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["from_date"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["expired"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["credID"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["url"]
        del cleanProfile[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["associated_skills"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Volunteering_Experiences"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["from_date"]
        del cleanProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["duration"]
        del cleanProfile[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["url"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Publications"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Publications"][str(i)]["date"]
        del cleanProfile[next(iter(profileDict))]["Publications"][str(i)]["url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Patents"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Patents"][str(i)]["applicationNo"]
        del cleanProfile[next(iter(profileDict))]["Patents"][str(i)]["status"]
        del cleanProfile[next(iter(profileDict))]["Patents"][str(i)]["url"]
        del cleanProfile[next(iter(profileDict))]["Patents"][str(i)]["date"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Projects"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Projects"][str(i)]["from_date"]
        del cleanProfile[next(iter(profileDict))]["Projects"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Projects"][str(i)]["url"]

   
    for i in range(1,len(profileDict[next(iter(profileDict))]["Honors_Awards"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Honors_Awards"][str(i)]["date"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Organizations"].keys())+1):
        del cleanProfile[next(iter(profileDict))]["Organizations"][str(i)]["to_date"]
        del cleanProfile[next(iter(profileDict))]["Organizations"][str(i)]["from_date"]

    return(cleanProfile)


def extract_position_suitability(profileDict, jobDescription):


    env_path= os.getcwd() + "/OpenAI_login.env"
    load_dotenv(env_path)

    openai.api_key = os.getenv('KEY')
    model_engine = "gpt-3.5-turbo"

    profile_stripped = suitability_clean(profileDict)
    max_tokens_limit = 12000
    profile_stripped = str(remove_highest_numbered_fields(profile_stripped,max_tokens_limit))


    fieldPrompt =""" I will give you a candidate and a job brief. Assess the candidates suitability for the job in a short paragraph. First state if the candidate has the qualifications for the position and discuss if their area of knowledge is a good fit with the position then discuss pros of the candidate first and then end with cons.\n
    """ + "Candidate: " +  profile_stripped +"\n\n Job Description: " + jobDescription

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