import os
from typing import Any

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.utilities import WikipediaAPIWrapper

import wikipedia as wp
import wikipediaapi

from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

# embding model
embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

# QA model
model_checkpoint = "Ahmed007/close-book"
question_answerer = pipeline("question-answering", model=model_checkpoint)

# we will make a class that will handle all the steps
class Close_wiki():
    def __init__(self,query,embeddings = embeddings ,question_answerer = question_answerer):
        self.query=query
        self.embeddings=embeddings
        self.question_answerer=question_answerer
        self.wiki_wiki = wikipediaapi.Wikipedia('en') 
        self.page_py = self.wiki_wiki.page(self.query)
        self.text=self.page_py.text
        self.title_index=None
    def get_titles(self):
        title = wp.search(self.query, results = 10)
        # make a dictionary of titles and their indices
        title_dict={}
        for i in range(len(title)):
            title_dict[i]=title[i]

        return title_dict
    
    def set_title_index(self,title_index):
        # take title index as input
        # title_index=int(input("Enter the index of the title you want to use: "))
        self.title_index=title_index
        return title_index
    
    def return_title(self,title_index):
        title_dict=self.get_titles()
        title_index=self.set_title_index(title_index)
        title=title_dict[title_index]
        return title
        
    def get_text(self):
        title_dict=self.get_titles()

        # get the title from the dictionary
        title=title_dict[self.title_index]
        print('the title is: ' + title + '\n')
        wiki_wiki = wikipediaapi.Wikipedia(
        language='en',)
        page_py = wiki_wiki.page(title)
        # print(page_py.text)
        wiki_html = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
        )
        p_html = wiki_html.page(title)

        paragraphs = []
        start = 0
        end = 0
        while True:
            start = p_html.text.find('<p>', end)
            end = p_html.text.find('</p>', start)
            if start == -1 or end == -1:
                break
            paragraphs.append(p_html.text[start+3:end])
            # check if there is folder named res
        if not os.path.exists('res'):
            os.makedirs('res')
        # else:
        #     # remove the res folder content
        #     for file in os.listdir('res'):
        #         os.remove('res/'+file)

        # save the text in a file
        # print(len(paragraphs))
        f = open('res/'+title+'.txt', 'w')
        for i in range(len(paragraphs)):
            f.write(paragraphs[i])
            f.write('\n')

        # load the text
        text_loader = TextLoader('res/'+title+'.txt')
        docs = text_loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=30)
        documents = text_splitter.split_documents(docs)
        return documents
    
    def get_closest(self):
        db = FAISS.from_documents(self.documents, self.embeddings)
        docs_1 = db.similarity_search(self.query)
        return docs_1[0].page_content
    
    def get_answer(self):
        documents=self.get_text()
        self.documents=documents
        closest=self.get_closest()
        answer = self.question_answerer(question=self.query, context=closest)
        return answer

    
    def get_summary(self):
        wikipedia = WikipediaAPIWrapper()
        # get the title
        title_dict=self.get_titles()
        title_index=self.title_index
        # take title index as input
        title=title_dict[title_index]
        summary =  wikipedia.run(title)
        # save the summary in a file
        f = open('res/'+title+'_summary.txt', 'w')
        f.write(summary)
        f.close()
        return summary
    
    def get_summary_answer(self):
        summary=self.get_summary()
        answer = self.question_answerer(question=self.query, context=summary)
        return [answer,summary]
    