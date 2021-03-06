import gspread
import httplib2
import oauth2client.service_account
import pluginconf


class GSpreadsheet:
    SCOPE = ['https://docs.google.com/feeds',
             'https://spreadsheets.google.com/feeds']

    def __init__(self):
        self.credentials = None
        self.gc = None

    def open(self, name):
        if not self.credentials:
            creds_json = pluginconf.get_path("google")
            self.credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(creds_json, self.SCOPE)
            self.gc = gspread.authorize(self.credentials)

        if self.credentials.access_token_expired:
            self.credentials.refresh(httplib2.Http())
            self.gc = gspread.authorize(self.credentials)
        return self.gc.open(name)

    def open_sheet1(self, name):
        ws = self.open(name)
        if ws:
            return ws.sheet1
