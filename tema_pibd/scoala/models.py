from django.db import models
from django.db import connection

# Create your models here.
class Elev(models.Model):
    idelev          = models.AutoField(primary_key=True, db_column="idelev")
    nume          = models.CharField(max_length=35)
    prenume       = models.CharField(max_length=35)
    an            = models.PositiveSmallIntegerField()

    def __repr__(self):
        return f'<Elevi: Elev object ({self.idelev}, {self.nume}, {self.prenume}, {self.an}>'
    def __str__(self):
        return f'<Elevi: Elev object ({self.idelev}, {self.nume}, {self.prenume}, {self.an}>'

    class Meta:
        managed = False
        db_table = "elevi"

class Profesor(models.Model):
    idprofesor      = models.AutoField(primary_key=True, db_column="idprofesor")
    nume          = models.CharField(max_length=35)
    prenume       = models.CharField(max_length=35)

    def __repr__(self):
        return f'<Profesori: Profesor object ({self.idprofesor}, {self.nume}, {self.prenume}>'
    def __str__(self):
        return f'<Profesori: Profesor object ({self.idprofesor}, {self.nume}, {self.prenume}>'

    class Meta:
        managed = False
        db_table = "profesori"

class Disciplina(models.Model):
    iddisciplina    = models.AutoField(primary_key=True, db_column="iddisciplina")
    nume            = models.CharField(max_length=35)
    profesor        = models.ForeignKey(Profesor, on_delete=models.CASCADE, db_column="idprofesor")

    def __repr__(self):
        return f'<Discipline: Disciplina object ({self.iddisciplina}, {self.nume}, {self.profesor.__repr__()}>'
    def __str__(self):
        return f'<Discipline: Disciplina object ({self.iddisciplina}, {self.nume}, {self.profesor.__repr__()}>'

    class Meta:
        managed = False
        db_table = "discipline"

class Aranjament(models.Model):
    elev          = models.ForeignKey(Elev, on_delete=models.CASCADE, db_column="idelev")
    disciplina    = models.ForeignKey(Disciplina, on_delete=models.CASCADE, db_column="iddisciplina")

    def __str__(self):
        return f'<Aranjament object ({self.elev.idelev}, {self.disciplina.iddisciplina}>'

    def __repr__(self):
        return f'<Aranjamente: Aranjament object ({self.elev.idelev}, {self.disciplina.iddisciplina}>'

    def all():
        cursor = connection.cursor()
        cursor.execute('select iddisciplina, idelev from aranjamente;')
        return list(cursor.fetchall())

    def get(iddisciplina: int = 0 , idelev: int = 0):
        cursor = connection.cursor()
        if idelev != 0 and iddisciplina != 0:
            cursor.execute('select iddisciplina, idelev from aranjamente where iddisciplina = `' + str(iddisciplina) + '` and idelev = `' + str(idelev) + '`;')
            return cursor.fetchall()
        else:
            if idelev != 0:
                cursor.execute('select iddisciplina, idelev from aranjamente where idelev = `' + str(idelev) + '`;')
                return cursor.fetchall()
            if iddisciplina != 0:
                cursor.execute('select iddisciplina, idelev from aranjamente where iddisciplina = `' + str(iddisciplina) + '`;')
                return cursor.fetchall()
        return None;

    def exist(iddisciplina: int, idelev: int):
        cursor = connection.cursor()
        cursor.execute('select iddisciplina, idelev from aranjamente;')
        return (int(iddisciplina), int(idelev)) in cursor.fetchall()

    def add(iddisciplina: int, idelev: int):
        if iddisciplina != None and idelev != None:
            if not Aranjament.exist(iddisciplina=iddisciplina, idelev=idelev):
                cursor = connection.cursor()
                cursor.execute(f'insert into aranjamente(iddisciplina, idelev) values({int(iddisciplina)}, {int(idelev)});')
                return True
        return False

    def modify(iddisciplina_old: int, idelev_old: int, iddisciplina_new: int, idelev_new: int):
        if not Aranjament.exist(iddisciplina=iddisciplina_new, idelev=idelev_new) and Aranjament.exist(iddisciplina=iddisciplina_old, idelev=idelev_old):
            cursor = connection.cursor()
            cursor.execute(f'update aranjamente set iddisciplina = {iddisciplina_new}, idelev = {idelev_new} where iddisciplina = {iddisciplina_old} and idelev = {idelev_old};')
            return True
        return False
    def delete(iddisciplina: int, idelev: int):
        if iddisciplina != None and idelev != None:
            if Aranjament.exist(iddisciplina=iddisciplina, idelev=idelev):
                cursor = connection.cursor()
                cursor.execute(f'delete from aranjamente where iddisciplina = {int(iddisciplina)} and idelev = {int(idelev)};')
                return True
        return False

    class Meta:
        managed = False
        db_table = "aranjamente"
        unique_together = (('elev', 'disciplina'),)