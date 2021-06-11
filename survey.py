#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:23:50 2021

@author: simplon
"""

import pandas as pd
from sqlalchemy import create_engine
import re

def fill_table_df(table_name,data,data_col_name):
    columns_name = pd.read_sql_query("select * from "+table_name+" limit 1;",engine).columns
    table_df = pd.DataFrame(columns = columns_name)
    table_df[columns_name[1]] = data[data_col_name]
    table_df.drop_duplicates(inplace=True)
    table_df[columns_name[0]] = [x+1 for x in range(table_df.shape[0])]
    return table_df

def fill_FK(df_data,data_col_name,df_PK,df_FK,id_name,name):
    l_temp=[]
    for label, row in df_data.iterrows():
        for label2, row2 in df_PK.iterrows():
            if (row[data_col_name] == row2[name]):
                l_temp.append(row2[id_name])
    if id_name=='db_id':
        df_FK['primary_db_id'] = l_temp
    else:
        df_FK[id_name] = l_temp

def push_df_db(l_df,engine):    
    for i in l_df:
        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        i[1].to_sql(i[0], if_exists='append', con=engine, index=False)

data_file = "01_Data_Professional_Salary_Survey_Responses_remi.xlsx"
data_path = "/home/simplon/Documents/Brief/"

data = pd.read_excel(data_path + data_file,
                     sheet_name='Salary Survey',
                     header=0)

engine = create_engine("mysql+pymysql://remi:Simplon21!@localhost/survey")

df_to_sql = []

# sondage
table = 'sondage'
df_sondage = fill_table_df(table, data,'Survey Year')
df_to_sql.append((table,df_sondage))

# carreer_plan
table = 'carreer_plan'
df_career_plan = fill_table_df(table, data, 'CareerPlansThisYear')
df_to_sql.append((table,df_career_plan))

# how_many_companies HowManyCompanies 0 = NA 6 = 6 and more
table = "how_many_companies"
df_hmc = fill_table_df(table, data, "HowManyCompanies")
df_to_sql.append((table,df_hmc))

# certification
table = "certification"
df_certification = fill_table_df(table, data, "Certifications")
df_to_sql.append((table,df_certification))

# country
table = "country"
df_country = fill_table_df(table, data, 'Country')
df_to_sql.append((table,df_country))

# employment_sector
table = 'employment_sector'
df_employment_sector = fill_table_df(table, data, "EmploymentSector")
df_to_sql.append((table,df_employment_sector))

# employment_status "EmploymentStatus"
table = 'employment_status'
df_employment_status = fill_table_df(table, data, "EmploymentStatus")
df_to_sql.append((table,df_employment_status))

# largest_city
table = "largest_city"
df_largest_city = fill_table_df(table, data, "PopulationOfLargestCityWithin20Miles")
df_to_sql.append((table,df_largest_city))

# looking_job "LookingForAnotherJob"
table = "looking_job"
df_looking_job = fill_table_df(table, data, "LookingForAnotherJob")
df_to_sql.append((table,df_looking_job))

# education "Education"
table = "education"
df_education = fill_table_df(table, data, "Education")
df_to_sql.append((table,df_education))

# job
table = "job"
df_job = fill_table_df(table, data, "JobTitle")
df_to_sql.append((table,df_job))

# task
s_tasks = data['KindsOfTasksPerformed']
s_tasks = s_tasks.unique()
l_tasks = []
exp = "[^,(\s]+ \([^\(]*\)|[^,(\s]+ [^,]*\([^\(]*\)|[^,(\s]+ [^,\(]*|[^,\s]+"
for t in s_tasks:
    if type(t)==type(''):
        # l_tasks+=t.split()
        l_tasks += re.findall(exp,t)
    else:
        l_tasks.append('Not Asked')
l_tasks = list(set(l_tasks))
table = 'task'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
df_task = pd.DataFrame(columns = columns_name)
df_task[columns_name[1]] = l_tasks
df_task[columns_name[0]] = [x+1 for x in range(df_task.shape[0])]
df_to_sql.append((table,df_task))

# primaryDB
table = "database_used"
df_db_used = fill_table_df(table, data, "PrimaryDatabase")

l_other_dbs = ['Informix', 'Hadoop', 'Sybase', 'Progress', 'memSQL', 'Ingres',
               'InterBase', 'FireBird', 'Google Cloud', 'Access', 'Redis', 'BigQuery']
mon_df = pd.DataFrame(columns=df_db_used.columns)
mon_df[df_db_used.columns[1]]=l_other_dbs
mon_df[df_db_used.columns[0]]=[x+df_db_used.shape[0]+1 for x in range(len(l_other_dbs))]
df_db_used.reset_index(drop = True, inplace = True)
mon_df.reset_index(drop = True, inplace = True)
mon_df.index += df_db_used.shape[0]
df_db_used = pd.concat([df_db_used,mon_df])
df_to_sql.append((table,df_db_used))

# sondage_item
df_sondage_item = pd.DataFrame()
df_sondage_item['sgi_id']=0
df_sondage_item[['survey_year', 'timestamp', 'salary_usd']] = data[['Survey Year','Timestamp','SalaryUSD']]
df_sondage_item[['postal_code', 'years_with_db', 'manage_staff']] = data[['Zone','YearsWithThisDatabase','ManageStaff']]
df_sondage_item[['years_with_job', 'other_people', 'company_employee']] = data[['YearsWithThisTypeOfJob','OtherPeopleOnYourTeam','CompanyEmployeesOverall']]
df_sondage_item[['database_servers', 'eduction_computer', 'hours_worked']] = data[['DatabaseServers','EducationIsComputerRelated','HoursWorkedPerWeek']]
df_sondage_item[['telecommute', 'newest_version', 'oldest_version', 'gender']] = data[['TelecommuteDaysPerWeek','NewestVersionInProduction', 'OldestVersionInProduction', 'Gender']]
df_sondage_item['sgi_id']=[x+1 for x in range(df_sondage_item.shape[0])]

table = 'sondage'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data,'Survey Year', df_sondage, df_sondage_item, columns_name[0], columns_name[1])

table = 'carreer_plan'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data,'CareerPlansThisYear', df_career_plan, df_sondage_item, columns_name[0], columns_name[1])

table = "how_many_companies"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data,'HowManyCompanies', df_hmc, df_sondage_item, columns_name[0], columns_name[1])

table = "certification"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "Certifications",df_certification, df_sondage_item, columns_name[0], columns_name[1])

table = "country"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, 'Country', df_country, df_sondage_item, columns_name[0], columns_name[1])

table = 'employment_sector'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "EmploymentSector", df_employment_sector, df_sondage_item, columns_name[0], columns_name[1])

table = 'employment_status'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "EmploymentStatus", df_employment_status, df_sondage_item, columns_name[0], columns_name[1])

table = "largest_city"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "PopulationOfLargestCityWithin20Miles", df_largest_city, df_sondage_item, columns_name[0], columns_name[1])

table = "looking_job"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "LookingForAnotherJob", df_looking_job, df_sondage_item, columns_name[0], columns_name[1])

table = "education"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "Education", df_education, df_sondage_item, columns_name[0], columns_name[1])

table = "job"
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "JobTitle", df_job, df_sondage_item, columns_name[0], columns_name[1])

table = 'database_used'
columns_name = pd.read_sql_query("select * from "+table+" limit 1;",engine).columns
fill_FK(data, "PrimaryDatabase", df_db_used, df_sondage_item, columns_name[0], columns_name[1])
df_to_sql.append(('sondage_item',df_sondage_item))

# otherDB: ajout d'autre db par exploration
# Progress==OpenEdge et mysql mariadb seul
l_sgi_id, l_db_id = [], []
for i in range(data.shape[0]):
    for j in range(df_db_used.shape[0]):
        temp=data.iloc[i]['OtherDatabases']
        if type(temp)==type(""):
            if temp.upper().find(df_db_used.iloc[j]['db_name'].upper())!=-1:
                l_sgi_id.append(df_sondage_item.iloc[i]['sgi_id'])
                l_db_id.append(df_db_used.iloc[j]['db_id'])
            elif temp.upper().find('OPENEDGE')!=-1:
                l_sgi_id.append(df_sondage_item.iloc[i]['sgi_id'])
                l_db_id.append(19)
            elif temp.upper().find('MYSQL')!=-1 or temp.upper().find('MARIADB')!=-1:
                l_sgi_id.append(df_sondage_item.iloc[i]['sgi_id'])
                l_db_id.append(9)
df_other_db = pd.DataFrame()
df_other_db['sgi_id']=l_sgi_id
df_other_db['db_id']=l_db_id
df_other_db.drop_duplicates(inplace=True)
df_to_sql.append(('other_database',df_other_db))

# OtherJobDuties
l_sgi_id, l_job_id = [], []
for i in range(data.shape[0]):
    for j in range(df_job.shape[0]):
        temp=data.iloc[i]['OtherJobDuties']
        if type(temp)==type(""):
            if temp.upper().find(df_job.iloc[j]['job_name'].upper())!=-1:
                l_sgi_id.append(df_sondage_item.iloc[i]['sgi_id'])
                l_job_id.append(df_job.iloc[j]['job_id'])
df_other_job = pd.DataFrame()
df_other_job['sgi_id']=l_sgi_id
df_other_job['job_id']=l_job_id
df_to_sql.append(('other_duties',df_other_job))

# TasksPerformed
l_sgi_id, l_tas_id = [], []
for i in range(data.shape[0]):
    for j in range(df_task.shape[0]):
        temp=data.iloc[i]['KindsOfTasksPerformed']
        if type(temp)==type(""):
            if temp.upper().find(df_task.iloc[j]['tas_name'].upper())!=-1:
                l_sgi_id.append(df_sondage_item.iloc[i]['sgi_id'])
                l_tas_id.append(df_task.iloc[j]['tas_id'])
df_task_perf = pd.DataFrame()
df_task_perf['sgi_id']=l_sgi_id
df_task_perf['tas_id']=l_tas_id
df_to_sql.append(('task_performed',df_task_perf))

push_df_db(df_to_sql,engine)