from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import Question, Answer, Markscheme
import requests
import random
import os
from mistralai import Mistral
import re

#OLD VIEW THAT IS WORKING TO DISPLAY QUESTIONS
# def view_questions(request):

#     if request.method == "POST": #Checking if the user has filled out the form and is submitting its answers

#         #When a user first visits the page, the server doesn't know anything about that user yet (because they haven’t done anything yet). 
#         #This page generates a new set of questions and stores their IDs in the session. The session's ID is then sent back to the user's browser as a cookie, so the server knows who the user is on subsequent requests.
#         #When the user comes back to the page, the browser sends the session ID back to the server. Using this ID, the server can retrieve the stored session data (the question IDs in this case). This allows the server to know which questions the user had already seen.
        

#         # When the user submits answers, the server retrieves the selected question IDs
#         # from the session and saves the user's answers to the database. This allows 
#         # the user to continue with the same set of questions even after page reloads 
#         # or submitting answers, ensuring persistence without needing to re-select questions.

#         # Retrieve the selected question IDs from the session. If the key doesn't exist, it returns an empty list 
#         selected_questions_ids = request.session.get('selected_questions', [])

#         if selected_questions_ids: #Checks if questions have been selected. Empty list returns False, non-empty list returns True
#             selected_questions = Question.objects.filter(id__in=selected_questions_ids) #Retrieves the question objects from the database whose ID matches the ID in the selected questions from the session

#             for question in selected_questions:
#                 answer_text = request.POST.get(f'answer_text_{question.Qnum}') #Tries to get the user's answer for the current question
#                 if answer_text: #IF THE USER HAS ENTERED AN ANSWER
#                     Answer.objects.create(
#                         user=request.user,
#                         question=question,
#                         answer_text=answer_text,
#                     ) #Create a new Answer object with the user, question object, and the user's answer 

#         # Clear the session after processing answers
#         if 'selected_questions' in request.session: #Checks if the key exists in the session data. If it does, delete the key-pair
#             del request.session['selected_questions']
#             #This prevents the same questions from being displayed again if the user refreshes or revisits the page, as the condition to generate new questions is that this key doesn't exist in the dictionary

#     # Generate new questions if no "selected_questions" key exists in the session data - e.g. WHEN THE USER FIRST VISITS THE PAGE or REFRESHES or SUBMITS ANSWERS
#     if not request.session.get('selected_questions'): #If the selected_questions key doesn't exist in the dictionary, it returns None which evaluates to False
#         questions = list(Question.objects.all()) #Retrieves all questions objects from the table and stores them as a list in "questions"
#         random.shuffle(questions) #Shuffles the questions in the list
#         selected_questions = questions[:3] #Picks the first 3 questions from the list

#         #Request.session is the dictionary object to store session data. 
#         request.session['selected_questions'] = [question.id for question in selected_questions] #Since we are accessing request.session["selected_questions"] for the FIRST TIME, Django will initalize the key-pair automatically with the data we've given it (the list of question IDS)
#         request.session.modified = True #Flag Django uses to determine if session data has been modified during current request. By setting it to True we tell Django that the session data needs to be saved back to the session storage so the new value for 'selected_questions' will be saved and available in future requests. 

#     # Fetch questions for rendering
#     # After the session is set with the question IDs, we need to fetch the full Question objects again. This is because the session only stores the IDs, not the actual Question objects with all their fields.
#     #Using the selected_questions list before storing them in the session might cause mismatches between what the user sees and what gets saved in the database because the session stores only the IDs, not the full question objects.
#     selected_questions = Question.objects.filter(id__in=request.session.get('selected_questions', []))
#     return render(request, 'random.html', {'questions': selected_questions})


def view_questions(request):

    if request.method == "POST":  # User is submitting answers

        # Retrieve the selected question IDs from the session
        selected_questions_ids = request.session.get('selected_questions', [])
        feedback = []

        if selected_questions_ids:
            selected_questions = Question.objects.filter(id__in=selected_questions_ids)

            for question in selected_questions:
                answer_text = request.POST.get(f'answer_text_{question.Qnum}')
                if answer_text:  # If the user has entered an answer
                    # Save the answer to the database
                    Answer.objects.create(user=request.user, question=question, answer_text=answer_text)

                    # Get the related mark scheme for the current question
                    try:
                        mark_scheme = Markscheme.objects.get(question=question)  # Fetch the related mark scheme
                        mark_scheme_content = mark_scheme.points
                    except Markscheme.DoesNotExist:
                        mark_scheme_content = "No mark scheme available."

                    # Prepare the AI prompt
                    prompt = f"""<PLEASE DO NOT INCLUDE THE PROMPT IN YOUR GENERATED RESPONSE OR ANY PARTS OF THE PROMPT.
                    
                    I'm going to give you a student's answer to an exam question and the mark scheme for that respective question. The question's markschemes use the follow annotations:
                    
                    ; - means a single mark
                    // - means alternative response
                    / - means an alternative word or sub-phrase
                    A. - means acceptable creditworthy answer
                    R. - means reject answer as not creditworthy
                    NE. - means not enough for a mark
                    I. - means ignore
                    DPT. - in some questions a specific error made by a candidate, if repeated, could result in the loss of more than one mark. The DPT label indicates that this mistake should only result in a candidate losing one mark on the first occasion that the error is made.
                    Provided that the answer remains understandable, subsequent marks should be awarded as if the error was not being repeated

                    The question being answered is: {question.text}
                    The User's Answer is: {answer_text}
                    The Mark Scheme: {mark_scheme_content}

                    For mark schemes that contain level descriptors, use the following instructions when marking. Mark schemes will contain level descriptors if they have the word "LEVEL" in them.
                        Each level has a descriptor. The descriptor for the level shows the average performance for the level. There are marks in each level.
                        Before you apply the mark scheme to a student's answer read through the answer and annotate it (as instructed) to show the qualities that are being looked for. You can then apply the mark scheme.

                        Step 1 Determine a level
                        Start at the lowest level of the mark scheme and use it as a ladder to see whether the answer meets the
                        descriptor for that level. The descriptor for the level indicates the different qualities that might be seen in
                        the student's answer for that level. If it meets the lowest level then go to the next one and decide if it
                        meets this level, and so on, until you have a match between the level descriptor and the answer. 
                        When assigning a level you should look at the overall quality of the answer and not look to pick holes in
                        small and specific parts of the answer where the student has not performed quite as well as the rest. If
                        the answer covers different aspects of different levels of the mark scheme you should use a best fit
                        approach for defining the level and then use the variability of the response to help decide the mark within
                        the level, for example if the response is predominantly level 3 with a small amount of level 4 material it would be
                        placed in level 3 but be awarded a mark near the top of the level because of the level 4 content.

                        Step 2 Determine a mark
                        Once you have assigned a level you need to decide on the mark. The descriptors on how to allocate
                        marks can help with this. Indicative content in the mark scheme is provided as a guide. It is not intended to be
                        exhaustive and you must credit other valid points. Students do not have to cover all of the points
                        mentioned in the Indicative content to reach the highest level of the mark scheme.
                        An answer which contains nothing of relevance to the question must be awarded no marks.

                    Based on all the instructions I've provided, please evaluate the user's answer based on the mark scheme and award them a mark out of {question.marks} with justifiable reasoning based on the mark scheme provided. If the mark you award doesn't match {question.marks}, provide constructive feedback that the student could use to improve their answer according to what they missed from the markscheme>
                    """

                    # Call the Hugging Face API (Mistral AI) for evaluation
                    api_key = os.getenv("HF_API_KEY")
                    headers = {"Authorization": f"Bearer {api_key}"}
                    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
                    response = requests.post(url, headers=headers, json={"inputs": prompt})

                    if response.status_code == 200:
                        response_data = response.json()
                        feedback_text = response_data[0].get("generated_text", "No response from the model.")
                        pattern = f"{re.escape("<")}.*?{re.escape(">")}"
                        feedback_text = re.sub(pattern,"",feedback_text)
                        

                    else:
                        feedback_text = f"Error: {response.status_code} - {response.text}"

                    print(feedback_text)
                    feedback.append({
                        'question': question,
                        'feedback': feedback_text
                    })

            # Clear the session after processing answers
            if 'selected_questions' in request.session:
                del request.session['selected_questions']

        return render(request, 'feedback.html', {'feedback': feedback})

    else:
        # Generate new questions if no "selected_questions" in session
        if not request.session.get('selected_questions'):
            questions = list(Question.objects.all())
            random.shuffle(questions)
            selected_questions = questions[:3]
            request.session['selected_questions'] = [question.id for question in selected_questions]
            request.session.modified = True

        selected_questions = Question.objects.filter(id__in=request.session.get('selected_questions', []))
        return render(request, 'random.html', {'questions': selected_questions})



# Get Hugging Face API token from the environment variables
# HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

# # Set up the URL for your Hugging Face model's API endpoint
# HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/your-model-name"

# def call_huggingface_model(data): #Sends a request to the Hugging Face API, passing data such as answers and receiving a response with analysis based on the model called
#     # Define headers including authorization using the Hugging Face token
#     headers = {
#         "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}", # Use our Hugging Face API token for authorization
#         "Content-Type": "application/json" #Indicates we're sending and expecting JSON data so the server understands the data format
#     } #Defines the HTTP headers needed to authenticate and send the data to the Hugging Face API. Without these headers:
# # - The API might reject the request with a 401 Unauthorized error due to missing or invalid authentication.
# # - The server might not correctly parse the data, resulting in errors or unexpected behavior (e.g., 415 Unsupported Media Type).


#     # Send a POST request to Hugging Face API with the input data (answers, etc.)
#     response = requests.post(HUGGINGFACE_API_URL, json=data, headers=headers)

#     if response.status_code == 200:
#         return response.json()  # Return the response data (e.g., predictions, analysis)
#     else:
#         return {"error": f"Request failed with status code {response.status_code}"}


# # Step 1: Prepare the data to send to Hugging Face
def mistral_test_view(request):
    if request.method == "POST":
        try:
            # Set up the Hugging Face API key (from environment variable or settings.py)
            api_key = os.getenv("HF_API_KEY")
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            # Example message to send to the model
            user_message = "What is the best French cheese?"

            # Send the request to the Hugging Face API for the Mistral model
            url = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
            response = requests.post(url, headers=headers, json={"inputs": user_message})

            # Check if the response is in JSON format
            if response.status_code == 200:
                try:
                    response_data = response.json()

                    # Check if the response is a list or a dictionary
                    if isinstance(response_data, list):
                        ai_message = response_data[0].get("generated_text", "No response from the model.")
                    else:
                        ai_message = response_data.get("generated_text", "No response from the model.")

                except ValueError as e:
                    ai_message = "Error parsing response data."
            else:
                ai_message = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            ai_message = "An error occurred while processing the request."

        return render(request, 'mistral_test.html', {'ai_message': ai_message, 'user_message': user_message})

    return render(request, 'mistral_test.html', {'ai_message': None, 'user_message': None})



# def prepare_data_for_huggingface(selected_questions, request):
#     # Collect the user's answers to the selected questions
#     messages = [
#         {
#             'role': 'user',  # Setting role as 'user'
#             'content': request.POST.get(f'answer_text_{question.Qnum}')
#         }
#         for question in selected_questions
#     ]
    
#     return {'messages': messages}

# # Step 2: Function to send data to Hugging Face API
# def send_to_huggingface(data):
#     # Hugging Face API URL for the model endpoint
#     model_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"  # Replace with the actual model URL

#     headers = {
#         "Authorization": f"Bearer {settings.HF_API_KEY}",  # Your token
#         "Content-Type": "application/json"
#     }

#     # Send POST request to Hugging Face API
#     response = requests.post(model_url, headers=headers, json=data)

#     # Check if the request was successful
#     if response.status_code == 200:
#         return response.json()  # Parse and return the result
#     else:
#         return {"error": f"Request failed with status {response.status_code}"}

# # Step 3: Main view for submitting answers and processing Hugging Face feedback
# def submit_answers(request):
#     if request.method == 'POST':
#         # Fetch selected questions from session
#         selected_questions_ids = request.session.get('selected_questions', [])
#         selected_questions = Question.objects.filter(id__in=selected_questions_ids)

#         # Store user answers in the Answer model
#         for question in selected_questions:
#             answer_text = request.POST.get(f'answer_text_{question.Qnum}')
#             if answer_text:
#                 Answer.objects.create(
#                     user=request.user,
#                     question=question,
#                     answer_text=answer_text,
#                 )

#         # Prepare the data to send to Hugging Face
#         data = prepare_data_for_huggingface(selected_questions, request)

#         # Send data to Hugging Face API and get feedback
#         result = send_to_huggingface(data)

#         # Process the response from Hugging Face (assuming it's JSON)
#         if 'error' not in result:
#             # Use the feedback from the model
#             for question, ai_result in zip(selected_questions, result['analysis']):
#                 # Assuming 'analysis' is the part of the result where feedback for each answer comes back
#                 answer = Answer.objects.get(user=request.user, question=question)
#                 answer.is_correct = ai_result['is_correct']
#                 answer.ai_feedback = ai_result['feedback']
#                 answer.save()

#             # Provide feedback to the user
#             correct_count = sum(1 for ai_result in result['analysis'] if ai_result['is_correct'])
#             total_count = len(result['analysis'])
#             feedback_message = f"You got {correct_count} out of {total_count} correct!"

#             return render(request, 'feedback.html', {
#                 'feedback_message': feedback_message,
#                 'analysis': result['analysis'],
#             })

#         # In case of an error, display it
#         return HttpResponse(f"Error: {result['error']}")

#     # If the request method is not POST, return a 405 Method Not Allowed
#     return HttpResponse("Invalid request method.")

import os
import requests
from django.shortcuts import render

def evaluate_answer_view(request):
    if request.method == "POST":
        try:
            # Example data (this would typically come from a form or user input)
            question = request.POST.get('question')  # Assuming the question is submitted along with the answer
            user_answer = request.POST.get('user_answer')  # Get the user's answer from the form
            mark_scheme = request.POST.get('mark_scheme')  # Get the mark scheme from the form

            # Prepare the AI prompt
            prompt = f"Question: {question}\nUser's Answer: {user_answer}\nMark Scheme: {mark_scheme}\nPlease evaluate the user's answer based on the mark scheme."

            # Set up the Hugging Face API key (from environment variable or settings.py)
            api_key = os.getenv("HF_API_KEY")
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            # Send the request to the Hugging Face API for the Mistral model
            url = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
            response = requests.post(url, headers=headers, json={"inputs": prompt})

            # Check if the response is in JSON format
            if response.status_code == 200:
                try:
                    response_data = response.json()

                    # Check if the response is a list or a dictionary
                    if isinstance(response_data, list):
                        feedback = response_data[0].get("generated_text", "No response from the model.")
                    else:
                        feedback = response_data.get("generated_text", "No response from the model.")

                except ValueError as e:
                    feedback = "Error parsing response data."
            else:
                feedback = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            feedback = "An error occurred while processing the request."

        # Pass the feedback and the user's input to the feedback template
        return render(request, 'feedback_template.html', {'feedback': feedback, 'question': question, 'user_answer': user_answer})

    # If it's not a POST request, return the form template for submitting the answer
    return render(request, 'submit_answer_template.html')
