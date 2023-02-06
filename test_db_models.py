import pytest
import json
from models import User, Exercise, Routine, Favorites, Statistics, Category, UserRating, db
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@pytest.fixture(scope="module")
def db_session():
    test_user = User(firstname="testUser", email="testUser@example.com", password="changeme")
    test_exercise = Exercise(exercise_name='test_exercise_name',
                             exercise_instructions='test_exercise_instructions',
                             exercise_description='test_exercise_descriptions',
                             exercise_length=12, category_id=1)
    test_user2 = User(firstname="testUser2", email="testUser2@example.com", password="changemetoo")
    test_exercise2 = Exercise(exercise_name='test_exercise_name2',
                              exercise_instructions='test_exercise_instructions2',
                              exercise_description='test_exercise_descriptions2',
                              exercise_length=12, category_id=1)
    with app.app_context():
        db.session.add(test_user)
        db.session.add(test_exercise)
        db.session.add(test_user2)
        db.session.add(test_exercise2)
        db.session.commit()
        yield db.session
        db.session.remove()


@pytest.fixture()
def current_user(db_session):
    currentUser = db.session.query(User).filter_by(email='testUser@example.com').one()
    return currentUser


@pytest.fixture()
def current_exercise(db_session):
    currentExercise = db.session.query(Exercise).filter_by(exercise_name='test_exercise_name').one()
    return currentExercise


def test_multiple_users(db_session):
    counter = 0
    user_table = db.session.query(User).all()
    for user in user_table:
        counter += 1
        print('\n')
        print(user.as_dict())
    assert counter == 2


def test_multiple_exercises(db_session):
    counter = 0
    exercise_table = db.session.query(Exercise).all()
    for exercise in exercise_table:
        counter += 1
        print('\n')
        print(exercise.as_dict())
    assert counter == 2


def test_user_model(db_session):
    test_user = db.session.query(User).filter_by(firstname='testUser').one()
    assert test_user.firstname == "testUser"
    assert test_user.email == "testUser@example.com"
    assert test_user.password == "changeme"
    print(f"\n Dictionary of User Object: {test_user.as_dict()} \n")


def test_user_fixture(current_user):
    assert current_user.firstname == "testUser"
    assert current_user.email == "testUser@example.com"
    assert current_user.password == "changeme"


def test_exercise_model(db_session):
    test_exercise = db_session.query(Exercise).filter_by(exercise_name='test_exercise_name').one()
    assert test_exercise.exercise_name == 'test_exercise_name'
    assert test_exercise.exercise_instructions == 'test_exercise_instructions'
    assert test_exercise.exercise_description == 'test_exercise_descriptions'
    assert test_exercise.exercise_length == 12
    # assert test_exercise.cumulative_rating == 100 todo test later
    print(f"\n Dictionary of exercise Object: {test_exercise.as_dict()} \n")


def test_exercise_fixture(current_exercise):
    assert current_exercise.exercise_name == 'test_exercise_name'
    assert current_exercise.exercise_instructions == 'test_exercise_instructions'
    assert current_exercise.exercise_description == 'test_exercise_descriptions'
    assert current_exercise.exercise_length == 12


def test_routine_model(db_session):
    test_routine_add = Routine(user_id=db.session.query(User).first().userID,
                               exercise_id=db.session.query(Exercise).first().exerciseID)
    db.session.add(test_routine_add)
    db.session.commit()
    test_routine = db.session.query(Routine).first()
    assert test_routine.user_id == db.session.query(User).first().userID
    assert test_routine.exercise_id == db.session.query(Exercise).first().exerciseID
    print(f"\n Dictionary of Routine Object: {test_routine.as_dict()} \n")


def test_favorites_model(db_session):
    test_favorites_add = Favorites(user_id=db.session.query(User).first().userID,
                                   exercise_id=db.session.query(Exercise).first().exerciseID)
    db.session.add(test_favorites_add)
    db.session.commit()
    assert test_favorites_add.user_id == db.session.query(User).first().userID
    assert test_favorites_add.exercise_id == db.session.query(Exercise).first().exerciseID
    print(f"\n Dictionary of Favorites Object: {test_favorites_add.as_dict()} \n")


def test_statistics_model_new(db_session, current_user, current_exercise):
    # On exercise complete
    if db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                              exercise_id=current_exercise.exerciseID).first() is None:
        test_add_statistics = Statistics(exercises_completed=1, exercise_id=current_exercise.exerciseID,
                                         user_id=current_user.userID)
        db.session.add(test_add_statistics)
        db.session.commit()

    # for actual code we need an else, but for this test it isn't needed as I am doing a new test here
    else:
        update_stats = db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                                              exercise_id=current_exercise.exerciseID).first()
        update_stats.exercises_completed += 1
        db.session.commit()
    assert db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                                  exercise_id=current_exercise.exerciseID).first().exercises_completed == 1
    print("\n Dictionary of Statistics Table:\n")
    statsTable = db_session.query(Statistics).all()
    for stat in statsTable:
        print(stat.as_dict())


def test_statistics_model_update(db_session, current_user, current_exercise):
    # On exercise complete
    if db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                              exercise_id=current_exercise.exerciseID).first() is None:
        test_add_statistics = Statistics(exercises_completed=1, exercise_id=current_exercise.exerciseID,
                                         user_id=current_user.userID)
        db.session.add(test_add_statistics)
        db.session.commit()

    # for actual code we need an else, but for this test it isn't needed as I am doing a new test here
    else:
        update_stats = db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                                              exercise_id=current_exercise.exerciseID).first()
        update_stats.exercises_completed += 1
        db.session.commit()
    assert db_session.query(Statistics).filter_by(user_id=current_user.userID,
                                                  exercise_id=current_exercise.exerciseID).first().exercises_completed == 2
    print("\n Dictionary of Statistics Table:\n")
    statsTable = db_session.query(Statistics).all()
    for stat in statsTable:
        print(stat.as_dict())


def test_category_model(db_session, current_user, current_exercise):
    test_category_add1 = Category(category_name='Inside Activity')
    test_category_add2 = Category(category_name='Outside Activity')
    db.session.add(test_category_add1)
    db.session.add(test_category_add2)
    db.session.commit()
    category_table = db.session.query(Category).all()
    for thing in category_table:
        print(thing.as_dict())
    pass


def test_userRating_model_new(db_session, current_user, current_exercise):
    # Check if rating exists
    if db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                              exercise_id=current_exercise.exerciseID).first() is None:
        print("Does not exist, creating new")
        db.session.add(
            UserRating(user_rating=100, user_id=current_user.userID, exercise_id=current_exercise.exerciseID))
        db.session.commit()
    else:
        rating_to_update = db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                                  exercise_id=current_exercise.exerciseID).first()
        rating_to_update.user_rating = 90
        print('\n')
    print(db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                 exercise_id=current_exercise.exerciseID).first().as_dict())
    assert db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                  exercise_id=current_exercise.exerciseID).first().user_rating == 100


def test_userRating_model_update(db_session, current_user, current_exercise):
    # Check if rating exists
    if db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                              exercise_id=current_exercise.exerciseID).first() is None:
        print("Does not exist, creating new")
        db.session.add(
            UserRating(user_rating=100, user_id=current_user.userID, exercise_id=current_exercise.exerciseID))
        db.session.commit()
    else:
        rating_to_update = db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                                  exercise_id=current_exercise.exerciseID).first()
        rating_to_update.user_rating = 90
    print('\n')
    print(db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                 exercise_id=current_exercise.exerciseID).first().as_dict())
    assert db_session.query(UserRating).filter_by(user_id=current_user.userID,
                                                  exercise_id=current_exercise.exerciseID).first().user_rating == 90
