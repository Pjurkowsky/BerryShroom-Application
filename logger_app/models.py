from django.db import models


class Log(models.Model):
    LOGGERS = [('DEBUG', 'DEBUG'), ('INFO', 'INFO'), ('WARNING', 'WARNING'),
               ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')]
    logger = models.CharField(max_length=8, choices=LOGGERS, default='ERROR')
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-datetime']
