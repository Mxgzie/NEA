# from django.shortcuts import render
# from .models import Question, Answer
# from .forms import AnswerForm
# import random
# # Create your views here.

# def view_questions(request):
#     # Get all questions from the database
#     questions = list(Question.objects.all())  # Convert to a list
#     random.shuffle(questions)

#     # Select the first 3 questions after shuffling
#     selected_questions = questions[:3]
#     print("Selected Questions:", [question.Qnum for question in selected_questions])
#     print("POST Keys:", request.POST.keys())
#     if request.method == "POST":
#         for question in selected_questions:
#             # Retrieve the answer for each question using the correct Qnum
#             print(question.Qnum)
#             answer_text = request.POST.get(f'answer_text_{question.Qnum}')
#             print(f"Answer for question {question.Qnum}: {answer_text}")  # Debugging line

#             if answer_text:
#                 # Create the answer if the answer text is provided
#                 Answer.objects.create(
#                     user=request.user,
#                     question=question,
#                     answer_text=answer_text,
#                 )
#                 print("Answer created successfully.")  # Debugging line

#     # Pass the shuffled questions to the template
#     return render(request, 'random.html', {'questions': selected_questions})

from django.shortcuts import render
import random
from .models import Question, Answer

def view_questions(request):
    if request.method == "POST":
        # Retrieve the selected question IDs from the session
        selected_questions_ids = request.session.get('selected_questions', [])
        if selected_questions_ids:
            selected_questions = Question.objects.filter(id__in=selected_questions_ids)

            for question in selected_questions:
                answer_text = request.POST.get(f'answer_text_{question.Qnum}')
                if answer_text:
                    Answer.objects.create(
                        user=request.user,
                        question=question,
                        answer_text=answer_text,
                    )

        # Clear the session after processing answers
        if 'selected_questions' in request.session:
            del request.session['selected_questions']

    # Generate new questions if no session data exists
    if not request.session.get('selected_questions'):
        questions = list(Question.objects.all())
        random.shuffle(questions)
        selected_questions = questions[:3]
        request.session['selected_questions'] = [question.id for question in selected_questions]
        request.session.modified = True

    # Fetch questions for rendering
    selected_questions = Question.objects.filter(id__in=request.session.get('selected_questions', []))
    return render(request, 'random.html', {'questions': selected_questions})
