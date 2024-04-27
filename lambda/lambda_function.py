
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Voicery. How can I assist you today?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "How can I assist you?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FoodInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("FoodInfoIntent")(handler_input)
        
    def handle(self, handler_input):
        speak_output = "Hello, we offer bananas, apples, nuts, pizza and chicken"
        
        return (
            handler_input.response_builder.speak(speak_output).response
            )
    

class OrderFoodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "OrderFoodIntent"
        return ask_utils.is_intent_name("OrderFoodIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        food_type = slots["foodtype"].value  # Get the food type from the slot
        
        # Parse the quantity from the slot
        quantity = int(slots["quantity"].value) if "quantity" in slots and slots["quantity"].value else 1  

        # Define the list of available food items
        available_food_items = ["bananas", "apples", "nuts", "pizza", "chicken", "orange", "grapes", "strawberries", "blueberries", "tomatoes", "cucumbers", "carrots", "potatoes", "broccoli", "spinach", "kale", "avocados", "peaches", "pears", "pineapples", "watermelons", "mangoes", "papayas", "cherries", "kiwis"]

        # Check if the requested food type is in the list of available food items
        if food_type.lower() not in available_food_items:
            # If the requested food type is not available, inform the user
            speak_output = f"Sorry, we currently don't offer {food_type}."
        else:
            # Retrieve the user's cart from session attributes
            session_attr = handler_input.attributes_manager.session_attributes
            user_cart = session_attr.get('cart', [])

            # Add the item to the cart
            user_cart.extend([food_type] * quantity)

            # Update session attributes with the modified cart
            session_attr['cart'] = user_cart

            # Build the response message indicating the order
            speak_output = f"Okay, I'll add {quantity} {food_type}{'s' if quantity > 1 else ''} to your cart."

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response




    
#add CartManagementIntentHandler  
class CartManagementIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "CartManagementIntent"
        return ask_utils.is_intent_name("CartManagementIntent")(handler_input)

    def handle(self, handler_input):
        # Retrieve the user's cart from session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        user_cart = session_attr.get('cart', [])

        if user_cart:
            # If the user has items in their cart, retrieve the latest item added
            last_item = user_cart[-1]
            speak_output = f"You just added {last_item} to your cart."
        else:
            # If the user has no items in their cart, inform them
            speak_output = "Your cart is empty."

        return handler_input.response_builder.speak(speak_output).response

class ModifyOrderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "ModifyOrderIntent"
        return ask_utils.is_intent_name("ModifyOrderIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        
        # Extract values from slots
        food_type = slots["foodtype"].value
        quantity = slots["quantity"].value
        
        # Check if the user provided both food type and quantity
        if food_type and quantity:
            # Logic to modify the order
            # Example: Update the order with the provided quantity for the specified food type
            speak_output = f"Your order has been updated to {quantity} {food_type}."
        else:
            # If either food type or quantity is missing, prompt the user for clarification
            speak_output = "I'm sorry, I couldn't understand your request. Please provide both the food type and quantity."
        
        # Return the response with speech and reprompt
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class RepeatOrderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "RepeatOrderIntent"
        return ask_utils.is_intent_name("RepeatOrderIntent")(handler_input)

    def handle(self, handler_input):
        # Retrieve the user's cart or order history from session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        user_cart = session_attr.get('cart', [])

        if user_cart:
            # If the user has items in their cart, repeat the latest item
            last_item = user_cart[-1]  # Get the latest item added to the cart
            speak_output = f"Sure, I've added {last_item} to your cart."
        else:
            # If the user has no items in their cart, inform them
            speak_output = "You haven't added anything to your cart yet."

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class CheckOutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "CheckOutIntent"
        return ask_utils.is_intent_name("CheckOutIntent")(handler_input)

    def handle(self, handler_input):
        # Retrieve session attributes
        session_attr = handler_input.attributes_manager.session_attributes

        # Check if the user has items in their cart
        user_cart = session_attr.get('cart', [])
        if not user_cart:
            speak_output = "Your cart is empty. Please add items to your cart before checking out."
            return handler_input.response_builder.speak(speak_output).response

    # Construct the confirmation message
        confirm_order_message = "Your order includes:"
        for item in user_cart:
            confirm_order_message += f" {item},"  # Append each item in the cart
        confirm_order_message += " Is this correct?"
        
        # Set the state to confirm the order
        session_attr['state'] = 'confirm_order'

        return (
            handler_input.response_builder
                .speak(confirm_order_message)
                .ask(confirm_order_message)
                .response
        )

class ConfirmCheckOutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "ConfirmCheckOutIntent"
        return ask_utils.is_intent_name("ConfirmCheckOutIntent")(handler_input)

    def handle(self, handler_input):
        # Retrieve session attributes
        session_attr = handler_input.attributes_manager.session_attributes

        # Check if the user has confirmed the order
        user_response = ask_utils.get_slot_value(handler_input, "confirmation")

        if user_response and user_response.lower() == "yes":
            # User confirmed the order, proceed with checkout logic
            # Example: Finalize the order, process payment, etc.
            session_attr['checked_out'] = True  # Set the flag to indicate the order has been checked out

            # Construct the response for completing the order
            order_summary = ", ".join(session_attr.get('cart', []))
            speak_output = f"Your order has been completed. You just ordered {order_summary}. Thank you for your purchase!"
            # Set the state to track the order
            session_attr['state'] = 'track_order'
        else:
            # User didn't confirm the order, handle accordingly
            speak_output = "Okay, let me know if you need any further assistance with your order."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class TrackOrderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "TrackOrderIntent"
        return ask_utils.is_intent_name("TrackOrderIntent")(handler_input)

    def handle(self, handler_input):
        # Check if the user has confirmed and checked out the order
        session_attr = handler_input.attributes_manager.session_attributes
        if session_attr.get('confirm_checked_out', False):
            # Your logic to track the order can go here
            # For example, you might check the order status in a database or external system
            order_status = "out for delivery"

            # Generate a response based on the order status
            if order_status:
                speak_output = f"Your order is currently {order_status}."
            else:
                speak_output = "I'm sorry, but we couldn't find information about your order at the moment."
        else:
            # User hasn't confirmed and checked out the order, so don't provide order tracking information
            speak_output = "You haven't placed an order yet or completed your purchase. Please complete your purchase first."

        # Return the response with speech and reprompt
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class RecommendationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the user invoked the "RecommendationIntent"
        return ask_utils.is_intent_name("RecommendationIntent")(handler_input)

    def handle(self, handler_input):
        # Extract the value of the "specialfood" slot from the request
        slots = handler_input.request_envelope.request.intent.slots
        special_food_slot = slots.get("specialfood")

        if special_food_slot and special_food_slot.value:
            # If the slot value exists, provide recommendations based on it
            special_food = special_food_slot.value
            speak_output = f"We have some special {special_food} available for you."
        else:
            # If the slot value is missing, provide a general message
            speak_output = "We have some special food items available for you."

        # Return the response with speech and reprompt
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response




class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FoodInfoIntentHandler())

sb.add_request_handler(OrderFoodIntentHandler())
sb.add_request_handler(CartManagementIntentHandler())
sb.add_request_handler(ModifyOrderIntentHandler())
sb.add_request_handler(RepeatOrderIntentHandler())
sb.add_request_handler(CheckOutIntentHandler())
sb.add_request_handler(ConfirmCheckOutIntentHandler())
sb.add_request_handler(RecommendationIntentHandler())
sb.add_request_handler(TrackOrderIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
lambda_handler = sb.lambda_handler()