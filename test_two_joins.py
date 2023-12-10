@escript
def test_two_joins(self):
    tp = self.tp
    dbp = self.dbp
    test_order_tp = dbp.test_order
    test_office_tp = dbp.test_shippment_office
    join_res = tp.join(test_order_tp, tp.node_id.__eq__(test_order_tp.test_customer_id))
    join_res.join(test_office_tp, test_order_tp.office_id.__eq__(test_office_tp.node_id))
    lst = ['bde']
    query = self.tp._and(tp.name._in(('abc', 'def')), tp.name._in(lst))
    res_header = join_res.read([test_office_tp.adress, tp.name, tp, test_order_tp, tp.country], test_office_tp.adress.__eq__('Washington str.'))
    res_no_header = join_res.read(test_office_tp.adress.__eq__('Washington str.'))
    res_empty = join_res.read()
    return query