from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        #1.1 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        #1.2 정상적으로 페이지 로드가 된다
        self.assertEqual(response.status_code, 200)
        #1.3 페이지 타이틀
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        #1.4 네비게이션 바
        navbar = soup.nav
        #1.5 Blog, About Me 라는 문구가 네비게이션바에 있는가?
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)


        #2.1 포스트(게시물)가 하나도 없다면
        self.assertEqual(Post.objects.count(),0)
        #2.2 main-area '아직 게시물이 없습니다'라는 문구 출력
        main_area = soup.find('div', id='main-area')

        #3.1 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title = '첫 번째 포스트 입니다',
            content = "Hello World, First Post!"
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다',
        content = "Hello World, Second Post!"
        )
        self.assertEqual(Post.objects.count(),2)
        #3.2 포스트 목록 페이지를 새로고침하면
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        #3.3 main-area에 포스트 2개의 제목이 존재하면
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        #3.4 '아직 게시물이 없습니다'라는 문구는 더이상 출력 안함
        self.assertNotIn("아직 게시물이 없습니다.", main_area.text)

    def test_post_detail(self):
        #1.1 Post가 하나 있다
        post_001 = Post.objects.create(
            title = '첫번쨰 포스트 입니다',
            content = "Hello world. First Post"
        )
        #1.2 그 포스트의 url은 'blog/1/'이다
        self.assertEqual(post_001.get_absolute_url(),'/blog/1/')

        #2 첫벚째 포스트의 상세 페이지 테스트
        #2.1 첫번째 post url로 접근하면 정상 작동된다
        response = self.client.get(post_001.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        #2.2 포스트 목록 페이지와 똑같은 네비게이션 바가 있다
        navbar = soup.nav
        self.assertIn('Blog',navbar.text)
        self.assertIn('About me',navbar.text)
        #2.3 첫번쩨 포스트의 제목이 웹 브라우저 탭 타이틀에 있다
        self.assertIn(post_001.title, soup.title.text)
        #2.4 첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id="post-area")
        self.assertIn(post_001.title,post_area.text)