import logging

from app import db
from app.db.models import User, Song


def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('bx5@njit.edu', '123456')
        #add it to get ready to be committed
        db.session.add(user)
        #finding one user record by email
        user = User.query.filter_by(email='bx5@njit.edu').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'bx5@njit.edu'
        #this is how you get a related record ready for insert
        user.songs= [Song("test","smap","2020","testGenre"),Song("test2","te","2021","testGenre")]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        #checking cascade delete
        db.session.delete(song1)
        db.session.delete(song2)

        db.session.delete(user)
        db.session.commit()
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0

