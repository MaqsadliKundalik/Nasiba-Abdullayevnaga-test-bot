from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tests(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='tests')
    test_keys = fields.TextField()
    test_code = fields.CharField(max_length=20)
    status = fields.CharField(max_length=20, default='active')
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'Test {self.id} for {self.user.name} with keys {self.test_keys}'

class UserAnswers(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='answers')
    test = fields.ForeignKeyField('models.Tests', related_name='user_answers')
    score = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'Answers of {self.user.name} for Test {self.test.id}: {self.score}'