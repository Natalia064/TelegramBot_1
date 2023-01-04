from aiogram.dispatcher.filters.state import StatesGroup, State

class Start(StatesGroup):
    start_name= State()
    start_number= State()
    start_timetable = State()
    start_timetable_1 = State()
    
