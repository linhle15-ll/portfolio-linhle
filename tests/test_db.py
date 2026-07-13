import unittest
import os
os.environ["TESTING"] = "true"

from app import TimelinePost


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        TimelinePost.delete().execute()

    def tearDown(self):
        TimelinePost.delete().execute()

    def test_timeline_post(self):
        TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I'm John!",
        )

        # TODO: retrieve the timeline post we just created and check its fields
        posts = list(TimelinePost.select())
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[0].content, "Hello world, I'm John!")


if __name__ == "__main__":
    unittest.main()
