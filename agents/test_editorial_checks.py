import unittest
from editorial_checks import content_warnings, recommend_links

class EditorialTests(unittest.TestCase):
    def test_recommend_only_relevant_pages(self):
        article={"title":"How to use ChatGPT to fact check information","target_keyword":"ChatGPT fact checking"}
        pages=[{"path":"/blog/chatgpt-fact-checking/","title":"ChatGPT Fact Checking Guide"},
               {"path":"/contact/","title":"Contact"}]
        self.assertEqual(recommend_links(article,pages)[0]["path"],"/blog/chatgpt-fact-checking/")
    def test_homepage_and_hypothetical_flag(self):
        article={"sections":[{"heading":"Practical Example","paragraphs":["Imagine a hypothetical claim."]}],
                 "sources":[{"url":"https://example.com"}]}
        notes=content_warnings(article)
        self.assertTrue(any("hypothetical" in n for n in notes))
        self.assertTrue(any("homepage" in n for n in notes))

if __name__=="__main__":
    unittest.main()
