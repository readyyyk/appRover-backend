from enum import Enum


class PollState(str, Enum):
    frozen = 'frozen'
    active = 'active'


class PollRole(str, Enum):
    voter = 'voter'
    viewer = 'viewer'
    admin = 'admin'
