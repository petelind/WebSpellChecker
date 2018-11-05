import os

from django.conf import settings
from django.db import models
from django.forms import FileField
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from SpellChecker.forms import DocumentForm
from SpellChecker.models import Document
from copy import copy
from shutil import copyfile
import random
from curses.ascii import isupper
from re import findall, match, search  # we will use regexp to parse words out of book fed to us
from collections import Counter  # this class implements what we need - dict with the words & frequencies
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('welcome')
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def welcome(request):
    return render(request, 'welcome.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        user_docs = Document.objects.get_documents_for(request.user)
        return render(request, 'files.html',
                      {'documents': user_docs})
    else:
        return redirect('welcome')


@login_required
def model_form_upload(request):
    if request.method == 'POST':
        document = Document(user=request.user)
        form = DocumentForm(instance=document, data=request.POST, files=request.FILES)
        if form.is_valid():
            process_file(request, form)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form,
    })


def process_file(request, submission: DocumentForm):
    if request.user:
        target = submission.save()
        spell_check(request, target.document)
    else:
        raise HttpResponseForbidden

@login_required
def download(request, path):
    try:
        original_document = Document.objects.get(document=path)
        all_user_docs = Document.objects.get_documents_for(request.user)
    except Document.DoesNotExist:
        raise Http404
    if original_document not in all_user_docs:
        raise HttpResponseForbidden()
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file_to_serve:
            response = HttpResponse(file_to_serve.read(), content_type='plain/txt')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def spell_check(request, path_to_file):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    vocabulary = Counter()
    path_to_vocabulary = 'documents/big.txt'

    def build_vocabulary(file_name):
        """
        Returns Counter of lower case words from the file contents.
        :param file_name: file to be parsed
        :return: Counter with word from file
        """
        try:
            file_content = open(file_name)
            with file_content:
                text = file_content.read()
                normalized_text = text.lower()
                all_words = findall(r'\w+', normalized_text)  # as per https://docs.python.org/3.6/howto/regex.html
                ok_words = []

                for word in all_words:
                    word.strip("_")

                    if not search('[0-9]', word):
                        ok_words.append(word)

                counter = Counter(ok_words)
                return counter
        except IOError:
            print("[ ERROR ] Cannot read from " + file_name)

    def propose_correction(for_this_word):
        """
        Most probable spelling for the word
        :param for_this_word: word you are checking
        :return: word (if its right already) or a correction proposition as string
        """
        candidates = identify_candidates(for_this_word)
        probabilities = {}
        for candidate in candidates:
            p = P(candidate)
            probabilities[p] = candidate
        most_probable_word_key = max(probabilities.keys())
        most_probable_word = probabilities[most_probable_word_key]
        return most_probable_word

    def identify_candidates(word):
        """
        We either know this word from file, or its on 1-2 edit distance from known, or we dont know it
        and thus leave as it is
        :param word:
        :return: candidate word(s) as set
        """

        # Do we know this word?
        result = known([word])
        if result:
            return result

        # May be its 1-edit from one of the words we know?..
        result = known(edits1(word))
        if result:
            return result

        # May be its 2-edit from one of the words we know?..
        result = known(edits2(word))
        if result:
            return result

        # Ok, we have no idea what to do, ship it back
        return set(word)

    def P(of_word):
        """
        Returns probability of the particular word in the text
        :param for_this_word word you are looking for
        :return: probablity as float
        """
        N = sum(vocabulary.values())
        p = vocabulary[of_word] / N
        return p

    def known(words):
        """
        Will returns word(s) which are in dictionary.
        :param words: words to check against dictionary
        :return: know word(s) as iterable set
        """

        known_words = set()
        for word in words:
            if word in vocabulary:
                known_words.add(word)

        return known_words
        # return set(w for w in words if w in vocabulary)

    """
    Next three functions are courtesy of Datta Sainath Dwarampudi, from:
    https://newclasses.nyu.edu/access/content/group/92f54196-4c8e-4057-b493-c1e043cb4334/Labs/Lab%205%20Spell%20Checker.ipynb
    """

    def produce_splits(word):
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    def edits1(word):
        pairs = produce_splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        """
        Recursive call of edits1 to produce edits who are 2 edits away.
        """
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    def store_register(word):
        """
        For a given word returns a list of 0 and 1 where 1 represents capital letter, and 0 is lowercase
        :param word: word to process into 0 and 1
        :return: list of 0 and 1 with the length of the word
        """
        index = []
        char_array = list(word)
        for each_char in char_array:
            if isupper(each_char):
                index.append(True)
            else:
                index.append(False)
        return index

    def restore_register(word, index):
        """
        Restores register according to the given index
        :param word: all-lowercase word to restore cases from propose_correction()
        :param index: list of True/False for each of letter in word
        :return: word with cases restored
        """
        if (len(word)) > len(index):
            zeros_to_add = len(word) - len(index)
            for i in range(0, zeros_to_add):
                index.append(0)

        if (len(index)) > len(word):
            index = index[0:len(word)]

        char_array = list(word)
        restored_word = ''
        for i in range(0, len(index)):
            if index[i]:
                restored_word += char_array[i].upper()
            else:
                restored_word += char_array[i]
        return restored_word

    # Lets create temp file, its a source for parsing...
    temp_file = copyfile(path_to_file.name, path_to_file.name + str(random.randint(0, 1000000)))
    source_file = open(temp_file, 'r')
    destination_file = open(path_to_file.name, 'w')

    # Here we build frequency / probability table we use for spell checking
    # TODO: Prebuild and store Vocabulary as JSON/Model
    # TODO: Update vocabulary as the user submits texts
    vocabulary = build_vocabulary(path_to_vocabulary)

    corrected_lines = []
    for line in source_file.readlines():
        corrected_line = copy(line)
        for word in findall(r'\w+', line):
            uppercase_index = store_register(word)
            corrected_word = propose_correction(word)
            corrected_line = corrected_line.replace(word, restore_register(corrected_word, uppercase_index))
        corrected_lines.append(corrected_line)

    # ok, now lets flush the list we created into the file & cleanup...
    destination_file.writelines(corrected_lines)
    os.remove(temp_file)
    return
