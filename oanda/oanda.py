from accounts import indicies, hk33, commodities, currencies
from heikin_strategy import SimpleHeikinStrategy
from accounts import lillian2_token, lillian2_ID
from accounts import lillian_token, lillian_ID
from amazing import AmazingCrossoverStrategy
from accounts import peter_token, peter_ID
from monitor import save_account_summary
from ichimoku import IchimokuStrategy
from config import trading_app

window = 'H1'

@trading_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3500, run_ichi_cron.s('args'), name='ichimoku_strategy')
    sender.add_periodic_task(3500, run_heikin_cron.s('args'), name='heikin_strategy')
    sender.add_periodic_task(3500, run_amazing_cron.s('args'), name='amazing_strategy')
    sender.add_periodic_task(300, run_summary_collection.s('args'), name='summary_collection')

@trading_app.task
def run_summary_collection(args):
    for name in ['peter', 'lillian', 'lillian2']:
        if name == 'peter':
            save_account_summary.delay(name, peter_token, peter_ID)
        elif name == 'lillian':
            save_account_summary.delay(name, lillian_token, lillian_ID)
        elif name == 'lillian2':
            save_account_summary.delay(name, lillian2_token, lillian2_ID)

@trading_app.task
def run_ichi_cron(args):
    for instr in indicies:
        IchimokuStrategy.delay(peter_ID, peter_token, instr, window, 1)
    for instr in hk33:
        IchimokuStrategy.delay(peter_ID, peter_token, instr, window, 10)
    for instr in commodities:
        IchimokuStrategy.delay(peter_ID, peter_token, instr, window, 100)
    for instr in currencies:
        IchimokuStrategy.delay(peter_ID, peter_token, instr, window, 10000)

@trading_app.task
def run_amazing_cron(args):
    for instr in indicies:
        AmazingCrossoverStrategy.delay(lillian_ID, lillian_token, instr, window, 1)
    for instr in hk33:
        AmazingCrossoverStrategy.delay(lillian_ID, lillian_token, instr, window, 10)
    for instr in commodities:
        AmazingCrossoverStrategy.delay(lillian_ID, lillian_token, instr, window, 100)
    for instr in currencies:
        AmazingCrossoverStrategy.delay(lillian_ID, lillian_token, instr, window, 10000)

@trading_app.task
def run_heikin_cron(args):
    for instr in indicies:
        SimpleHeikinStrategy.delay(lillian2_ID, lillian2_token, instr, window, 1)
    for instr in hk33:
        SimpleHeikinStrategy.delay(lillian2_ID, lillian2_token, instr, window, 10)
    for instr in commodities:
        SimpleHeikinStrategy.delay(lillian2_ID, lillian2_token, instr, window, 100)
    for instr in currencies:
        SimpleHeikinStrategy.delay(lillian2_ID, lillian2_token, instr, window, 10000)
