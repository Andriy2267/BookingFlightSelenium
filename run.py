from bookingFlight.booking_flight import BookingFlight

with BookingFlight(teardown=False) as bot:
    bot.land_first_page()
    bot.close_optional_popup()
    bot.change_currency()
    bot.close_optional_popup()
    bot.open_flight()
    bot.close_optional_popup()
    bot.change_language()
    bot.close_optional_popup()
    ## One-way, Round-trip, Multi-city
    bot.select_flight_type(type="One-way")
    ## Economy, Premium economy, Business, First
    bot.select_flight_option(option="Business")
    bot.select_direct_flight(direct_flight=True)
    bot.select_outbound_flight()
    bot.select_oneway_flight_date(checkin="2025-06-20")
    bot.select_flight_occupancy(adults=1, children=1, children_ages=[5])
    bot.select_search_button()
    bot.select_BCF_flight()
    bot.report_results()


