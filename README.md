![Licence](https://img.shields.io/badge/licence-AGPL--3-blue.svg)
git 
TechTools Localización de Odoo para Ecuador
=================================

Este proyecto crea una localización para ecuador soportado para la version 14 Comunity de Odoo.

- version 1.0 no soporta facturación electrónica
- version 1.2 soporta facturacion electrónica (en desarrollo)
- version 1.2.2 Factura electronicamente de manera correcta
- version 1.3.0 Se cambia la lógica de asignacion de punto de emisión
   cada documento electrónico tiene su punto de emisión
   Ej. Factura Local ->pto emision 001
       Factura Exportación ->pto emision 002
       Nota de Crédito  ->pto emision 003
       Guia de Remisión ->pto emision 004  

Puntos a tener en cuenta en la implementación:
---------------------------------------------
 - Establecer el método de costeo de inventario al momento de cargar las categorías de productos
 - Establecer permiso de lectura/escritura para la ruta rides/utils/signP12
    - Aquí se cargan las firmas digitales de los clientes
 - Establecer permiso de lectura/escritura para el path configurado para los comprobantes electrónicos
    - Aquí se generan los pdf y xml de los documentos electrónicos
 - cuando se creen las variables de entorno para java y python hacerlas a nivel de sistema no de usuario 

Estado de Módulos:
-----------------
| MODULO                   | ESTADO    | OBSERVACIONES                           |
|--------------------------|-----------|-----------------------------------------|
| res_partner_ec   | Finalizado| configuraciones de la compañía
| rides   | Finalizado| factura electrónica
| ridesReports   | Finalizado| generación de layouts
| sale_order_line_check_stock   | Finalizado| Impide crear un pedido si no hay stock
| sale_order_line_view_weight   | Finalizado| Registrar el peso en la línea del pedido
| tt_config   | Finalizado| establece los costos de los productos si ya han sido ingresados
| tt_activos_fijos   | En Desarrollo | Gestión de activos fijos 

