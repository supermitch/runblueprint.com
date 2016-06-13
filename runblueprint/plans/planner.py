import uuid


class Plan():
    def __init__(self):
        self.id = uuid.uuid1().hex
        self.weeks = []

    def __str__(self):
        return 'Plan {}: {} weeks'.format(self.id, len(self.weeks))


def sanity_check(data):
    return "{}, your plan is {} weeks long.".format(data['your_name'], data['weeks'])

def generate_plan(data):
    plan = Plan()
    weeks = data['weeks']
    while weeks > 0:
        plan.weeks.append(plan_week())
        weeks -= 1
    return plan

def plan_week():
    week = {'days': [],
            'total_dist': 0}
    days = 7
    for i in range(0, 7):
        week['days'].append({'day': i, 'dist': 5})
    return week

def stringify_plan(plan):
    """print plan out to console for debugging"""
    print(plan)
