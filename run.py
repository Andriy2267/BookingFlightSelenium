from bookingFlight.booking_flight import BookingFlight

with BookingFlight(teardown=False) as bot:
    bot.land_first_page()
    # bot.bypass_captcha()
    bot.close_optional_popup()
    bot.change_currency()
    bot.close_optional_popup()
    bot.open_flight()
    bot.close_optional_popup()
    bot.change_language()
    bot.close_optional_popup()
    bot.select_flight_type()
    bot.select_flight_option(option="First-class")
    bot.select_direct_flight(direct_flight=True)
    bot.select_outbound_flight()

