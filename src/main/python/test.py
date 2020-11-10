from homoeopathy_app import App
from homoeopathy_app.new_case import Case

app = App()
# app.run()

test = Case()
# test.casedb.reset_all()
test.create_case(1)
