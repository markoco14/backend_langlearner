from django.db import models

# Create your models here.

class Word(models.Model):
    traditional = models.CharField(max_length=255, db_index=True, verbose_name="Traditional Characters")
    simplified = models.CharField(max_length=255, db_index=True, verbose_name="Simplified Characters")
    pinyin = models.CharField(max_length=255, db_index=True, verbose_name="Pinyin Letters")
    english = models.TextField()
	
    def __str__(self):
        return f"{self.traditional} ({self.simplified}) - {self.english}"
    
    class Meta:
        db_table='cedict_words'
		