from django.db import models


class voteGradeModel(models.Model):
    id_Grade = models.AutoField(primary_key=True)
    grade = models.IntegerField()
    name = models.CharField(max_length=13)

    class Meta:
        verbose_name = "Уровень выборов"
        verbose_name_plural = "Уровень выборов"

    def __str__(self):
        return self.name


class territoryModel(models.Model):
    id_Terr = models.AutoField(primary_key=True)
    id_Grade = models.ForeignKey(voteGradeModel, on_delete=models.CASCADE, verbose_name="Уровень выборов")
    territory_Name = models.CharField(max_length=30, verbose_name="Территория проведения выборов")

    class Meta:
        verbose_name = "Территория"
        verbose_name_plural = "Территория"

    def __str__(self):
        return self.territory_Name


class candidateModel(models.Model):
    id_Candidate = models.AutoField(primary_key=True)
    fio = models.CharField(max_length=30, verbose_name="ФИО")
    description = models.TextField(verbose_name="Описание кандидата")
    image = models.ImageField(verbose_name="Фото кандидата", upload_to="images/")

    class Meta:
        verbose_name = "Кандидаты"
        verbose_name_plural = "Кандидаты"

    def __str__(self):
        return self.fio


class voteModel(models.Model):
    id_Vote = models.AutoField(primary_key=True)
    id_Grade = models.ForeignKey(voteGradeModel, on_delete=models.CASCADE, verbose_name="Уровень выборов")
    id_Terr = models.ForeignKey(territoryModel, on_delete=models.CASCADE, verbose_name="Территория выборов")

    class Meta:
        verbose_name = "Выборы"
        verbose_name_plural = "Выборы"

    def __str__(self):
        return "{0} выборы в {1}".format(self.id_Grade, self.id_Terr)


class voteCandidateModel(models.Model):
    id_Vote = models.ForeignKey(voteModel, on_delete=models.CASCADE, verbose_name="Выборы")
    id_Candidate = models.ForeignKey(candidateModel, on_delete=models.CASCADE, verbose_name="Кандидат")

    def __str__(self):
        return "{0}, {1}".format(self.id_Vote, self.id_Candidate)