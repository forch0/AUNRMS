# class DatabaseRouter:
#     def db_for_read(self, model, **hints):
#         # Route reads to the Supabase database
#         return 'supabase'

#     def db_for_write(self, model, **hints):
#         # Route writes to the default (local) database
#         return 'default'

#     def allow_relation(self, obj1, obj2, **hints):
#         # Allow relations between models in different databases
#         return True

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         # Allow migrations on both default and Supabase databases
#         if db in ['default', 'supabase']:
#             return True
#         return False

