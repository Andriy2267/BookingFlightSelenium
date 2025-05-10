from bookingFlight.booking_flight import BookingFlight

with BookingFlight(teardown=False) as bot:
    bot.land_first_page()
    # bot.bypass_captcha()
    bot.change_currency()
    bot.open_flight()
    bot.change_language()
    bot.select_flight_type()
    bot.select_flight_option(option="First-class")
    bot.select_direct_flight(direct_flight=False)

