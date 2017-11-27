from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    active = models.BooleanField(default='true')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    choice_picture = models.ImageField(upload_to='imgs/', max_length=200, blank='true')

    def __str__(self):
        return self.choice_text


#Для проверки на повторное голосование с одногоIP
class Ipcheck(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    check_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)

    def __str__(self):
        return str(self.user_ip)
