from .base import Base

class FQDN(Base):

    TABLE_ID = "tblK0murYomondNdt"

    BCY_SERIE_A_VIEW_ID = "viwSKcHeEHqLG4ZU0"

    def get_record(self, record_id):
        response = self.request.get_record(self.TABLE_ID, record_id)

        return response.json()

    def get_total(self):
        response = self.request.get_total(self.TABLE_ID, self.BCY_SERIE_A_VIEW_ID, ['Fully Qualified Domain Name'])

        return response.json()
