def hay_productos_sin_stock(self):
    sin_stock = False
    for line in self:
        # si la cantidad del producto es mayor que el stock
        if (line.product_id
                and line.product_id.type == 'product'
                and line.product_uom_qty > line.product_id.qty_available):
            sin_stock = True
    return sin_stock
