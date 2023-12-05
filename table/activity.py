from .base import Base

class Activity(Base):

    TABLE_ID = "tblTGVXeqPecdKpTm"

    VARIATIONS_VIEW_ID = "viwxuGJT9KRlUISFa"

    def get_variations(self) -> dict:
        """
        Method used to retrieve variations from the view.

        :return: list of variation records.
        """

        response = self.request.get_activity(self.TABLE_ID, self.VARIATIONS_VIEW_ID)

        return response.json()
