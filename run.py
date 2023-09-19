from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    bot.close_dialog()
    bot.change_currency(currency='INR')
    bot.place_to_go(place='Vrindavan')
    bot.checkin_date(checkindate='2023-09-20', checkoutdate='2023-09-23')
    bot.occupancy_details(adults=3, children=2, rooms=1, children_age=[10, 11])
    bot.search()