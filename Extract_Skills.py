# load default skills data base
import NUGigSkillNER
from NUGigSkillNER.general_params import SKILL_DB
# import skill extractor
from NUGigSkillNER.skill_extractor_class import SkillExtractor
from nltk.corpus import stopwords


import warnings
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import json
import os
import sys
import copy
import re
from collections import Counter



def clean_skills(skills):
    combinedSkills = skills["Hard Skill"]+skills["Soft Skill"]
    #countHard = Counter(skills["Hard Skill"])
    #print(countHard)
    #counterHardSorted = sorted(countHard.items(), key=lambda n: n[1], reverse=True)
    skill_counter =Counter(combinedSkills)
    counterSorted = sorted(combinedSkills, key=Counter(combinedSkills).get, reverse=True)
    

    return counterSorted

def round_numbers(string):
    pattern = "\d+\.\d{4,}"
    matches = re.findall(pattern, string)

    for match in matches:
        rounded_number = round(float(match), 4)
        string = string.replace(match, str(rounded_number))

    return string

def sort_skills_based_on_counter(skill_counter, linkedin_skills, extracted_skills):
    # Sort LinkedIn skills with corresponding extracted skills from greatest to least frequency
    sorted_linkedin_skills_with_extracted = sorted(
        [skill for skill in linkedin_skills if skill_counter[skill] > 0],
        key=lambda skill: skill_counter[skill],
        reverse=True
    )
    
    # Sort extracted skills with more than one appearance but no corresponding LinkedIn skill
    sorted_extracted_skills_no_linkedin = sorted(
        [skill for skill in extracted_skills if skill_counter[skill] > 1 and skill not in linkedin_skills],
        key=lambda skill: skill_counter[skill],
        reverse=True
    )
    
    # LinkedIn skills with no corresponding extracted skill
    unmatched_linkedin_skills = [
        skill for skill in linkedin_skills if skill_counter[skill] == 0
    ]
    
    # Extracted skills with one appearance and no corresponding LinkedIn skill
    sorted_extracted_skills_one_no_linkedin = sorted(
        [skill for skill in extracted_skills if skill_counter[skill] == 1 and skill not in linkedin_skills],
        key=lambda skill: skill_counter[skill],
        reverse=True
    )
    
    return (
        sorted_linkedin_skills_with_extracted +
        sorted_extracted_skills_no_linkedin +
        unmatched_linkedin_skills +
        sorted_extracted_skills_one_no_linkedin
    )

def skillNer_extraction(resume,nlp):
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


    annotations = skill_extractor.annotate(resume)

  
    
    annotations= round_numbers(str(annotations))
    annotation_dict = eval(annotations)
    
    with open("skills.json", "w") as write_file:
        json.dump(annotation_dict, write_file, indent=4, sort_keys=True)
    
    skill_types =[]
    skills = []
    skills_expanded = []

    
    for matches in annotation_dict['results']:
        for i in range(0,len(annotation_dict['results'][matches])):
            skill_types.append(SKILL_DB[annotation_dict['results'][matches][i]["skill_id"]]['skill_type'])
            skills.append(annotation_dict['results'][matches][i]["doc_node_value"])
            skills_expanded.append(SKILL_DB[annotation_dict['results'][matches][i]["skill_id"]]['skill_name'])


    hard = []
    soft =[]
    soft_expanded = []
    hard_expanded =[]
    for i in range(0,len(skills)):
        if skill_types[i] == 'Hard Skill':
            hard.append(skills[i])
            hard_expanded.append(skills_expanded[i])
        else:
            soft.append(skills[i])
            soft_expanded.append(skills_expanded[i])
    
    skill_dict = {"Hard Skill" : hard , "Hard Skill Expanded": hard_expanded, "Soft Skill": soft, "Soft Skill Expanded": soft_expanded}
            
            
    return(skill_dict)

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def remove_duplicates_and_retain_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result



def clean_profile(profileDict):
    cleanProfile_Extract_Skills = profileDict

    ######### Delete whole sections ########
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["About"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Volunteering_Experiences"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Honors_Awards"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Organizations"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Skills"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Publications"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Patents"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Projects"]
    # del cleanProfile_Extract_Skills[next(iter(profileDict))]["Languages"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Experiences"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["duration"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["location"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["location_type"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["employment_type"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["associated_skills"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["linkedin_url"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["institution_name"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["institution_desc"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["institution_size"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["institution_specialties"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Experiences"][str(i)]["institution_url"]
            

    for i in range(1,len(profileDict[next(iter(profileDict))]["Educations"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"][str(i)]["associated_skills"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"][str(i)]["grade"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Educations"][str(i)]["linkedin_url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Licenses_Certifications"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["issuer"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["expired"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["credID"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["url"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Licenses_Certifications"][str(i)]["associated_skills"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Skills"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Skills"][str(i)]["usage"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Volunteering_Experiences"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["duration"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Volunteering_Experiences"][str(i)]["url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Publications"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Publications"][str(i)]["publisher"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Publications"][str(i)]["date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Publications"][str(i)]["url"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Patents"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Patents"][str(i)]["applicationNo"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Patents"][str(i)]["status"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Patents"][str(i)]["url"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Patents"][str(i)]["date"]

    for i in range(1,len(profileDict[next(iter(profileDict))]["Projects"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Projects"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Projects"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Projects"][str(i)]["url"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Projects"][str(i)]["association"]


   
    for i in range(1,len(profileDict[next(iter(profileDict))]["Honors_Awards"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Honors_Awards"][str(i)]["issuer"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Honors_Awards"][str(i)]["date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Honors_Awards"][str(i)]["association"]


    for i in range(1,len(profileDict[next(iter(profileDict))]["Organizations"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Organizations"][str(i)]["to_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Organizations"][str(i)]["from_date"]
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Organizations"][str(i)]["association"]
    
    for i in range(1,len(profileDict[next(iter(profileDict))]["Languages"].keys())+1):
        del cleanProfile_Extract_Skills[next(iter(profileDict))]["Languages"][str(i)]["proficiency"]

    return(cleanProfile_Extract_Skills)



def extract_skills(resume, resumeDict, nlp):
    extractedSkills = []

    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        skills = skillNer_extraction(resume,nlp)
        extractedSkills = clean_skills(skills)



    #Get skills explicitly stated on profile
    linkedinSkills = []
    for i in range(1,len(resumeDict[next(iter(resumeDict))]["Skills"].keys())+1):
        linkedinSkills.append(resumeDict[next(iter(resumeDict))]["Skills"][str(i)]["name"])

    extract_skills = []
    for string in extractedSkills:
        new_string = string.title()
        extract_skills.append(new_string)

    #Remove duplicates from a list but retain order
    skills = sort_skills_based_on_counter(Counter(extract_skills), linkedinSkills,extract_skills)
    skills = remove_duplicates_and_retain_order(skills)

    return skills


def convert_dict_to_string(d):
    result = ""
    for value in d.values():
        if isinstance(value, dict):
            result += convert_dict_to_string(value)
        else:
            if value is not None:
                result += str(value) + "\n"
    return result

def remove_urls(text):
    pattern = re.compile(r'(https?://\S+|www\.\S+)')
    return re.sub(pattern, '', text)

#Pull resume dict from file
with open("DemoProfiles/ethan-mandel-61b549221-Profile.json") as json_file:
    resumeDict = json.load(json_file)

#Clean resume for easier parsing
resumeDict= clean_profile(resumeDict)
resumeDictCopy = copy.deepcopy(resumeDict)
del resumeDictCopy[next(iter(resumeDictCopy))]["Skills"]    
resume = convert_dict_to_string(resumeDictCopy)
resume = remove_urls(resume)

# Convert the dictionary to a nicely formatted JSON string
formatted_json = json.dumps(resumeDict, indent=4)

# Print the formatted JSON string
print(formatted_json)
print("\n")
print(next(iter(resumeDict)) + " Profile Insights:")
print("\n")
nlp = spacy.load('en_core_web_lg')

################################# SKILLZ #################################

skills = extract_skills(resume,resumeDict,nlp)
print(skills)
