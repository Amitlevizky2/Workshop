import datetime


class Statistics:
    def __init__(self):
        self.stat_by_day = {}
        self.guests = 0
        self.reg_users = 0
        self.managers = 0
        self.owners = 0

    def get_today_statistics(self):
            self.stat_by_day[datetime.date.today()] = {
                'guests': self.guests,
                'registered_users': self.reg_users,
                'managers': self.managers,
                'owners': self.owners,
            }

            return self.stat_by_day

    def get_range_statistics(self, start_date, end_date):
        range_stats = {
            'guests': 0,
            'registered_users': 0,
            'managers': 0,
            'owners': 0,
        }

        self.get_today_statistics()

        for _date in self.stat_by_day.keys():
            if start_date <= datetime.date.today() <= end_date:
                if _date in self.stat_by_day.keys():
                    range_stats['guests'] += self.stat_by_day[_date]['guests']
                    range_stats['registered_users'] += self.stat_by_day[_date]['registered_users']
                    range_stats['managers'] += self.stat_by_day[_date]['managers']
                    range_stats['owners'] += self.stat_by_day[_date]['owners']

        return range_stats

    def add_guests_stats(self):
        self.is_new_day()
        self.guests += 1

    def remove_guests_stats(self):
        self.guests += 1

    def add_reg_users(self):
        self.is_new_day()
        self.reg_users += 1

    def add_managers(self):
        self.is_new_day()
        self.managers += 1

    def add_owners(self):
        self.is_new_day()
        self.owners += 1

    def is_new_day(self):
        if datetime.date.today() not in self.stat_by_day.keys():
            self.guests = 0
            self.reg_users = 0
            self.managers = 0
            self.owners = 0