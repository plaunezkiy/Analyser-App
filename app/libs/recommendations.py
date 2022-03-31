import pandas as pd

rec_combined = pd.DataFrame(index=['X', 'Y', 'Z'], columns=['A', 'B', 'C'])

rec_combined.loc['X']['A'] = 'High demand, high price, most profitable ' \
                'product, client most likely to pick it, mention ' \
                'last.'

rec_combined.loc['X']['B'] = 'High demand, medium price, most popular product, ' \
                'client most likely to pick it, highly profitable.'

rec_combined.loc['X']['C'] = 'High demand, low price, client very likely to pick, ' \
                'if offered, offer it last, ' \
                'medium profitability, big orders are uncommon.'

rec_combined.loc['Y']['A'] = 'Medium demand, high price, highly profitable, ' \
                'mention after the first one.'

rec_combined.loc['Y']['B'] = 'Medium demand, medium price, mention rarely, preferably ' \
                'in big orders.'

rec_combined.loc['Y']['C'] = 'Medium demand, low price, mention rarely in ' \
                'big orders, due to low profitability.'

rec_combined.loc['Z']['A'] = 'Low demand, high price, offer periodically ' \
                'highly profitable.'

rec_combined.loc['Z']['B'] = rec_combined.loc['Z']['C'] = \
    'Low demand, low/medium price, the product is usually sat ' \
    'in the warehouse in small quantities, offer at the start ' \
    'despite the lower price.'

xyz_rec = {
    'X': 'Stable demand.',
    'Y': 'Medium-stable demand.',
    'Z': 'Unstable demand.'
}

abc_rec = {
    'A': 'High price.',
    'B': 'Medium price.',
    'C': 'Low price.'
}

bcg_rec = {
    # Темп роста, Доля рынка
    'HIGH': {
        'LOW': 'Good sales growth, though comparing with leader, '
               'sales are low, offer a small batch for testing, '
               'potentially highly profitable.',

        'HIGH': 'High sales growth, high market share '
                'comparing to leader, client likely to be interested '
                'in buying, offer last, highly profitable.'
    },
    'LOW': {
        'LOW': 'Low sales growth & low market share, better not '
               'to mention at all, unprofitable.',

        'HIGH': 'High market share and low sales growth, likely to be a '
                'new product with a stable demand, offer often.'
    },
}
