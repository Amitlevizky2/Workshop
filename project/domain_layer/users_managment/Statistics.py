from datetime import datetime, date

from project.data_access_layer.StatsORM import StatsORM


class Statistics:
    def __init__(self, orm=None):
        self.publisher = None
        # today = str(date.today())
        self.stat_by_day = {}
        self.guests = 0
        self.reg_users = 0
        self.managers = 0
        self.owners = 0
        if orm is None:
            self.orm = StatsORM()
            self.orm.guests = self.guests
            self.orm.reg_users = self.reg_users
            self.orm.managers = self.managers
            self.orm.owners = self.owners
            self.orm.add()
        else:
            self.orm = orm
            orm.add()
        self.stat_by_day[str(date.today())] = {
            'guests': self.guests,
            'registered_users': self.reg_users,
            'managers': self.managers,
            'owners': self.owners,
        }


    def get_today_statistics(self):
        """
        :return: returns number of guest users, number of registered users, number of store managers and owners visited the store TODAY
        """
        today = str(date.today())
        if today not in self.stat_by_day.keys():
            self.stat_by_day[today] = {
                'guests': self.guests,
                'registered_users': self.reg_users,
                'managers': self.managers,
                'owners': self.owners,
            }
            self.orm = StatsORM()
            self.orm.date = today
            self.orm.guests=self.guests
            self.orm.reg_users=self.reg_users
            self.orm.managers=self.managers
            self.orm.owners= self.owners
            self.orm.add()
        else:
            # today_stats = self.stat_by_day[date.today()]
            self.stat_by_day[today]['guests'] = self.guests
            self.stat_by_day[today]['registered_users'] = self.reg_users
            self.stat_by_day[today]['managers'] = self.managers
            self.stat_by_day[today]['owners'] = self.owners
        return self.stat_by_day[today]

    def get_range_statistics(self, _start_date, _end_date):
        start_date = datetime.strptime(_start_date, '%Y-%m-%d')
        end_date = datetime.strptime(_end_date, '%Y-%m-%d')
        """
        :param start_date: starting date
        :param end_date: end date
        :return: returns number of guest users, number of registered users, number of store managers and owners
                visited the store on those days.
        """
        range_stats = {
            'guests': 0,
            'registered_users': 0,
            'managers': 0,
            'owners': 0,
        }

        self.get_today_statistics()

        for _date in self.stat_by_day.keys():
            if start_date <= date.today() <= end_date:
                if _date in self.stat_by_day.keys():
                    range_stats['guests'] += self.stat_by_day[_date]['guests']
                    range_stats['registered_users'] += self.stat_by_day[_date]['registered_users']
                    range_stats['managers'] += self.stat_by_day[_date]['managers']
                    range_stats['owners'] += self.stat_by_day[_date]['owners']

        return range_stats

    def get_all_data(self):
        self.get_today_statistics()
        return self.stat_by_day
        # if not date.today() in self.stat_by_day.keys():
        #     self.get_today_statistics()
        #     return self.stat_by_day
        # today_stats = self.stat_by_day[datetime.today()]
        # today_stats['guests'] = self.guests
        # today_stats['registered_users'] = self.reg_users
        # today_stats['managers'] = self.managers
        # today_stats['owners'] = self.owners
        # return self.stat_by_day

    def add_guests_stats(self):
        self.is_new_day()
        self.guests += 1
        if self.orm is not None:
            self.orm.update_guest()
        self.notify_admins()

    def remove_guests_stats(self):
        self.guests = self.guests - 1
        if self.orm is not None:
            self.orm.reduce_guest()

    def add_reg_users(self):
        self.is_new_day()
        self.reg_users += 1
        if self.orm is not None:
            self.orm.update_reg_users()
        self.notify_admins()

    def add_managers(self):
        self.is_new_day()
        self.managers += 1
        if self.orm is not None:
            self.orm.update_managers()
        self.notify_admins()

    def add_owners(self):
        self.is_new_day()
        self.owners += 1
        if self.orm is not None:
            self.orm.update_owner()
        self.notify_admins()

    def is_new_day(self):
        today = str(date.today())
        if today not in self.stat_by_day.keys():
            self.guests = 0
            self.reg_users = 0
            self.managers = 0
            self.owners = 0
            self.orm = StatsORM()
            self.orm.date = today
            self.orm.guests = self.guests
            self.orm.reg_users = self.reg_users
            self.orm.managers = self.managers
            self.orm.owners = self.owners
            self.orm.add()

    def set_publisher(self, publisher):
        self.publisher = publisher

    def notify_admins(self):
        st = self.get_all_data()
        print(st)
        self.publisher.notify_admins(st)
