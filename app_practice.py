import database1 

database1.show_all()
# database1.add_one('Norocel','Balcescu','Nororcel@codemy.com')
database1.show_all()
# database1.delete_one('9')
database1.show_all()
database1.add_many([('Ovi','copertinescu','coperty@codemy.com'), 
                    ('Marcel','Vasilache','Marcel@codemy.com')])
database1.show_all()
database1.conn.close()