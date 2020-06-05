from ATK.Story import Story
from ATK.StoryElement import StoryElement
from ATK.lib import Base
from ATK.lib.Enums import StepName, SlideType


class StoryDeveloper(Base.Base):

    def __init__(self):
        self.story = Story()
        self.slide_counter = 0

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def _get_StoryElement(self, text:str, is_cached:bool, type: SlideType, stay_on_slide:bool = False):
        element = StoryElement(
                transcript=text,
                slide=self.slide_counter,
                next_slide=self.slide_counter+1 if not stay_on_slide else self.slide_counter+0,
                type=type,
                is_cached=is_cached
            )
        self.slide_counter += 1 if not stay_on_slide else 0
        return element

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def start(self) -> None:
        text = f"Welcome to today's episode of trending twitter topics!"
        self.story.add_line(self._get_StoryElement(text=text, is_cached=True, type=SlideType.TITLE))

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def subtitle(self, topic:str) -> None:
        text = f'We will now cover the trending topic of {topic}.'
        self.story.add_line(self._get_StoryElement(text=text, is_cached=False, type=SlideType.SUBTITLE))

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def content(self, content:str):
        self.story.add_line(self._get_StoryElement(text=content, is_cached=False, type=SlideType.CONTENT))

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def end(self) -> None:
        text = f'This is it for today! We hope you have enjoyed todays episode. Please leave your comments in the comment section down below.'
        self.story.add_line(self._get_StoryElement(text=text, is_cached=True, type=SlideType.END))

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def develop(self, **kwargs) -> Story:
        twitter_content = list(filter(lambda x: x['step'] == f'{StepName.GET_TWEETS.value}_get_tweets' , kwargs['dependent_results']))[0]['results']
        self.start()
        for content in twitter_content:
            self.subtitle(topic=content['query'])
            for element in content['content']:
                text = f'User @{element.handle} posted: "{element.text}"'
                self.content(content=text)
        self.end()
        return self.story
