from aiogram.fsm.state import StatesGroup, State



class ServiceState(StatesGroup):

	region = State()
	sname = State()
	applicant = State()
	fedback = State()


class AddService(StatesGroup):

	text = State()


class OfferState(StatesGroup):

	text = State()



class RegisterState(StatesGroup):


	region = State()
	service = State()
	first_name = State()
	last_name = State()
	year_experence = State()
	skills = State()
	schedule = State()
	price = State()
	phone_number = State()

	
