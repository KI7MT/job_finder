"""
Job Finder

Gathers IT Jobs from the State of Montana,
which are located in Helena, MT, 
and notifies a group of users about it.

Built for the IT students of UM Helena.
"""

import requests
from lxml import html
import time
import urllib
import sqlite3
from db_util import db_util
from job import job
from recipient import recipient
from job_emailer import job_emailer

class job_finder(object):

	def __init__(self):
		"""Constructor"""

		self.dbu = db_util()

	def gather_and_review_jobs(self):

		self.mailer = job_emailer()

		self.current_recipients = self.dbu.gather_current_recipients()

		self.current_jobs = self.dbu.gather_current_jobs()

		changes_made = self.review_jobs()

		if changes_made: self.notify_recipients()

		self.dbu.close_connection()

		self.conn_closed = True

	def add_recipient(self,email):
		
		self.dbu.add_recipient(email)

	def remove_recipient(self,email):

		self.dbu.remove_recipient(email)

	def review_jobs(self):
		"""Gathers all the jobs from the State of MT jobs site,
		saving those that are new,
		and deleting those that have expired.
		"""

		jobs_on_site = self.gather_jobs_on_site()

		jobs_to_save = self.find_jobs_to_save(jobs_on_site)

		jobs_to_delete = self.find_jobs_to_delete(jobs_on_site)

		self.dbu.save_jobs(jobs_to_save)

		self.dbu.delete_jobs(jobs_to_delete)

		changes_made = len(jobs_to_save) > 0 or len(jobs_to_delete) > 0

		return changes_made

	def gather_jobs_on_site(self):
		"""Grabs the jobs from the State of MT website.
		
		Returns:
			list -- The of jobs to delete.
		"""

		jobs_on_site = []

		# Prepare everything necessary to gather the webpage data.
		url = 'https://mtstatejobs.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'

		headers = {'Content-Type':'application/json','Accept':'application/json'}

		payload = {"multilineEnabled":'false',"sortingSelection":{"sortBySelectionParam":"5","ascendingSortingOrder":"true"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":"","ORGANIZATION":""},"valid":'true'},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},{"id":"LOCATION","selectedValues":["20300100198"]},{"id":"JOB_FIELD","selectedValues":["7000100198"]}]},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]},{"id":"STUDY_LEVEL","selectedValues":[]},{"id":"WILL_TRAVEL","selectedValues":[]},{"id":"JOB_SHIFT","selectedValues":[]}]},"pageNo":1}

		# Gather the webpage data.
		response = requests.post(url, json=payload)

		json_data = response.json()

		# Pull out just the jobs data from the webpage data.
		jobs_data = json_data['requisitionList']

		# Iterate through the jobs data.
		for job_data in jobs_data:

			# Generated by the state, used to identify the job.
			site_id = job_data['jobId']

			# Generated by the state, used to identify the job's webpage.
			contest_num = job_data['contestNo']

			# The job's full webpage (I.e. contains all the detailed job info.)
			site_url = 'https://mtstatejobs.taleo.net/careersection/200/jobdetail.ftl?job={}'.format(contest_num)

			# Contains the primary job details such as...
			target_data = job_data['column']

			# ...Title...
			title = target_data[0]

			# ... and Department.
			dept = target_data[2]

			# Uncomment this to see what else is included.
			#print(target_data)

			# No way to guarantee that the site_id and contest_num will always be unique, so a hashcode is generated.
			job_id = hash(site_id + contest_num + site_url + title + dept)

			# Create a job object with the collected data.
			new_job = job([job_id,site_id,contest_num,title,dept,site_url])

			jobs_on_site.append(new_job)

		return jobs_on_site

	def find_jobs_to_save(self,jobs_on_site):

		jobs_to_save = []

		current_job_ids = self.gather_job_ids(self.current_jobs)

		for job in jobs_on_site:

			job_id = job.job_id

			if job_id not in current_job_ids: jobs_to_save.append(job)

		return jobs_to_save

	def find_jobs_to_delete(self,jobs_on_site):

		jobs_to_delete = []

		site_job_ids = self.gather_job_ids(jobs_on_site)

		for job in self.current_jobs:

			if job.job_id not in site_job_ids: jobs_to_delete.append(job)

		return jobs_to_delete

	def gather_job_ids(self,jobs):

		job_ids = []

		for job in jobs:

			job_ids.append(job.job_id)

		return job_ids

	def notify_recipients(self):
		"""Notifies all recipients in the database about a new job.
		
		Arguments:
			new_job {job} -- The job to notify recipeints of.
		"""
		for job in self.dbu.saved_jobs: self.mailer.notify_recipients_of_job(self.recipients,job)

		for job in self.dbu.deleted_jobs: self.mailer.notify_recipients_of_job(self.recipients,job,False)

def main():
	"""Main method"""

	try: 
		
		jf = job_finder()

		jf.gather_and_review_jobs()

	except:

		print('There was an error during job_finder execution.')

		if jf.conn_closed == False: jf.dbu.close_connection()

if __name__ == '__main__': main()