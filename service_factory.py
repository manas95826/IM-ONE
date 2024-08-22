from services import TavilySearchService, GroqSearchService, ECommerceSearchService, TravelSearchService, CalendarInviteService

class ServiceFactory:
    def create_service(self, service_type):
        if service_type == "web_information_retrieval":
            return TavilySearchService()
        elif service_type == "information_retrieval":
            return GroqSearchService()
        elif service_type == "e_commerce_search":
            return ECommerceSearchService()
        elif service_type == "travel_and_navigation":
            return TravelSearchService()
        elif service_type == "send_calendar_invite":
            return CalendarInviteService()
        else:
            raise ValueError(f"Unknown service type: {service_type}")
