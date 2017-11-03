from django.test import TestCase
from .models import UserProfile, Message, Topic, Topiccomment, Photo, PhotoComment
from .forms import CommentForm, photoForm
from django.utils import timezone
from django.core.urlresolvers import reverse
import json

# Create your tests here.
class UserProfileTest(TestCase):
    def create_userprofile(self, username="Alice", password="test0001", gender="male", email="Alice@test.com", remarks="", address=""):
        return UserProfile.objects.create(username=username, password=password, gender=gender, email=email, remarks=remarks, address=address)

    def test_userprofile_creation(self):
        w = self.create_userprofile()
        self.assertTrue(isinstance(w, UserProfile))
        self.assertEqual(w.__str__(), w.username)

class MessageTest(TestCase):
    def create_message(self, content='Hi', readflag='UNREAD'):
        author = UserProfileTest.create_userprofile(UserProfileTest, "Silk")
        receiver = UserProfileTest.create_userprofile(UserProfileTest, "Bob")
        return Message.objects.create(author=author, receiver=receiver, content=content, time=timezone.now(), readflag=readflag)

    def test_message_creation(self):
        w = self.create_message()
        s = 'from %s to %s at %s:%s %s/%s/%s' % (w.author, w.receiver, w.time.hour, w.time.minute, w.time.day, w.time.month,
                   w.time.year)
        self.assertTrue(isinstance(w, Message))
        self.assertEqual(w.__str__(), s)

class TopicTest(TestCase):
    def create_topic(self, author='', title='title', content='testing', views=12, remarks=2):
        if len(author) is 0:
            author = UserProfileTest.create_userprofile(UserProfileTest, "Icy")
        return Topic.objects.create(author=author, title=title, content=content, time=timezone.now(), views=views, remarks=remarks)

    def test_topic_creation(self):
        w = self.create_topic()
        pv = w.views
        w.increase_views()
        av = w.views
        pr = w.remarks
        w.increase_remarks()
        ar = w.remarks
        self.assertTrue(isinstance(w, Topic))
        self.assertEqual(w.__str__(), w.content)
        self.assertEqual(pv+1, av)
        self.assertEqual(pr+1, ar)

class TopiccommentTest(TestCase):
    def create_topiccomment(self, topic='', author='', content='comment'):
        if len(topic) is 0:
            topic = TopicTest.create_topic(TopicTest)
        if len(author) is 0:
            author = UserProfileTest.create_userprofile(UserProfileTest, "Ashy")
        return Topiccomment.objects.create(author=author, topic=topic, content=content, time=timezone.now())

    def test_topiccomment_creation(self):
        w = self.create_topiccomment()
        self.assertTrue(isinstance(w, Topiccomment))
        self.assertEqual(w.__str__(), w.content)

class PhotoTest(TestCase):
    def create_photo(self, image='images/album/1.jpeg', thumbs_up_number=1, category="1", photoname='test01'):
        photographer = UserProfileTest.create_userprofile(UserProfileTest, "Ash")
        return Photo.objects.create(photographer=photographer, image=image, thumbs_up_number=thumbs_up_number, category=category,
                                    time=timezone.now(), photo_name=photoname)

    def test_photo_creation(self):
        w = self.create_photo()
        s = '%s %s' % (w.photo_name, w.image)
        pt = w.thumbs_up_number
        w.increase_thumbs_up()
        at = w.thumbs_up_number
        self.assertTrue(isinstance(w, Photo))
        self.assertEqual(w.__str__(), w.photo_name)
        self.assertEqual(w.__unicode__(), s)
        self.assertEqual(pt+1, at)

class PhotoCommentTest(TestCase):
    def create_photocomment(self, content='test01'):
        author = UserProfileTest.create_userprofile(UserProfileTest, "Arch")
        photo = PhotoTest.create_photo(PhotoTest)
        return PhotoComment.objects.create(author=author, content=content, time=timezone.now(), photo=photo)

    def test_photo_creation(self):
        w = self.create_photocomment()
        s = '%s %s' % (w.photo, w.content)
        self.assertTrue(isinstance(w, PhotoComment))
        self.assertEqual(w.__str__(), w.content)
        self.assertEqual(w.__unicode__(), s)

class IndexViewTest(TestCase):
    def setUp(self):
        super(IndexViewTest, self).setUp()

    def test_index(self):
        response = self.client.get(reverse('index'))
        expected_url = reverse('album_scenery_new')
        expected_url = expected_url[:len(expected_url)-1]
        self.assertRedirects(response, expected_url=expected_url, status_code=302, target_status_code=301)

    def tearDown(self):
        super(IndexViewTest, self).tearDown()

class ForumViewTest(TestCase):
    def setUp(self):
        super(ForumViewTest, self).setUp()
        self.latest_topic = TopicTest.create_topic(TopicTest)

    def test_forum(self):
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('forum') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(ForumViewTest, self).tearDown()
        self.latest_topic.delete()

class HotTopicViewTest(TestCase):
    def setUp(self):
        super(HotTopicViewTest, self).setUp()
        self.latest_topic = TopicTest.create_topic(TopicTest)

    def test_hottopic(self):
        response = self.client.get(reverse('hot_topic'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('hot_topic') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(HotTopicViewTest, self).tearDown()
        self.latest_topic.delete()

class HotAlbumViewTest(TestCase):
    def setUp(self):
        super(HotAlbumViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('album_people_hot'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('album_people_hot') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(HotAlbumViewTest, self).tearDown()
        self.latest_topic.delete()

class NewPeopleViewTest(TestCase):
    def setUp(self):
        super(NewPeopleViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('album_people_new'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('album_people_new') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(NewPeopleViewTest, self).tearDown()
        self.latest_topic.delete()

class NewSceneryViewTest(TestCase):
    def setUp(self):
        super(NewSceneryViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('album_scenery_new'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('album_scenery_new') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(NewSceneryViewTest, self).tearDown()
        self.latest_topic.delete()


class HotSceneryViewTest(TestCase):
    def setUp(self):
        super(HotSceneryViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('album_scenery_hot'))
        self.assertEqual(response.status_code, 200)
        resp1 = self.client.get(reverse('album_scenery_hot') + '?page=5')
        self.assertEqual(resp1.status_code, 200)
        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(HotSceneryViewTest, self).tearDown()
        self.latest_topic.delete()

class DeletePhotoViewTest(TestCase):
    def setUp(self):
        super(DeletePhotoViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('delete_photo', args=(self.latest_topic.id,)))
        self.assertEqual(response.status_code, 200)

        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(DeletePhotoViewTest, self).tearDown()
        self.latest_topic.delete()

class DeletePhotoCommentViewTest(TestCase):
    def setUp(self):
        super(DeletePhotoCommentViewTest, self).setUp()
        self.latest_topic = PhotoCommentTest.create_photocomment(PhotoCommentTest)

    def test_hottopic(self):
        response = self.client.get(reverse('delete_comment', args=(self.latest_topic.id,)))
        self.assertEqual(response.status_code, 200)

        # self.assertContains(response, 'testing')

    def tearDown(self):
        super(DeletePhotoCommentViewTest, self).tearDown()
        self.latest_topic.delete()

class PhotoThumbsUpViewTest(TestCase):
    def setUp(self):
        super(PhotoThumbsUpViewTest, self).setUp()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_hottopic(self):
        response = self.client.get(reverse('thumbs_up', args=(self.latest_topic.id,)))
        expected_url = '/ShutterWeb/album/photo/' + str(self.latest_topic.id)
        self.assertRedirects(response, expected_url=expected_url, status_code=302, target_status_code=301)


    def tearDown(self):
        super(PhotoThumbsUpViewTest, self).tearDown()
        self.latest_topic.delete()

class TopicViewTest(TestCase):
    def setUp(self):
        super(TopicViewTest, self).setUp()
        self.latest_topic = TopicTest.create_topic(TopicTest)
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()
        self.valid_data = {'content': 'testing01', 'author': self.testuser1, 'topic': self.latest_topic,}

    def test_topic_redirect_if_not_logged_in(self):
        self.latest_topic.increase_views()
        response = self.client.get(reverse('topic', args=(self.latest_topic.id,)))
        s = '/ShutterWeb/login?next=/ShutterWeb/topic/' + str(self.latest_topic.id) + '/'
        self.assertEqual(response.url, s)

    def test_topic_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('topic', args=(self.latest_topic.id,)))
        self.assertEqual(response.status_code, 200)

    def test_topic_post(self):
        login = self.client.login(username='Alice', password='test0001')
        form = CommentForm(data=self.valid_data)
        url = reverse('topic', args=(self.latest_topic.id,))
        self.assertTrue(form.is_valid())
        # response = self.client.post(url, {'content': 'test01'})
        # print(response)
        # self.assertEqual(response.status_code, 200)

        # response = self.client.post(reverse('topic', args=(self.latest_topic.id,)))
        # print(response)
        # form = CommentForm(data=self.valid_data)
        # self.assertTrue(form.is_valid())
        # obj = form.save()
        # self.assertEqual(obj.content, self.valid_data['content'])

    def test_topic_not_exist(self):
        self.latest_topic.increase_views()
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('topic', args=(1000000,)))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        super(TopicViewTest, self).tearDown()
        self.latest_topic.delete()
        self.testuser1.delete()

class AddTopicViewTest(TestCase):
    def setUp(self):
        super(AddTopicViewTest, self).setUp()
        self.latest_topic = TopicTest.create_topic(TopicTest)
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()
        self.valid_data = {'content': 'testing01', 'author': self.testuser1, 'topic': self.latest_topic,}

    def test_add_topic_redirect_if_not_logged_in(self):
        self.latest_topic.increase_views()
        response = self.client.get(reverse('add_topic'))
        s = '/ShutterWeb/login?next=/ShutterWeb/add_topic/'
        self.assertEqual(response.url, s)

    def test_add_topic_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('add_topic'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(AddTopicViewTest, self).tearDown()
        self.latest_topic.delete()
        self.testuser1.delete()

class LogoutViewTest(TestCase):
    def setUp(self):
        super(LogoutViewTest, self).setUp()

    def test_index(self):
        response = self.client.get(reverse('logout'))
        expected_url = reverse('index')
        expected_url = expected_url[:len(expected_url)-1]
        self.assertRedirects(response, expected_url=expected_url, status_code=302, target_status_code=301)

    def tearDown(self):
        super(LogoutViewTest, self).tearDown()

class UserinfoViewTest(TestCase):
    def setUp(self):
        super(UserinfoViewTest, self).setUp()

    def test_index(self):
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(UserinfoViewTest, self).tearDown()

class LoginViewTest(TestCase):
    def setUp(self):
        super(LoginViewTest, self).setUp()

    def test_index(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(LoginViewTest, self).tearDown()

class RegisterViewTest(TestCase):
    def setUp(self):
        super(RegisterViewTest, self).setUp()

    def test_index(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(RegisterViewTest, self).tearDown()

class editprofileViewTest(TestCase):
    def setUp(self):
        super(editprofileViewTest, self).setUp()
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()

    def test_index_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(editprofileViewTest, self).tearDown()
        self.testuser1.delete()

class InboxViewTest(TestCase):
    def setUp(self):
        super(InboxViewTest, self).setUp()
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()

    def test_index_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(InboxViewTest, self).tearDown()
        self.testuser1.delete()

class MessageDetailViewTest(TestCase):
    def setUp(self):
        super(MessageDetailViewTest, self).setUp()
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()
        self.latest_message = MessageTest.create_message(MessageTest)

    def test_index_not_your_message(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('message_detail', args=(self.latest_message.id,)))
        self.assertEqual(response.status_code, 404)

    def test_index_not_exist(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('message_detail', args=(1000,)))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        super(MessageDetailViewTest, self).tearDown()
        self.testuser1.delete()
        self.latest_message.delete()

class AlbumPhotoViewTest(TestCase):
    def setUp(self):
        super(AlbumPhotoViewTest, self).setUp()
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_index_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        response = self.client.get(reverse('album_photo', args=(self.latest_topic.id,)))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(AlbumPhotoViewTest, self).tearDown()
        self.testuser1.delete()
        self.latest_topic.delete()

class UploadPhotoViewTest(TestCase):
    def setUp(self):
        super(UploadPhotoViewTest, self).setUp()
        self.testuser1 = UserProfileTest.create_userprofile(UserProfileTest, 'Alice', 'test0001')
        self.testuser1.set_password('test0001')
        self.testuser1.save()
        self.latest_topic = PhotoTest.create_photo(PhotoTest)

    def test_index_logged_in(self):
        login = self.client.login(username='Alice', password='test0001')
        form = photoForm(data={'category': '', 'photo_name': '', 'photographer_name': '', 'photographer_remark': '', 'image': ''})
        self.assertTrue(form.is_valid())
        response = self.client.get(reverse('album_upload_image'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        super(UploadPhotoViewTest, self).tearDown()
        self.testuser1.delete()
        self.latest_topic.delete()
