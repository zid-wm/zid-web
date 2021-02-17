"""
This module contains definitions for alerts which can be shown on the homepage.
Allowed alert types:
    primary
    secondary
    success (green)
    danger (red)
    warning (yellow)
    info
    light
    dark
"""

MESSAGES = {
    0: {
        'type': 'warning',
        'text': 'Error displaying the requested alert message. The webmaster has been notified.'
    },
    1: {
        'type': 'success',
        'text': 'Your request for event staffing was successfully submitted.'
    },
    2: {
        'type': 'success',
        'text': 'Your feedback was successfully submitted.'
    },
    3: {
        'type': 'success',
        'text': 'Your email was successfully sent.'
    },
    4: {
        'type': 'success',
        'text': 'You have been successfully logged out!'
    },
    5: {
        'type': 'success',
        'text': 'You have been successfully logged in!'
    },
    6: {
        'type': 'success',
        'text': 'Your visiting request has been successfully submitted.'
    },
    7: {
        'type': 'success',
        'text': 'News article successfully posted.'
    }
}
