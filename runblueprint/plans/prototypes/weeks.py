from plans.week import Week_types, Week_variants
from plans.day import Day_types
from plans.plan import Phases


prototypes = {
    Week_types.Base: {
        0: {  # Monday
            'percent_of_weekly_distance': 0.075,
            'type': 'easy'
        },
        1: {
            'percent_of_weekly_distance': 0.125,
            'type': 'easy'
        },
        2: {
            'percent_of_weekly_distance': 0.2,
            'type': 'easy'
        },
        3: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        4: {
            'percent_of_weekly_distance': 0,
            'type': 'crosstrain',
        },
        5: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        6: {
            'percent_of_weekly_distance': 0.4,
            'type': 'long',
        }
    },
    Week_types.Work: {
        0: {  # Monday
            'percent_of_weekly_distance': 0.075,
            'type': 'easy'
        },
        1: {
            'percent_of_weekly_distance': 0.125,
            'type': 'easy'
        },
        2: {
            'percent_of_weekly_distance': 0.2,
            'type': 'quality'
        },
        3: {
            'percent_of_weekly_distance': 0.1,
            'type': 'recovery'
        },
        4: {
            'percent_of_weekly_distance': 0,
            'type': 'crosstrain',
        },
        5: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        6: {
            'percent_of_weekly_distance': 0.4,
            'type': 'long',
        }
    },
    Week_types.Growth: {
        0: {  # Monday
            'percent_of_weekly_distance': 0.075,
        },
        1: {
            'percent_of_weekly_distance': 0.125,
            'type': 'easy'
        },
        2: {
            'percent_of_weekly_distance': 0.2,
        },
        3: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        4: {
            'percent_of_weekly_distance': 0,
            'type': 'crosstrain',
        },
        5: {
            'percent_of_weekly_distance': 0.1,
        },
        6: {
            'percent_of_weekly_distance': 0.4,
        }
    },
    Week_types.Taper: {
        0: {  # Monday
            'percent_of_weekly_distance': 0.075,
            'type': 'easy'
        },
        1: {
            'percent_of_weekly_distance': 0.125,
            'type': 'easy'
        },
        2: {
            'percent_of_weekly_distance': 0.2,
            'type': 'easy'
        },
        3: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        4: {
            'percent_of_weekly_distance': 0,
            'type': 'crosstrain',
        },
        5: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        6: {
            'percent_of_weekly_distance': 0.4,
            'type': 'long',
        }
    },
    Week_types.Recovery: {
        0: {  # Monday
            'percent_of_weekly_distance': 0.075,
            'type': 'recovery'
        },
        1: {
            'percent_of_weekly_distance': 0.125,
            'type': 'recovery'
        },
        2: {
            'percent_of_weekly_distance': 0.2,
            'type': 'rest'
        },
        3: {
            'percent_of_weekly_distance': 0.1,
            'type': 'easy'
        },
        4: {
            'percent_of_weekly_distance': 0,
            'type': 'crosstrain',
        },
        5: {
            'percent_of_weekly_distance': 0.1,
            'type': 'recovery'
        },
        6: {
            'percent_of_weekly_distance': 0.4,
            'type': 'easy'
        }
    }
}
