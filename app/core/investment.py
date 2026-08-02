from datetime import datetime


def process_investment(target, sources: list):
    """
    Распределяет средства между целевым объектом
    и списком доступных источников
    """
    for source in sources:
        target_need = target.full_amount - target.invested_amount
        source_free = source.full_amount - source.invested_amount

        invest_amount = min(target_need, source_free)

        target.invested_amount += invest_amount
        source.invested_amount += invest_amount

        if target.full_amount == target.invested_amount:
            target.fully_invested = True
            target.close_date = datetime.now()

        if source.full_amount == source.invested_amount:
            source.fully_invested = True
            source.close_date = datetime.now()

        if target.fully_invested:
            break

    return target, sources
