from django.test import TestCase
from django.contrib.auth import get_user_model
from Database.models import Questions, Answers, UserAnswers, LoginAttempts, \
    UserRelationships, Practice, Results, SuddenDeath, \
    Games, UserScores, get_sentinel_user
from django.db import IntegrityError, transaction


class ModelTests(TestCase):
    """Tests to be performed on models"""

    def setUp(self):
        self.username = 'Somerandom'
        self.email = 'definitelynot@gmail.com'
        self.password = 'password123'

        self.sample_user = get_user_model().objects.create_user(
            username='Headshotzz',
            email='arealmail@gmail.com',
            password='password123',
        )

    """The following tests are performed on the custom user model"""

    def test_create_user(self):
        """Test that a user will be created when valid
        credentials are provided"""
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_create_user_without_email(self):
        """Test that a user won't be created without an email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=self.username,
                email=None,
                password=self.password
            )

    def test_create_user_without_username(self):
        """Test that a user won't be created without a username"""
        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username=None,
                    email=self.email,
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 1)

    def test_duplicate_email(self):
        """Test that a user won't be created with a duplicated email"""
        get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username='AnotherRandom',
                    email=self.email,
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 2)

    def test_duplicate_username(self):
        """Test that a user won't be created with a duplicated username"""
        get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        try:
            with transaction.atomic():
                get_user_model().objects.create_user(
                    username=self.username,
                    email='different@protonmail.com',
                    password=self.password
                )
        except IntegrityError:
            pass

        self.assertEqual(get_user_model().objects.count(), 2)

    def test_email_is_normalised(self):
        """Test that emails are normalised"""
        email = 'fakemail@PROTONMAIL.com'
        user = get_user_model().objects.create_user(
            username=self.username,
            email=email
        )

        self.assertEqual(user.email, email.lower())

    def test_create_superuser(self):
        """Test the creation of a superuser"""
        user = get_user_model().objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_delete_user(self):
        """Test that a users account can be deleted"""
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(get_user_model().objects.count(), 2)

        user.delete()

        self.assertEqual(get_user_model().objects.count(), 1)

    def test_delete_superuser(self):
        """Test that a superuser can be deleted"""
        superuser = get_user_model().objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.assertEqual(get_user_model().objects.count(), 2)

        superuser.delete()

        self.assertEqual(get_user_model().objects.count(), 1)

    def test_username_is_returned(self):
        """Test that a users username is returned as the objects
        string reprsentation instead of the email address"""
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.assertEqual(str(user), self.username)

    def test_question_and_answer_text_returned(self):
        """Test that a questions and answers text is returned as the
        objects string reprsentation"""
        new_question = Questions()
        new_question.category = 'food'
        new_question.difficulty = 'easy'
        new_question.question_type = 'multiple'
        new_question.text = 'What colour is an orange?'
        new_question.save()

        self.assertEqual(str(new_question), new_question.text)

        new_answer = Answers()
        new_answer.question = Questions.objects.get()
        new_answer.correct_answer = 'orange'
        new_answer.incorrect_answer = 'blue'
        new_answer.incorrect_answer2 = 'green'
        new_answer.incorrect_answer3 = 'pink'
        new_answer.save()

        self.assertEqual(str(Answers.objects.get()),
                         new_answer.correct_answer)

    def test_user_answers_returns_result(self):
        """Test that the user's answer model returns their result"""
        new_question = Questions()
        new_question.category = 'food'
        new_question.difficulty = 'easy'
        new_question.question_type = 'multiple'
        new_question.text = 'What colour is an orange?'
        new_question.save()

        new_user_answer = UserAnswers()
        new_user_answer.user = get_user_model().objects.get()
        new_user_answer.question = Questions.objects.get()
        new_user_answer.result = 'correct'
        new_user_answer.save()

        self.assertEqual(str(UserAnswers.objects.get()),
                         new_user_answer.result)

    def test_login_attempts_returns_status(self):
        """Test that the string reprsentation of a login attempts
        returns the login status"""
        new_login = LoginAttempts()
        new_login.user = get_user_model().objects.get()
        new_login.login_status = 'success'
        new_login.save()

        self.assertEqual(str(LoginAttempts.objects.get()),
                         new_login.login_status)

    def test_user_relationships_returns_status(self):
        """Test that the user relationship model returns the relationship
         status"""
        new_relationship = UserRelationships()
        new_relationship.user_first = get_user_model().objects.get()
        new_relationship.user_second = get_user_model().objects.get()
        new_relationship.relationship_status = 'friends'
        new_relationship.save()

        self.assertEqual(str(UserRelationships.objects.get()),
                         new_relationship.relationship_status)

    def test_practice_returns_score(self):
        """Test that the practice model returns the score"""
        new_practice = Practice()
        new_practice.user = get_user_model().objects.get()
        new_practice.score = 6
        new_practice.time_taken = 60
        new_practice.save()

        self.assertEqual(str(Practice.objects.get()), str(new_practice.score))

    def test_results_returns_winner(self):
        """Test that the results model returns the winner"""
        new_result = Results()
        new_result.winner = get_user_model().objects.get()
        new_result.second_place = get_user_model().objects.get()
        new_result.save()

        self.assertEqual(str(Results.objects.get()), str(new_result.winner))

    def test_sudden_death_returns_rounds(self):
        """Test that the sudden death model returns the number of rounds"""
        new_sudden_death = SuddenDeath()
        new_sudden_death.rounds = 333
        new_sudden_death.save()

        self.assertEqual(str(SuddenDeath.objects.get()),
                         str(new_sudden_death.rounds))

    def test_game_returns_winner(self):
        """test that the game model returns the winner"""
        new_result = Results()
        new_result.winner = get_user_model().objects.get()
        new_result.second_place = get_user_model().objects.get()
        new_result.save()

        new_game = Games()
        new_game.number_of_questions = 50
        new_game.number_of_players = 2
        new_game.category = 'history'
        new_game.created_by = get_user_model().objects.get()
        new_game.winner = Results.objects.get()
        new_game.save()

        self.assertEqual(str(Games.objects.get()), str(new_game.winner))

    def test_user_scores_returns_total_score(self):
        """Test that the user scores model returns the total score"""
        new_user_score = UserScores()
        new_user_score.user = get_user_model().objects.get()
        new_user_score.base_score = 5
        new_user_score.bonus_score = 10
        new_user_score.total_score = 15
        new_user_score.time_taken_seconds = 100
        new_user_score.save()

        self.assertEqual(str(UserScores.objects.get()),
                         format(new_user_score.total_score, '.3f'))

    def test_sentinel_user(self):
        """Test that when a user deletes their account their details
        are replaced with the sentinel user and the game record
        remains after the user has been deleted"""
        new_game = Games()
        new_game.number_of_questions = 50
        new_game.number_of_players = 2
        new_game.category = 'history'
        new_game.created_by = get_user_model().objects.get()
        new_game.save()

        self.assertEqual(Games.objects.get().created_by,
                         get_user_model().objects.get())

        user = get_user_model().objects.get()
        user.delete()

        self.assertEqual(Games.objects.get().created_by,
                         get_sentinel_user())
