from .base import Base

class IPAddress(Base):

    TABLE_ID = "tblJKiHOUidKr5kC8"

    def get_records(self):
        response = self.request.get_total(self.TABLE_ID, None, ['IP Address'])

        return response.json()
