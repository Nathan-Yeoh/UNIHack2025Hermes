import openai
import langchain
import PyPDF2

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI

from DBHandler import DBHandler
from Entities.Classroom import Classroom
from Entities.Classroom_TestPaper import Classroom_TestPaper
from Entities.Skill import Skill
from Entities.Skill_TestPaper import Skill_TestPaper
from Entities.Student import Student
from Entities.Student_Classroom import Student_Classroom
from Entities.Teacher import Teacher
from Entities.TestPaper import TestPaper
from Entities.Test_Result import Test_Result




class OpenaiHandler:

    openai_api_key = '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'

    template = """
        test paper: {test_paper}

        valid skills: {skill_list}

        for each question in this test paper, could you please output the following in a list:
        [question number, question text, [skill1$ skill2$ skill3], question marks]ඞ
        
        rules:
        -please do not output anything except for the list items
        -do not output anything outside of the square brackets [] except for ඞ
        -please make sure the output skills are a part of the given valid skills
        -if there are less than three valid skills, you may output less than three
        -at most, 3 skills can be output for each question
        -make sure every question from  in the test paper has been considered

        example:
        testpaper:
        1.What are the four seasons of the year? (5 marks)
        2.If you have a pencil, a book, and a rubber, which one would you use to write? (3 marks)
        3.What is your favorite color? Can you think of 3 things that are that color? (4 marks)
        output:
        1# What are the four seasons of the year?# Memory$ Perception$ Application# 3ඞ
        2# If you have a pencil, a book, and a rubber, which one would you use to write?# Problem Solving$ Language$ Logical Reasoning# 3ඞ
        3# What is your favorite color? Can you think of 3 things that are that color?# Creativity$ Application$ Memory# 3ඞ
    """

    prompt = PromptTemplate(input_variables=['test_paper', 'skill_list'], template=template)

    llm = OpenAI(api_key=openai_api_key)

    qa_chain = LLMChain(llm=llm, prompt=prompt)
    
    @staticmethod
    def insert_pdf_into_database(filename: str, tp_id: int, cl_id: str, cltp_name: str):
        skills = " ".join(DBHandler.get_all_skill_names())
        data = DBHandler.get_file(filename)
        pdf_text = OpenaiHandler.extract_text_from_pdf(data)
        output = OpenaiHandler.qa_chain.run(test_paper=pdf_text, skill_list=skills)
        print(output)
        formatted = OpenaiHandler.output_to_list(output)
        DBHandler.add_to_classroom_testpaper(cl_id, tp_id, cltp_name)
        
        for question in formatted:
            DBHandler.add_to_testpaper(tp_id, question[0], question[1], question[3])
            for skill in question[2]:
                sk_id = DBHandler.get_sk_id_by_name(skill).sk_id
                DBHandler.add_to_skill_testpaper(tp_id, question[0], sk_id)


    @staticmethod
    def extract_text_from_pdf(data):
        with open("output.pdf", "wb") as output_file:
            output_file.write(data)
        pdfFile = PyPDF2.PdfReader("output.pdf")
        output = ""
        for page in pdfFile.pages:
            output += page.extract_text()
        return output

    @staticmethod
    def output_to_list(txt):
        outerlist = txt.strip("ඞ").split("ඞ")
        output = []
        for i in outerlist:
            init = i.strip("\n").split("#")
            temp = [int(init[0]), init[1].strip(" "), [x.strip(" ") for x in init[2].strip(" ").split("$")], int(init[3])]
            output.append(temp)

        return output
