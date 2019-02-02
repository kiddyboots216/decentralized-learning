from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import pandas as pd
import os
import time


class DBClient(object):
	"""
	DBClient

	- Label datasets and retrieve datasets with corresponding category
	- Needed here so that DL2 Notebook can retrieve classifications
	- Will most likely replace RDS DB with DynamoDB for performance reasons, 
	  but I'll figure that out after MVP

	TODO: authenthication needs to be set up for DB
	"""
	
	def __init__(self, config):
		"""
		Set up DBClient with corresponding database credentials
		"""
		app = Flask(__name__)
		app.config['SQLALCHEMY_DATABASE_URI'] =  \
			'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
				user=config.get('DB_CLIENT', 'user'),
				pw=os.environ['DB_PASS'],
				host=config.get('DB_CLIENT', 'host'),
				port=config.getint('DB_CLIENT', 'port'),
				db=config.get('DB_CLIENT', 'db')
			)
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		self.db = SQLAlchemy(app)
		self.table_name = config.get('DB_CLIENT', 'table_name')
		self.num_tries = config.getint('DB_CLIENT', 'num_tries')
		self.wait_time = config.getint('DB_CLIENT', 'wait_time')

	def get_classifications(self):
		"""
		Get category_labels table. Returns DataFrame.
		"""
		query = "select * from {table_name}".format(table_name=self.table_name)
		for _ in range(self.num_tries):
			try:
				return pd.read_sql_query(query, self.db.engine)
			except Exception as e:
				time.sleep(self.wait_time)
				continue
		raise Exception('Getting classifications failed.')

	def get_data_providers_with_category(self, category):
		"""
		Get a list of data providers with the given category. Returns DataFrame.
		"""
		query = "select * from {table_name} where category = '{category}'".format(
			category=category, 
			table_name=self.table_name
		)
		for _ in range(self.num_tries):
			try:
				return pd.read_sql_query(query, self.db.engine)
			except Exception as e:
				time.sleep(self.wait_time)
				continue
		raise Exception('Getting classifications failed.')
		