#coding=utf-8
import os,sys,rados
import pdb


if __name__=="__main__":
	try:
		cluster=rados.Rados(conffile='/etc/ceph/ceph.conf')
	except TypeError as e:
		print 'AArgument validation error: ', e
		raise e
	print "Created cluster handle."
	try:
		pdb.set_trace()
		cluster.connect()
		print cluster.get_fsid()
		cluster_stats=cluster.get_cluster_stats()
		for pool in cluster.list_pools():
			ioctx=cluster.open_ioctx(str(pool))
			obj_iter = ioctx.list_objects()
			while True:
				try:
					obj=obj_iter.next()
					obj_path='%s/%s'%(str(pool),str(obj.key))
					os.system('mkdir -p %s'%obj_path)
					with open('%s/obj'%obj_path,'w') as fp:
						fp.write(obj.read())
				except StopIteration:
					break
			ioctx.close()
	except Exception as e:
		print "connection error:",e
		raise e
	finally:
		print "Connected to the cluster."
