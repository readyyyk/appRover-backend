from .core import *


@invites_router.get('/group/{group_id}')
async def group_invite(group_id: int):
    pass


@invites_router.get('/poll/{poll_id}')
async def poll_invite(poll_id: int):
    pass


@invites_router.post('/poll/create/{poll_id}')
async def create_poll_invite(poll_id: int):
    pass


@invites_router.post('/group/create/{group_id}')
async def create_group_invite(group_id: int):
    pass
