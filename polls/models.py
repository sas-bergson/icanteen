from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=200) # text varchar(200) not null
    publication_date = models.DateTimeField('date published') # publication_date date not null

    # getters
    def getText(self):
        return self.text
    def getPublicationDate(self):
        return self.publication_date
    
    #setters
    def setText(self, txt):
        self.text = txt
    def setPublicationDate(self, pub_date):
        self.publication_date = pub_date
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    text = models.CharField(max_length=200) # text varchar(200) not null
    votes = models.IntegerField(default=0) # votes integer default 0 not null
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    #getters
    def getText(self):
        return self.text
    def getVotes(self):
        return self.votes
    def getQuestionId(self):
        return self.question_id
    
    #setters
    def setText(self, txt):
        self.text = txt
    def setVotes(self, votes):
        self.votes = votes
    def setQuestionId(self, q_id):
        self.question_id = q_id
    
    
    def __str__(self):
        return self.text

