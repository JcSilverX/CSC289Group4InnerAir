import json
from datetime import datetime, timedelta
from random import uniform, randint

from sqlalchemy import text

from inner_air import app, db
from inner_air.models import DBVersion, Exercise, User, Statistics


def DeleteAndCreateDB():
    with app.app_context():
        try:
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()
        except:
            print("Database is not found - generating database with starter generic data. DB Version is now 0.05")
            thisVersion = None

        if thisVersion is None:
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"],
                                            exercise_inhale=i["exercise_inhale"],
                                            exercise_inhale_pause=i["exercise_inhale_pause"],
                                            exercise_exhale=i["exercise_exhale"],
                                            exercise_exhale_pause=i["exercise_exhale_pause"]))

                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days'],
                                        is_confirmed=1)
                                   )
                for i in range(365):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=1, exercise_id=1))
                    db.session.commit()
                for i in range(45):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=2, exercise_id=1))
                    db.session.commit()
                for i in range(7):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=3, exercise_id=3))

                db.session.add(Exercise(exercise_name="Control Pause",
                                        exercise_instructions="Sit up with a straight back.  Pinch both nostrils closed with your thumb and forefinger.  Exhale slowly out of your mouth to a natural conclusion.  Press the Start button to begin. When you feel the first potent desire to breath, press stop and take a soft inhale.",
                                        exercise_description="It is important that the first breath in after the Control Pause is controlled and relaxed.  Do not wait so long that you begin to gasp for air, or have generally labored breathing.  Please wait a few minutes and try again.  You should only do this when you are calm and relaxed.  Do not do this after strenuous activities.  Like ANY breath restriction techniques, never attempt while driving, underwater, or in any condition that you could become injured.",
                                        exercise_length="1", category_id="1",
                                        exercise_inhale="1",
                                        exercise_inhale_pause="1",
                                        exercise_exhale="1",
                                        exercise_exhale_pause="1"))
                db.session.add(Exercise(exercise_name="Mini Breath Holds",
                                        exercise_instructions="Exhale gently and hold the breath for half of your Control Pause.  IE: if your Control Pause is 50 seconds, your goal is 25 seconds. You can repeat as often as you want throughout the day.  Try for 100 repetitions.",
                                        exercise_description="A key component to Buteyko breathing is to practice breathing less throughout the day.  This technique trains the body to do just this. Many Buteyko practitioners, medical researchers, and other swear by this to stave off asthma and anxiety attacks.  You can try to do this every 15 minutes through the day if you want to practice.",
                                        exercise_length="1", category_id="1",
                                        exercise_inhale="1",
                                        exercise_inhale_pause="1",
                                        exercise_exhale="1",
                                        exercise_exhale_pause="1"))

            db.session.add(Exercise(exercise_name="Demo Exercise",
                                    exercise_instructions="Test Demo Instructions",
                                    exercise_description="Test Demo Descriptions",
                                    exercise_length="1", category_id="1",
                                    exercise_inhale="2",
                                    exercise_inhale_pause="2",
                                    exercise_exhale="2",
                                    exercise_exhale_pause="2"))

            db.session.add(User(firstname='DemoFirstName',
                                email='demo@demo.com',
                                password_hash="$2b$12$nEfHRbAwWBJYrk05CvH/x.WEa1DK.mWjmM0HU6LDIIYr9V4ra6l4S",
                                consecutive_days=45,
                                is_confirmed=1))
            db.session.commit()
            demoUser = db.session.query(User).filter(User.email == 'demo@demo.com').first()
            j = 90.20
            k = 120.34
            for i in range(45):
                x = datetime.today() - timedelta(days=i)
                db.session.add(
                    Statistics(date_completed=x, user_id=demoUser.id, exercise_id=11, hold_length=uniform(j, k)))
                db.session.commit()
                j -= uniform(1, 3)
                k -= uniform(1, 5)

            db.session.commit()
            demoUser = db.session.query(User).filter(User.email == 'demo@demo.com').first()
            for i in range(45):
                x = datetime.today() - timedelta(days=i)
                for zz in range(5):
                    if randint(0, 1) % 2 == 0:
                        db.session.add(
                            Statistics(date_completed=x, user_id=demoUser.id, exercise_id=1))
                db.session.commit()

            db.session.commit()

            db.session.query(Exercise).filter(Exercise.exercise_name == 'Square Breathing').first().update_breath_data(
                4, 4, 4, 4, 6)
            db.session.query(Exercise).filter(
                Exercise.exercise_name == 'Square Breathing v2').first().update_breath_data(
                4, 4, 6, 2, 6)
            db.session.query(Exercise).filter(Exercise.exercise_name == 'Nadi Shodhana').first().update_breath_data(
                4, 4, 4, 4, 10)
            db.session.query(Exercise).filter(
                Exercise.exercise_name == 'Resonant (Coherent) Breathing').first().update_breath_data(6, 0, 6, 0, 10)
            db.session.query(Exercise).filter(Exercise.exercise_name == 'Buteyko Breathing').first().update_breath_data(
                4, 4, 4, 4, 2)
            db.session.query(Exercise).filter(
                Exercise.exercise_name == 'Breathing Coordination').first().update_breath_data(10, 0, 10, 0, 20)
            # db.session.query(Exercise).filter(
            #     Exercise.exercise_name == 'Decongest The Nose').first().update_breath_data(
            #     1, 1, 1, 1)
            db.session.query(Exercise).filter(Exercise.exercise_name == '4-7-8 Breathing').first().update_breath_data(
                4, 7, 8, 0, 4)
            db.session.query(Exercise).filter(
                Exercise.exercise_name == 'Yogic Breathing Phase 1').first().update_breath_data(
                4, 4, 4, 4, 12)
            db.session.query(Exercise).filter(
                Exercise.exercise_name == 'Yogic breathing Phase 2').first().update_breath_data(
                4, 4, 4, 4, 12)
            db.session.commit()


DeleteAndCreateDB()
