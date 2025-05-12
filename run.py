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
    bot.select_flight_type(type="One-way")
    bot.select_flight_option(option="First-class")
    bot.select_direct_flight(direct_flight=True)
    bot.select_outbound_flight()
    bot.select_oneway_flight_date(checkin="2025-06-20")
    bot.select_flight_occupancy(adults=1, children=1, children_ages=[5])
    bot.select_search_button()

