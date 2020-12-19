class Review:
    def __init__(self, stars, text, reviewer_id, reviewee_id):
        self.__stars = stars
        self.__text = text
        self.__reviewer_id = reviewer_id
        self.__reviewee_id = reviewee_id

    def return_obj(self):
        return {
            "stars": self.__stars,
            "text": self.__text,
            "reviewer": self.__reviewer_id,
            "reviewee": self.__reviewee_id,
        }