from data.iterators import count_datapoints, create_train_dataset_iterator, create_test_dataset_iterator
import pandas as pd
import os
import pytest


@pytest.fixture
def dataset_path():
	return "tests/artifacts/iterators"

def test_train_test_split(dataset_path):
	"""
	Test train-test split works by:
		1. Checking the split put the right number of datapoints (proportional 
		   to the total number) in the training and test datasets.
		2. Checking that datapoints don't overlap between each dataset
	"""

	count = count_datapoints(dataset_path)

	#Set up iterator for training set
	train_iterator = create_train_dataset_iterator(
			dataset_path,
			count,
			batch_size=7,
			labeler=0,
			infinite=False 
		)

	#Set up iterator for test set.
	test_iterator = create_test_dataset_iterator(
			dataset_path,
			count,
			batch_size=7,
			labeler=0,
			infinite=False
		)

	#Collect "datapoints" for training and test set. In reality, just take the 
	#index so that overlapping points can be detected later.
	train_data = []
	for X,y in train_iterator:
		for datapoint in X:
			train_data.append(datapoint[-1])

	test_data = []
	for X,y in test_iterator:
		for datapoint in X:
			test_data.append(datapoint[-1])

	#Check that training set and test set have right number of datapoints
	assert len(train_data) == 0.8*count
	assert len(test_data) == 0.2*count

	#Set up dataframe for join
	train_df = pd.DataFrame(data={"index": train_data})
	test_df = pd.DataFrame(data={"index": test_data})

	#Check for no overlapping datapoints
	assert len(pd.merge(train_df, test_df, on='index').index) == 0

def test_large_batch_size(dataset_path):
	"""
	Same as above, except test with batch_size > count (datapoints)
	"""

	count = count_datapoints(dataset_path)

	#Set up iterator for training set
	train_iterator = create_train_dataset_iterator(
			dataset_path,
			count,
			batch_size=2000,
			labeler=0,
			infinite=False 
		)

	#Set up iterator for test set.
	test_iterator = create_test_dataset_iterator(
			dataset_path,
			count,
			batch_size=2000,
			labeler=0,
			infinite=False
		)

	#Collect "datapoints" for training and test set. In reality, just take the 
	#index so that overlapping points can be detected later.
	train_data = []
	for X,y in train_iterator:
		for datapoint in X:
			train_data.append(datapoint[-1])

	test_data = []
	for X,y in test_iterator:
		for datapoint in X:
			test_data.append(datapoint[-1])

	#Check that training set and test set have right number of datapoints
	assert len(train_data) == 0.8*count
	assert len(test_data) == 0.2*count

	#Set up dataframe for join
	train_df = pd.DataFrame(data={"index": train_data})
	test_df = pd.DataFrame(data={"index": test_data})

	#Check for no overlapping datapoints
	assert len(pd.merge(train_df, test_df, on='index').index) == 0

def test_invalid_batch_size(dataset_path):
	"""
	Test that assertion fails with invalid batch size.
	"""
	count = count_datapoints(dataset_path)

	#Set up iterator for training set
	train_iterator = create_train_dataset_iterator(
			dataset_path,
			count,
			batch_size=-1,
			labeler=0,
			infinite=False 
		)

	#Set up iterator for test set.
	test_iterator = create_test_dataset_iterator(
			dataset_path,
			count,
			batch_size=-1,
			labeler=0,
			infinite=False
		)

	#Assertion should fail here.
	try:
		train_data = []
		for X,y in train_iterator:
			for datapoint in X:
				train_data.append(datapoint[-1])
		assert False,"Assertion for batch size should have failed"
	except AssertionError as e:
		assert str(e) == "Invalid batch size provided."

def test_labeler_out_of_bounds(dataset_path):
	"""
	Test that assertion fails with invalid labeler.
	"""
	count = count_datapoints(dataset_path)

	#Set up iterator for training set
	train_iterator = create_train_dataset_iterator(
			dataset_path,
			count,
			batch_size=7,
			labeler=-1,
			infinite=False 
		)

	#Set up iterator for test set.
	test_iterator = create_test_dataset_iterator(
			dataset_path,
			count,
			batch_size=7,
			labeler=-1,
			infinite=False
		)

	#Assertion should fail here.
	try:
		train_data = []
		for X,y in train_iterator:
			for datapoint in X:
				train_data.append(datapoint[-1])
		assert False,"Assertion for labeler should have failed."
	except AssertionError as e:
		assert str(e) == "Labeler is out of bounds."
