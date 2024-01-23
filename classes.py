from config import questions, animals_answers, answer_choice
import random as rnd


class User:
    def __init__(self):
        self.result = {k: 0 for k in animals_answers.keys()}
        self.answers = []

    def quiz(self):
        count = 0
        for question, answers in questions.items():
            print('|', end='')
            count += 1
            yield f'{count}. {question}'
            my_dict = {answer: answer_choice[i] for i, answer in enumerate(answers)}
            keys = list(my_dict.keys())
            rnd.shuffle(keys)
            new_dict = {}
            for key in keys:
                new_dict[key] = my_dict[key]
            yield new_dict

    def add_answer(self, answer):
        self.answers.append(answer)

    def result_func(self):
        for animal, animal_answers in animals_answers.items():
            for i in range(len(animal_answers)):
                if animal_answers[i] == self.answers[i]:
                    self.result[animal] += 1
        mx = 0
        mx_animal = None
        for animal, score in self.result.items():
            if score > mx:
                mx = score
                mx_animal = animal
        return mx_animal


if __name__ == '__main__':
    user = User()
    print(user.result.keys())