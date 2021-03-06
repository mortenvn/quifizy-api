from models import Round, Question, Song, Category
import random


def generate_round(game, category, whos_turn):
    round = Round.objects.create(category=category, game=game, status='active', whos_turn=whos_turn)
    songs = list(Song.objects.filter(category=Category.objects.get(id=category.id)))
    number_of_questions = 5

    for i in range(0, number_of_questions):
        random.shuffle(songs)
        correct_ans = songs.pop()
        alternatives = songs[:3]
        question = Question.objects.create(round=round, correct_answer=correct_ans)
        question.alternatives.add(*alternatives)
        question.save()
    return round
