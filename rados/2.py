#coding=utf-8
import os,sys,rados,json,requests
import pdb
import boto,boto.s3.connection
from boto.s3.cors import CORSConfiguration
url="http://192.168.136.187:10001"

def user_info(uid):
	cmd_line="radosgw-admin user info --uid=%s"%uid
	out=os.popen(cmd_line).readlines()
	user_info_with_json_format=''.join(out)
	user_info_dict=json.loads(user_info_with_json_format)
	info_s3=user_info_dict["keys"]
	info_swift=user_info_dict["swift_keys"]
	return info_s3,info_swift

def swift_api_auth(user,key):
	path="/auth"
	headers={"X-Auth-User":user,"X-Auth-Key":key}
	rsp=requests.get(url+path,headers=headers)
	h=rsp.headers
	return h["X-Storage-Url"],h["X-Storage-Token"]

def out_storage_info(XSU,headers):
	account_list=requests.get(XSU,headers=headers).text.split('\n')
	print "--------------begin--------------------------------------------"	
	for account in account_list:
		print '-',account,":"
		container_list=requests.get(XSU+'/'+account,headers=headers).text.split('\n')
		for container in container_list:
			print '   -',container,':'
			obj_list=requests.get(XSU+'/'+account+'/'+container,headers=headers).text.split('\n')
			for obj in obj_list:
				print '       -',obj
	print "--------------end-----------------------------------------------"	

def s3_connect(access_key,secret_key):
	conn = boto.connect_s3(
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	host = "192.168.136.187",port=10001,
	is_secure=False,
	calling_format = boto.s3.connection.OrdinaryCallingFormat())
	return conn

if __name__=="__main__":
	info_s3,info_swift=user_info("mxx")
	if len(info_swift)<1:
		sys.exit(0)
	
	user=info_swift[0]["user"]
	key=info_swift[0]["secret_key"]
	XSU,XST=swift_api_auth(user,key)
	headers={"X-Auth-Token":XST,"limit":10,"offset":0,"format":"json"}
	'''
	out_storage_info(XSU,headers)
	requests.put(XSU+"/abc",headers=headers)	
	requests.put(XSU+"/abc/def",headers=headers)	
	requests.put(XSU+"/abc/def/a",headers=headers,data="wo")	
	requests.put(XSU+"/abc/def/b",headers=headers,data="go")	
	requests.put(XSU+"/abc/def/c",headers=headers,data="op")	
	requests.put(XSU+"/abc/def/d",headers=headers,data="no")	
	out_storage_info(XSU,headers)
	'''
	access_key=info_s3[0]["access_key"]
	secret_key=info_s3[0]["secret_key"]
	s3_conn=s3_connect(access_key,secret_key)
	#import pdb;pdb.set_trace()	
	s3_conn.create_bucket("eisoo")
	bkt=s3_conn.get_bucket('eisoo')
	#cors=bkt.get_cors()
	config=CORSConfiguration()
	config.add_rule('POST','*')
	bkt.set_cors(config)
	out_storage_info(XSU,headers)
	'''
	for bucket in s3_conn.get_all_buckets():
		key=bucket.get_key("def")
		key.set_contents_from_filename("/etc/hosts")
		#print "{name}\t{created}".format(name=bucket.name,created=bucket.creation_date)
	out_storage_info(XSU,headers)
	'''
	
